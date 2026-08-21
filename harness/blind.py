"""Blind a grading round: strip provenance trailers, hash-order copies, write a KEY.

Every candidate copy ends with a `TOOL CALLS:` / `SOURCES USED:` trailer that
names the arm. Judges must not see it. This script cuts the trailer, drops any
leading meta sentence, orders the copies by the SHA-256 of their own blinded
text (so the order carries no information about the arm), and writes the
mapping to a KEY file that stays out of the judges' reach.

Completeness is checked on the *blinded* file, not on the source: in the eval4
Qwen round a repaired block had been appended after the trailer and was
silently cut, and only a judge noticed. See LIMITATIONS.md.
"""

import argparse
import hashlib
import pathlib
import re


def strip(text: str) -> str:
    text = re.split(r"\n\s*(?:---\s*\n\s*)?\**TOOL CALLS\**\s*:", text)[0]
    text = re.sub(r"^.*?(?=^\s*(?:\*\*)?1[.\)])", "", text, count=1, flags=re.S | re.M)
    return text.rstrip() + "\n"


def numbered_answers(text: str) -> int:
    return len(re.findall(r"^\s*(?:\*\*)?(\d{1,2})[.\)]", text, re.M))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--answers", type=pathlib.Path, required=True,
                    help="directory of candidate copies, one .md per arm")
    ap.add_argument("--salted", type=pathlib.Path, required=True,
                    help="the salted copy for this round")
    ap.add_argument("--out", type=pathlib.Path, required=True,
                    help="directory to write copie-N.md into")
    ap.add_argument("--key", type=pathlib.Path, required=True,
                    help="where to write the de-anonymisation key")
    ap.add_argument("--expect", type=int, default=60,
                    help="expected number of numbered answers per copy")
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    pieces = {p.stem: strip(p.read_text()) for p in sorted(args.answers.glob("*.md"))}
    pieces["salted"] = strip(args.salted.read_text())

    order = sorted(pieces, key=lambda k: hashlib.sha256(pieces[k].encode()).hexdigest())
    key = []
    for i, name in enumerate(order, 1):
        (args.out / f"copie-{i}.md").write_text(pieces[name])
        key.append(f"copie-{i} = {name}")
    args.key.write_text("\n".join(key) + "\n")
    print("\n".join(key))

    short = []
    for i in range(1, len(order) + 1):
        n = numbered_answers((args.out / f"copie-{i}.md").read_text())
        print(f"copie-{i}: {n} numbered answers")
        if n != args.expect:
            short.append(f"copie-{i} ({n}/{args.expect})")
    if short:
        raise SystemExit("INCOMPLETE after blinding: " + ", ".join(short))


if __name__ == "__main__":
    main()
