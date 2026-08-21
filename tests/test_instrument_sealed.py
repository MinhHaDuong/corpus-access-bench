"""Guard: the sealed instrument never becomes tracked.

`.gitignore` denies `instrument/*` and `campaigns/*/raw/` by default, which is
the right shape — but a `git add -f`, a renamed directory, or a new campaign
laid out slightly differently defeats it silently, and the failure is
irreversible once pushed. So the invariant is asserted against `git ls-files`
rather than against the ignore file that is supposed to produce it.

As in test_naming_policy, the check is validated against a known positive: a
path that should be refused must actually be refused, or the test proves
nothing.
"""

import pathlib
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALLOWED_IN_INSTRUMENT = {"instrument/README.md", "instrument/MANIFEST.sha256"}


def tracked_files() -> list[str]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files"],
                         capture_output=True, text=True, check=True)
    return [f for f in out.stdout.splitlines() if f]


def is_sealed(path: str) -> bool:
    if path.startswith("instrument/") and path not in ALLOWED_IN_INSTRUMENT:
        return True
    parts = path.split("/")
    return len(parts) > 2 and parts[0] == "campaigns" and parts[2] == "raw"


def test_predicate_refuses_known_sealed_paths():
    assert is_sealed("instrument/corrige.md")
    assert is_sealed("instrument/questions-par-strate.md")
    assert is_sealed("campaigns/2026-08-v2-sonnet-opus/raw/answers-opus/A-map.md")
    assert not is_sealed("instrument/MANIFEST.sha256")
    assert not is_sealed("campaigns/2026-08-v2-sonnet-opus/RESULTS-fr.md")
    assert not is_sealed("public/questions.md")


def test_no_sealed_file_is_tracked():
    leaked = [f for f in tracked_files() if is_sealed(f)]
    assert not leaked, f"sealed material is tracked: {leaked}"


def test_manifest_covers_the_live_instrument():
    """Every sealed file on disk has a digest recorded."""
    manifest = ROOT / "instrument" / "MANIFEST.sha256"
    if not manifest.exists():
        pytest.skip("no manifest yet")
    recorded = {line.split("  ", 1)[1] for line in manifest.read_text().splitlines() if line}
    live = {str(p.relative_to(ROOT / "instrument"))
            for p in (ROOT / "instrument").rglob("*")
            if p.is_file() and p.name not in {"MANIFEST.sha256", "README.md"}}
    if not live:
        pytest.skip("instrument not present in this checkout")
    assert live <= recorded, f"unhashed sealed files: {sorted(live - recorded)}"
