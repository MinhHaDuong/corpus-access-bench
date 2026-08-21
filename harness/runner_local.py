#!/usr/bin/env python3
"""Tool-loop runner for the Qwen B' arm — runs ON padme, corpus local.

Blocks of --block-size questions, each in a fresh session, so the 131k
context never accumulates 60 questions of tool results and reasoning.
Prompt-based tool protocol (ls/grep/read), locked to the corpus directory;
global cap of --max-calls tool calls across all blocks.
"""
import argparse
import json
import logging
import re
import subprocess
import time
import urllib.request
from pathlib import Path

log = logging.getLogger("runner")
CORPUS = Path("corpus")
FEUILLE = Path("feuille-de-reponse.md")


def api(endpoint, messages, max_tokens):
    payload = {"messages": messages, "max_tokens": max_tokens, "cache_prompt": True}
    req = urllib.request.Request(endpoint + "/v1/chat/completions",
                                 json.dumps(payload).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        return json.load(r)


def tool_ls():
    return "\n".join(sorted(p.name for p in CORPUS.glob("*.md") if p.name != "README.md"))


def tool_grep(pattern, max_lines=30):
    max_lines = min(int(max_lines or 30), 60)
    try:
        out = subprocess.run(["grep", "-rniE", "--include=*.md", pattern, str(CORPUS)],
                             capture_output=True, timeout=30).stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return "grep: timeout"
    lines = [ln.replace(str(CORPUS) + "/", "")[:220] for ln in out.splitlines()]
    extra = f"\n[... {len(lines) - max_lines} lignes omises]" if len(lines) > max_lines else ""
    return ("\n".join(lines[:max_lines]) + extra) if lines else "aucune occurrence"


def tool_read(fname, start_line=1, max_lines=120):
    target = CORPUS / Path(str(fname)).name
    if not target.exists() or target.name == "README.md":
        return f"fichier inconnu : {fname} (utilise ls)"
    lines = target.read_text(encoding="utf-8").splitlines()
    s = max(1, int(start_line or 1)) - 1
    n = min(int(max_lines or 120), 200)
    chunk = lines[s:s + n]
    tail = (f"\n[fichier {len(lines)} lignes ; suite : start_line={s + n + 1}]"
            if s + n < len(lines) else "\n[fin du fichier]")
    return "\n".join(chunk) + tail


def run_tool(spec):
    name = spec.get("name")
    if name == "ls":
        return tool_ls()
    if name == "grep":
        return tool_grep(spec.get("pattern", ""), spec.get("max", 30))
    if name == "read":
        return tool_read(spec.get("file", ""), spec.get("start_line", 1), spec.get("max_lines", 120))
    return f"outil inconnu : {name} (ls | grep | read)"


PROMPT = """Réponds à un questionnaire d'histoire de la pensée économique.

Préambule et questions de ce tour ({label}) :
<feuille-de-reponse.md>
{feuille}
</feuille-de-reponse.md>

RESSOURCES : le the reference work (the reference work's editors, the publisher, 2016) converti en répertoire de 196 fichiers Markdown, un par notice (I = personnes, II = écoles, III = champs). Nom de fichier : <volume>-<folio début>-<titre>.md. Une notice absente du répertoire n'existe pas dans le reference work. Les marqueurs <!-- p. N --> sont les folios imprimés — cite la page.

OUTILS — un seul par tour, en TERMINANT ta réponse par une ligne exactement de la forme :
TOOL: {{"name": "ls"}}
TOOL: {{"name": "grep", "pattern": "expression", "max": 30}}
TOOL: {{"name": "read", "file": "I-174-antoine-augustin-cournot.md", "start_line": 1, "max_lines": 120}}
Le résultat te sera donné au tour suivant. Plafond global : 200 appels pour l'ensemble du questionnaire. Aucun autre accès (ni web, ni autre fichier) n'existe.

CONSIGNE : ce tour couvre les questions {label} (les autres tours sont traités séparément). Réponds à CHACUNE, 150 mots max, en gardant la numérotation d'origine, en français. Si tu ne sais pas, dis-le : une abstention honnête est notée séparément d'une erreur affirmée, et vaut mieux qu'elle. N'invente aucune référence. Quand tu as fini tes recherches pour ce tour, rends tes réponses COMPLÈTES en un seul tour, précédées de la ligne FINAL, suivies d'une ligne SOURCES USED: <notices et folios consultés dans ce tour>. Pas de préambule, pas de commentaire de méthode."""


def split_feuille(text, block_size):
    qs = re.split(r"^(?=\d{1,2}\. )", text, flags=re.M)
    preamble, questions = qs[0], qs[1:]
    assert len(questions) == 60, f"{len(questions)} questions parsées"
    return preamble, [(f"{i + 1}-{i + block_size}", "".join(questions[i:i + block_size]))
                      for i in range(0, 60, block_size)]


def run_block(endpoint, preamble, label, qtext, calls_state, max_calls, tr):
    messages = [{"role": "user", "content": PROMPT.format(feuille=preamble + qtext, label=label)}]
    total_gen, prompt_peak = 0, 0
    while True:
        r = api(endpoint, messages, max_tokens=24000)
        u = r.get("usage", {})
        total_gen += u.get("completion_tokens", 0)
        prompt_peak = max(prompt_peak, u.get("prompt_tokens", 0))
        content = r["choices"][0]["message"].get("content") or ""
        tr.write(json.dumps({"block": label, "assistant": content, "usage": u}, ensure_ascii=False) + "\n")
        tr.flush()
        messages.append({"role": "assistant", "content": content})
        m = re.search(r"^TOOL:\s*(\{.*\})\s*$", content, flags=re.M)
        if re.search(r"^FINAL\s*$", content, flags=re.M) or not m:
            final = content.split("FINAL", 1)[-1].strip() if "FINAL" in content else content
            return final, total_gen, prompt_peak
        calls_state[0] += 1
        if calls_state[0] > max_calls:
            messages.append({"role": "user", "content": "Plafond global atteint. Rends tes réponses FINALES maintenant."})
            continue
        try:
            result = run_tool(json.loads(m.group(1)))
        except Exception as e:
            result = f"erreur d'analyse du TOOL: {e}"
        warn = ("\nATTENTION : contexte presque plein — termine et rends tes réponses FINALES."
                if prompt_peak > 90_000 else "")
        messages.append({"role": "user", "content": f"RÉSULTAT ({calls_state[0]}/{max_calls}) :\n{result}{warn}"})
        log.info("bloc %s | call %d | prompt %d | gen %d", label, calls_state[0], prompt_peak, total_gen)


def main():
    global CORPUS, FEUILLE
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", default="http://127.0.0.1:8080")
    ap.add_argument("--corpus", type=Path, default=Path.home() / "qwen-bench/corpus")
    ap.add_argument("--feuille", type=Path, default=Path.home() / "qwen-bench/feuille-de-reponse.md")
    ap.add_argument("--output", type=Path, default=Path.home() / "qwen-bench/answers-Bprime-qwen.md")
    ap.add_argument("--transcript", type=Path, default=Path.home() / "qwen-bench/transcript-Bprime-qwen.jsonl")
    ap.add_argument("--max-calls", type=int, default=200)
    ap.add_argument("--block-size", type=int, default=10)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    CORPUS, FEUILLE = args.corpus, args.feuille

    preamble, blocks = split_feuille(FEUILLE.read_text(encoding="utf-8"), args.block_size)
    t0, calls_state, gen_sum, peak = time.time(), [0], 0, 0
    parts = []
    with args.transcript.open("w") as tr:
        for label, qtext in blocks:
            final, g, p = run_block(args.endpoint, preamble, label, qtext, calls_state, args.max_calls, tr)
            final = re.sub(r"^\s*TOOL CALLS:.*$", "", final, flags=re.M)
            final = re.sub(r"^\s*SOURCES USED:(.*)$", r"[sources du bloc :\1]", final, flags=re.M)
            parts.append(final.strip())
            gen_sum += g
            peak = max(peak, p)
            log.info("bloc %s FINI | appels cumulés %d", label, calls_state[0])
    copy = ("\n\n".join(parts)
            + f"\n\nTOOL CALLS: {calls_state[0]}\n"
            + "SOURCES USED: notices du répertoire Markdown consultées par ls/grep/read — détail par bloc ci-dessus.\n")
    args.output.write_text(copy, encoding="utf-8")
    stats = {"tool_calls": calls_state[0], "generation_tokens": gen_sum, "prompt_tokens_peak": peak,
             "wall_seconds": round(time.time() - t0), "blocks": len(blocks)}
    Path(str(args.output) + ".stats.json").write_text(json.dumps(stats))
    log.info("FINI %s", stats)


if __name__ == "__main__":
    main()
