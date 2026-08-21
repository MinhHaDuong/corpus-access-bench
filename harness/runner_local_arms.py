#!/usr/bin/env python3
"""Local-model arms B / A / D — tool-loop runner, sequential, runs on the
machine serving the model.

Same block structure as runner_local.py (fresh session per 10 questions,
global tool-call cap). Toolsets per arm:
  B : grep_txt / read_pages over the whole-volume text extracts (printed
      folios computed from form-feed page index + per-volume offset).
  A : arm-B tools + grep_map / read_map over the corpus map; the canon
      roster is inlined in the prompt.
  D : web_search (DuckDuckGo HTML) + web_fetch (urllib + tag strip) — a
      best-effort web arm; coverage caveat reported with the results.
"""
import argparse
import html
import os
import json
import logging
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

log = logging.getLogger("runner")
BASE = Path(os.environ.get("BENCH_DIR", Path.home() / "corpus-bench"))
MAP_FILE = BASE / os.environ.get("BENCH_MAP", "corpus-map.md")
CANON_FILE = BASE / os.environ.get("BENCH_CANON", "corpus-canon.md")
OFFSETS = {"I": 27, "II": 11, "III": 10}
_PAGES = {}


def pages(vol):
    if vol not in _PAGES:
        _PAGES[vol] = (BASE / f"extraits/vol{vol}.txt").read_text(encoding="utf-8").split("\f")
    return _PAGES[vol]


def api(endpoint, messages, max_tokens):
    payload = {"messages": messages, "max_tokens": max_tokens, "cache_prompt": True}
    req = urllib.request.Request(endpoint + "/v1/chat/completions",
                                 json.dumps(payload).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        return json.load(r)


def tool_grep_txt(pattern, max_hits=25):
    max_hits = min(int(max_hits or 25), 50)
    try:
        rx = re.compile(pattern, re.I)
    except re.error as e:
        return f"regex invalide : {e}"
    hits = []
    for vol in ("I", "II", "III"):
        off = OFFSETS[vol]
        for i, page in enumerate(pages(vol)):
            for line in page.splitlines():
                if rx.search(line):
                    folio = i + 1 - off
                    hits.append(f"vol{vol} folio {folio}: {line.strip()[:180]}")
                    if len(hits) >= max_hits + 1:
                        break
            if len(hits) >= max_hits + 1:
                break
    extra = "\n[résultats tronqués — précise le motif]" if len(hits) > max_hits else ""
    return ("\n".join(hits[:max_hits]) + extra) if hits else "aucune occurrence"


def tool_read_pages(vol, folio, n=2):
    vol = str(vol).upper().replace("VOL", "").strip()
    if vol not in OFFSETS:
        return "volume inconnu (I | II | III)"
    n = min(int(n or 2), 4)
    ps, off = pages(vol), OFFSETS[vol]
    out = []
    for f in range(int(folio), int(folio) + n):
        idx = f + off - 1
        if 0 <= idx < len(ps):
            out.append(f"<!-- vol{vol} folio {f} -->\n{ps[idx].strip()}")
    return "\n\n".join(out) if out else "folio hors limites"


def tool_grep_map(pattern, max_hits=25):
    max_hits = min(int(max_hits or 25), 50)
    try:
        rx = re.compile(pattern, re.I)
    except re.error as e:
        return f"regex invalide : {e}"
    lines = [ln[:250] for ln in MAP_FILE.read_text(encoding="utf-8").splitlines() if rx.search(ln)]
    extra = f"\n[... {len(lines) - max_hits} lignes omises]" if len(lines) > max_hits else ""
    return ("\n".join(lines[:max_hits]) + extra) if lines else "aucune occurrence"


def _http_get(url, limit=120_000):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (bench-het)"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read(limit).decode("utf-8", "replace")


def tool_web_search(query):
    try:
        raw = _http_get("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(str(query)))
    except Exception as e:
        return f"recherche indisponible : {e}"
    out = []
    for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>',
                         raw, re.S):
        url = urllib.parse.parse_qs(urllib.parse.urlparse(m.group(1)).query).get("uddg", [m.group(1)])[0]
        title = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        snip = html.unescape(re.sub(r"<[^>]+>", "", m.group(3)))[:200]
        out.append(f"- {title}\n  {url}\n  {snip}")
        if len(out) >= 8:
            break
    return "\n".join(out) if out else "aucun résultat"


def tool_web_fetch(url):
    try:
        raw = _http_get(str(url))
    except Exception as e:
        return f"échec du fetch : {e}"
    raw = re.sub(r"(?is)<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", raw)
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:8000] + ("\n[tronqué]" if len(text) > 8000 else "")


