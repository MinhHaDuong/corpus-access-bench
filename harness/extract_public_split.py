"""Extract the public split of the instrument: one stratum, everything about it.

The control stratum is published in full — statements, answer key, every arm's
answers, every judge's per-question line — while the discriminating strata stay
sealed. See PROTOCOL.md § What is public and why.

Nothing here is hand-copied: the split is derived from the stratum map, so the
public files cannot drift from the sealed ones, and re-running this script after
a correction regenerates them.

    uv run python harness/extract_public_split.py \
        --strata instrument/strata.json --stratum C \
        --questions instrument/questions-par-strate.md \
        --answer-key instrument/corrige.md \
        --campaign 2026-08-v2-sonnet-opus:campaigns/2026-08-v2-sonnet-opus \
        --out public/
"""

import argparse
import json
import pathlib
import re

ANSWER_RE = re.compile(r"^\s*\**(\d{1,2})[.\)]\**\s", re.M)
KEYED_RE = re.compile(r"^\s*\**(\d{1,2})\.\**\s", re.M)
GRADE_RE = re.compile(r"^\s*\**(\d{1,2})[.\)]?\**\s+\**([01](?:[.,]\d+)?)\**\s*[—–-]\s*(.*)$")
COPY_RE = re.compile(r"#+\s*(copie-\d+)")


def sheet_numbers(strata: dict[str, str], letter: str) -> list[int]:
    return sorted(int(n) for n, lab in strata.items() if lab.startswith(letter))


