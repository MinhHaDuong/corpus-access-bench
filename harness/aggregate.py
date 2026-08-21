"""Aggregate one grading round: per-arm, per-stratum, salted detection, agreement.

One invocation per round. Everything that varied between rounds in the original
copy-and-edit scripts (`aggregate2.py`, `aggregate3.py`) is a flag here: the
round directory, the key, the stratum map, and the numbers of the questions
carrying seeded defects.

The salted-question marks are what validates the jury. A panel that does not
catch the seeded defects is not measuring the real copies either — see
PROTOCOL.md § Jury calibration for the pre-registered threshold.
"""

import argparse
import json
import pathlib
import re
import statistics as st

MARK_RE = re.compile(r"\**(\d{1,2})\.?\**[.\)]?\s+\**([01](?:[.,]\d+)?)\**\s*[—–-]")
COPY_RE = re.compile(r"#+\s*(copie-\d+)")


def parse_grades(path: pathlib.Path) -> dict[str, dict[int, float]]:
    """One judge's report -> {copie: {question: mark}}."""
    out: dict[str, dict[int, float]] = {}
    cur = None
    for line in path.read_text().splitlines():
        m = COPY_RE.match(line.strip())
        if m:
            cur = m.group(1)
            out[cur] = {}
            continue
        if cur:
            m = MARK_RE.match(line.strip())
            if m:
                out[cur][int(m.group(1))] = float(m.group(2).replace(",", "."))
    return out


def read_key(path: pathlib.Path) -> dict[str, str]:
    key = {}
    for line in path.read_text().splitlines():
        if " = " in line:
            c, a = line.split(" = ")
            key[c.strip()] = a.strip()
    return key


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--notes", type=pathlib.Path, required=True,
                    help="directory of judge reports (juge*.md)")
    ap.add_argument("--key", type=pathlib.Path, required=True,
                    help="de-anonymisation key written by blind.py")
    ap.add_argument("--strata", type=pathlib.Path, required=True,
                    help="strata.json: {question number: stratum letter}")
    ap.add_argument("--salted-questions", type=int, nargs="*", default=[],
                    help="question numbers carrying the seeded defects of this round")
    ap.add_argument("--n-questions", type=int, default=60)
    ap.add_argument("--label", default="round")
    args = ap.parse_args()

    strata = json.loads(args.strata.read_text())
    key = read_key(args.key)

    judges = {}
    for p in sorted(args.notes.glob("juge*.md")):
        data = parse_grades(p)
        judges[p.stem] = data
        for c, qs in data.items():
            if len(qs) != args.n_questions:
                print(f"  ! {p.stem} {c}: {len(qs)}/{args.n_questions} questions parsed")

    arms = sorted(set(key.values()))
    print(f"\n=== {args.label} — {len(judges)} judge(s) ===\n")

    print(f"{'Copy':<10}" + "".join(f"{j[-12:]:>14}" for j in judges)
          + f"{'mean/' + str(args.n_questions):>9}")
    for a in arms:
        c = next(k for k, v in key.items() if v == a)
        marks = [sum(d.get(c, {}).values()) for d in judges.values()]
        mu = st.mean(marks) if marks else float("nan")
        print(f"{a:<10}" + "".join(f"{m:>14.2f}" for m in marks) + f"{mu:>9.2f}")

    letters = sorted({v[0] for v in strata.values()})
    per = args.n_questions // len(letters)
    print("\n" + f"{'Copy':<10}" + "".join(f"{s + '/' + str(per):>11}" for s in letters))
    for a in arms:
        c = next(k for k, v in key.items() if v == a)
        row = []
        for s in letters:
            vals = [sum(v for q, v in d.get(c, {}).items() if strata[str(q)][0] == s)
                    for d in judges.values()]
            row.append(st.mean(vals) if vals else float("nan"))
        print(f"{a:<10}" + "".join(f"{v:>11.2f}" for v in row))

    if args.salted_questions:
        salted_c = next((k for k, v in key.items() if v == "salted"), None)
        if salted_c:
            print(f"\nSalted copy ({salted_c}) — marks on the seeded questions:")
            for q in args.salted_questions:
                vals = [d.get(salted_c, {}).get(q) for d in judges.values()]
                print(f"  Q{q}: " + " ".join("?" if v is None else f"{v:.2f}" for v in vals))

    if len(judges) > 1:
        diffs = []
        for c in key:
            for q in range(1, args.n_questions + 1):
                vals = [d[c][q] for d in judges.values() if c in d and q in d[c]]
                if len(vals) == len(judges):
                    diffs.append(max(vals) - min(vals))
        n = len(diffs)
        print(f"\nInter-judge agreement over {n} paired marks:")
        print(f"  mean max spread : {st.mean(diffs):.3f}")
        print(f"  identical       : {sum(1 for d in diffs if d == 0)}/{n}")
        print(f"  spread > 0.25   : {sum(1 for d in diffs if d > 0.25)}/{n}")


if __name__ == "__main__":
    main()