TOOLSETS = {
    "B": {"grep_txt": lambda s: tool_grep_txt(s.get("pattern", ""), s.get("max", 25)),
          "read_pages": lambda s: tool_read_pages(s.get("vol", ""), s.get("folio", 1), s.get("n", 2))},
    "A": {"grep_txt": lambda s: tool_grep_txt(s.get("pattern", ""), s.get("max", 25)),
          "read_pages": lambda s: tool_read_pages(s.get("vol", ""), s.get("folio", 1), s.get("n", 2)),
          "grep_map": lambda s: tool_grep_map(s.get("pattern", ""), s.get("max", 25))},
    "D": {"web_search": lambda s: tool_web_search(s.get("query", "")),
          "web_fetch": lambda s: tool_web_fetch(s.get("url", ""))},
}

TOOL_DOC = {
    "B": '''TOOL: {{"name": "grep_txt", "pattern": "expression", "max": 25}}   (cherche dans les trois volumes ; rend volume + folio imprimé)
TOOL: {{"name": "read_pages", "vol": "I", "folio": 174, "n": 2}}   (lit n folios imprimés, n<=4)''',
    "A": '''TOOL: {{"name": "grep_map", "pattern": "expression", "max": 25}}   (cherche dans la carte : titre | volume:folios | auteur | renvois)
TOOL: {{"name": "grep_txt", "pattern": "expression", "max": 25}}   (cherche dans le texte des trois volumes ; rend volume + folio)
TOOL: {{"name": "read_pages", "vol": "I", "folio": 174, "n": 2}}   (lit n folios imprimés, n<=4)''',
    "D": '''TOOL: {{"name": "web_search", "query": "..."}}
TOOL: {{"name": "web_fetch", "url": "https://..."}}''',
}

RESOURCES = {
    "B": "les trois volumes du the reference work (the reference work's editors, the publisher, 2016) en texte intégral, accessibles par les outils ci-dessous (grep pour localiser, lecture par folio imprimé).",
    "A": '''une carte du champ extraite du the reference work (the reference work's editors, the publisher, 2016) — 196 notices, folios imprimés, 1613 renvois — interrogeable par grep_map, plus le texte intégral des trois volumes (grep_txt, read_pages). La carte ne dit pas le contenu : elle route vers des pages ; pour répondre au fond, lis les pages. Voici la liste des notices (canon) :

{canon}''',
    "D": "le web, exclusivement (web_search, web_fetch). Cite tes sources web. Couverture best-effort : si la recherche échoue, dis-le et abstiens-toi.",
}

PROMPT = """Réponds à un questionnaire d'histoire de la pensée économique.

Préambule et questions de ce tour ({label}) :
<feuille-de-reponse.md>
{feuille}
</feuille-de-reponse.md>

RESSOURCES : {resources}

OUTILS — un seul par tour, en TERMINANT ta réponse par une ligne exactement de la forme :
{tooldoc}
Le résultat te sera donné au tour suivant. Plafond global : {maxcalls} appels pour l'ensemble du questionnaire. Aucun autre accès n'existe.

CONSIGNE : ce tour couvre les questions {label} (les autres tours sont traités séparément). Réponds à CHACUNE, 150 mots max, en gardant la numérotation d'origine, en français. Si tu ne sais pas, dis-le : une abstention honnête est notée séparément d'une erreur affirmée, et vaut mieux qu'elle. N'invente aucune référence. Quand tu as fini tes recherches pour ce tour, rends tes réponses COMPLÈTES en un seul tour, précédées de la ligne FINAL, suivies d'une ligne SOURCES USED: <sources réellement consultées dans ce tour>. Pas de préambule, pas de commentaire de méthode."""