def split_numbered(text: str, pattern: re.Pattern[str]) -> dict[int, str]:
    """Cut a numbered document into {number: block}."""
    marks = [(int(m.group(1)), m.start()) for m in pattern.finditer(text)]
    blocks: dict[int, str] = {}
    for i, (n, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        if n not in blocks:  # first occurrence wins; later ones are stray numerals
            blocks[n] = text[start:end].strip()
    return blocks


def read_key(path: pathlib.Path) -> dict[str, str]:
    key = {}
    for line in path.read_text().splitlines():
        if " = " in line:
            c, a = line.split(" = ")
            key[c.strip()] = a.strip()
    return key


def load_redactions(path: pathlib.Path | None) -> list[tuple[re.Pattern[str], str]]:
    if path is None:
        return []
    spec = json.loads(path.read_text())
    return [(re.compile(pat), repl) for pat, repl in spec["patterns"]]


def redact(text: str, rules: list[tuple[re.Pattern[str], str]]) -> str:
    for pat, repl in rules:
        text = pat.sub(repl, text)
    return text


def emit_questions(master: pathlib.Path, strata: dict[str, str], letter: str,
                   wanted: list[int], out: pathlib.Path,
                   rules: list[tuple[re.Pattern[str], str]]) -> None:
    """Pull the labelled statements (C1., C2., …) out of the master question file."""
    text = redact(master.read_text(), rules)
    labels = {strata[str(n)]: n for n in wanted}
    body = [f"# Public split — stratum {letter}, {len(wanted)} statements", "",
            "Sheet numbers are the positions on the shuffled answer sheet served to",
            "the arms; the stratum label was never shown to them.", ""]
    for label in sorted(labels, key=lambda lb: labels[lb]):
        m = re.search(rf"^{re.escape(label)}\.\s+(.*?)(?=^\w+\d+\.\s|^#|\Z)",
                      text, re.M | re.S)
        if not m:
            raise SystemExit(f"statement {label} not found in {master}")
        body.append(f"**{label} (sheet {labels[label]}).** {m.group(1).strip()}\n")
    out.write_text("\n".join(body) + "\n")


def emit_blocks(src: pathlib.Path, pattern: re.Pattern[str], wanted: list[int],
                strata: dict[str, str], out: pathlib.Path, header: str,
                rules: list[tuple[re.Pattern[str], str]]) -> int:
    blocks = split_numbered(redact(src.read_text(), rules), pattern)
    body = [header, ""]
    found = 0
    for n in wanted:
        if n in blocks:
            found += 1
            body.append(f"### {strata[str(n)]} (sheet {n})\n\n{blocks[n]}\n")
        else:
            body.append(f"### {strata[str(n)]} (sheet {n})\n\n*(absent from this copy)*\n")
    out.write_text("\n".join(body) + "\n")
    return found


def emit_grades(src: pathlib.Path, key: dict[str, str], wanted: list[int],
                strata: dict[str, str], out: pathlib.Path, header: str,
                rules: list[tuple[re.Pattern[str], str]]) -> None:
    body = [header, ""]
    cur = None
    rows: dict[str, list[str]] = {}
    for line in redact(src.read_text(), rules).splitlines():
        m = COPY_RE.match(line.strip())
        if m:
            cur = key.get(m.group(1), m.group(1))
            rows[cur] = []
            continue
        if cur:
            g = GRADE_RE.match(line.strip())
            if g and int(g.group(1)) in wanted:
                n = int(g.group(1))
                rows[cur].append(f"- **{strata[str(n)]}** (sheet {n}) — "
                                 f"`{g.group(2).replace(',', '.')}` — {g.group(3)}")
    for arm, lines in rows.items():
        body.append(f"## {arm}\n")
        body.extend(lines or ["*(no line parsed)*"])
        body.append("")
    out.write_text("\n".join(body) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strata", type=pathlib.Path, required=True)
    ap.add_argument("--stratum", default="C", help="stratum letter to publish")
    ap.add_argument("--questions", type=pathlib.Path, required=True)
    ap.add_argument("--answer-key", type=pathlib.Path, required=True)
    ap.add_argument("--campaign", action="append", default=[],
                    help="NAME:PATH of a campaign directory holding raw/")
    ap.add_argument("--redactions", type=pathlib.Path,
                    default=pathlib.Path(__file__).with_name("redactions.json"),
                    help="naming-policy substitutions applied to every public file")
    ap.add_argument("--out", type=pathlib.Path, required=True)
    args = ap.parse_args()

    strata = json.loads(args.strata.read_text())
    rules = load_redactions(args.redactions)
    wanted = sheet_numbers(strata, args.stratum)
    args.out.mkdir(parents=True, exist_ok=True)
    print(f"stratum {args.stratum}: {len(wanted)} questions -> {wanted}")

    emit_questions(args.questions, strata, args.stratum, wanted,
                   args.out / "questions.md", rules)
    n = emit_blocks(args.answer_key, KEYED_RE, wanted, strata,
                    args.out / "answer-key.md",
                    f"# Public split — answer key, stratum {args.stratum}\n\n"
                    "Built from a second reference work and the open web, never from the\n"
                    "corpus the arms worked on. Points marked *corrigé incertain*\n"
                    "were outside the scale.", rules)
    print(f"answer key: {n}/{len(wanted)} entries")

    for spec in args.campaign:
        name, _, path = spec.partition(":")
        cdir = pathlib.Path(path)
        odir = args.out / name
        odir.mkdir(parents=True, exist_ok=True)
        for ans in sorted(cdir.glob("raw/answers*/*.md")):
            tag = f"{ans.parent.name}-{ans.stem}".replace("answers-", "").replace("answers", "")
            n = emit_blocks(ans, ANSWER_RE, wanted, strata,
                            odir / f"answers-{tag.strip('-')}.md",
                            f"# {name} — {ans.stem}, stratum {args.stratum}", rules)
            print(f"{name} {ans.stem}: {n}/{len(wanted)} answers")
        for notes in sorted(cdir.glob("raw/notes*")):
            round_tag = notes.name.replace("notes-", "").replace("notes", "round")
            keyfile = next(iter(sorted(cdir.glob(f"raw/KEY*{round_tag}*.txt"))), None)
            key = read_key(keyfile) if keyfile else {}
            for judge in sorted(notes.glob("juge*.md")):
                emit_grades(judge, key, wanted, strata,
                            odir / f"grades-{round_tag}-{judge.stem}.md",
                            f"# {name} — {judge.stem}, stratum {args.stratum}\n\n"
                            "Copies are named by arm here; the judges saw them blinded.",
                            rules)
            print(f"{name} {notes.name}: {len(list(notes.glob('juge*.md')))} judge files")


if __name__ == "__main__":
    main()
