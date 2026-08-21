"""Apply the naming policy to files published as-is (prompts, campaign notes).

`extract_public_split.py` redacts what it generates. The French artefacts
committed verbatim — the arm prompts, the rubric, the campaign preregistrations
and result notes — need the same pass, from the same rule file, so one policy
governs the whole tree.

The redacted copies are no longer verbatim, and say so. The originals stay with
the sealed instrument and are recorded in `instrument/MANIFEST.sha256`: the
naming is part of what is withheld, not an editorial preference.
"""

import argparse
import json
import pathlib
import re

BANNER = ("> Redacted under the naming policy (PROTOCOL.md): the two reference\n"
          "> works are described by role, never named. The unredacted original is\n"
          "> sealed with the instrument and recorded in `instrument/MANIFEST.sha256`.\n")


def load_rules(path: pathlib.Path) -> list[tuple[re.Pattern[str], str]]:
    spec = json.loads(path.read_text())
    return [(re.compile(pat), repl) for pat, repl in spec["patterns"]]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="+", type=pathlib.Path)
    ap.add_argument("--rules", type=pathlib.Path,
                    default=pathlib.Path(__file__).with_name("redactions.json"))
    ap.add_argument("--banner", action="store_true",
                    help="prepend a note saying the file was redacted")
    args = ap.parse_args()

    rules = load_rules(args.rules)
    for path in args.files:
        text = original = path.read_text()
        for pat, repl in rules:
            text = pat.sub(repl, text)
        if text == original:
            print(f"unchanged  {path}")
            continue
        if args.banner and not text.startswith("> Redacted"):
            text = BANNER + "\n" + text
        path.write_text(text)
        print(f"redacted   {path}")


if __name__ == "__main__":
    main()