def split_feuille(text, block_size):
    qs = re.split(r"^(?=\d{1,2}\. )", text, flags=re.M)
    preamble, questions = qs[0], qs[1:]
    assert len(questions) == 60, f"{len(questions)} questions parsées"
    return preamble, [(f"{i + 1}-{i + block_size}", "".join(questions[i:i + block_size]))
                      for i in range(0, 60, block_size)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=["B", "A", "D"], required=True)
    ap.add_argument("--endpoint", default="http://127.0.0.1:8080")
    ap.add_argument("--max-calls", type=int, default=200)
    ap.add_argument("--block-size", type=int, default=10)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    resources = RESOURCES[args.arm]
    if args.arm == "A":
        resources = resources.format(canon=CANON_FILE.read_text(encoding="utf-8"))
    tools = TOOLSETS[args.arm]
    output = BASE / f"answers-{args.arm}-qwen.md"
    transcript = BASE / f"transcript-{args.arm}-qwen.jsonl"

    preamble, blocks = split_feuille((BASE / "feuille-de-reponse.md").read_text(encoding="utf-8"), args.block_size)
    t0, calls, gen_sum, peak = time.time(), [0], 0, 0
    parts = []
    with transcript.open("w") as tr:
        for label, qtext in blocks:
            messages = [{"role": "user", "content": PROMPT.format(
                feuille=preamble + qtext, label=label, resources=resources,
                tooldoc=TOOL_DOC[args.arm], maxcalls=args.max_calls)}]
            while True:
                r = api(args.endpoint, messages, max_tokens=24000)
                u = r.get("usage", {})
                gen_sum += u.get("completion_tokens", 0)
                peak = max(peak, u.get("prompt_tokens", 0))
                content = r["choices"][0]["message"].get("content") or ""
                tr.write(json.dumps({"block": label, "assistant": content, "usage": u}, ensure_ascii=False) + "\n")
                tr.flush()
                messages.append({"role": "assistant", "content": content})
                m = re.search(r"^TOOL:\s*(\{.*\})\s*$", content, flags=re.M)
                if re.search(r"^FINAL\s*$", content, flags=re.M) or not m:
                    final = content.split("FINAL", 1)[-1].strip() if "FINAL" in content else content
                    final = re.sub(r"^\s*TOOL CALLS:.*$", "", final, flags=re.M)
                    final = re.sub(r"^\s*SOURCES USED:(.*)$", r"[sources du bloc :\1]", final, flags=re.M)
                    parts.append(final.strip())
                    break
                calls[0] += 1
                if calls[0] > args.max_calls:
                    messages.append({"role": "user", "content": "Plafond global atteint. Rends tes réponses FINALES maintenant."})
                    continue
                try:
                    spec = json.loads(m.group(1))
                    fn = tools.get(spec.get("name"))
                    result = fn(spec) if fn else f"outil inconnu : {spec.get('name')} ({' | '.join(tools)})"
                except Exception as e:
                    result = f"erreur d'analyse du TOOL: {e}"
                warn = ("\nATTENTION : contexte presque plein — termine et rends tes réponses FINALES."
                        if peak > 90_000 else "")
                messages.append({"role": "user", "content": f"RÉSULTAT ({calls[0]}/{args.max_calls}) :\n{result[:12000]}{warn}"})
                log.info("bras %s | bloc %s | call %d | prompt %d | gen %d", args.arm, label, calls[0], peak, gen_sum)
            log.info("bloc %s FINI | appels cumulés %d", label, calls[0])
    copy = ("\n\n".join(parts)
            + f"\n\nTOOL CALLS: {calls[0]}\n"
            + "SOURCES USED: détail par bloc ci-dessus.\n")
    output.write_text(copy, encoding="utf-8")
    stats = {"arm": args.arm, "tool_calls": calls[0], "generation_tokens": gen_sum,
             "prompt_tokens_peak": peak, "wall_seconds": round(time.time() - t0), "blocks": len(blocks)}
    Path(str(output) + ".stats.json").write_text(json.dumps(stats))
    log.info("FINI %s", stats)


if __name__ == "__main__":
    main()
