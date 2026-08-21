"""Guard: no tracked file names either reference work.

The naming policy (PROTOCOL.md, amendment journal) is that published files
describe the two reference works by role and never name them. A policy nobody
checks is a policy that decays at the first hurried commit.

The second test is the one that makes the first worth anything. A grep whose
"all clear" is indistinguishable from "I could not look" is not a check, and the
first version of this scan did in fact return clean while a citation key
(`FaccarelloKurz2016`) sat in the output — the `\\b` after the surname never
matched, because a letter-to-digit transition is not a word boundary. So the
scanner is run against a string known to leak, and must fail on it.
"""

import json
import pathlib
import re
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
FORBIDDEN = json.loads((ROOT / "harness" / "redactions.json").read_text())["forbidden"]
SCAN = re.compile("|".join(FORBIDDEN), re.I)
# This file states the policy, so it necessarily contains the words it forbids.
SELF = {"tests/test_naming_policy.py", "harness/redactions.json"}


def tracked_files() -> list[str]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files"],
                         capture_output=True, text=True, check=True)
    return [f for f in out.stdout.splitlines() if f and f not in SELF]


def scan(text: str) -> list[str]:
    return SCAN.findall(text)


def test_scanner_detects_a_known_positive():
    """Fails if the scanner cannot see a leak it is meant to catch."""
    assert scan("Source : notice Quesnay (FaccarelloKurz2016)"), \
        "scanner blind to a citation-key leak — the exact defect it exists for"
    assert scan("the New Palgrave, s.v. Cantillon")
    assert not scan("a standard multi-volume reference work in the field")


@pytest.mark.parametrize("rel", tracked_files())
def test_tracked_file_names_no_reference_work(rel):
    path = ROOT / rel
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        pytest.skip(f"{rel} is not UTF-8 text")
    hits = scan(text)
    assert not hits, f"{rel} names a reference work: {sorted(set(h.lower() for h in hits))}"
