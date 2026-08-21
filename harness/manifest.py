"""Record the SHA-256 of every sealed file, so a campaign can prove which
version of the instrument it sat without exposing its content.

The manifest is the whole protection scheme: the questions, the answer key, the
blinding keys and the seal files never enter git, and the hashes are what make
that omission auditable rather than merely convenient. Seal files are burned
after a campaign; their hash outlives them and is what proves they were sealed
in advance.
"""

import argparse
import hashlib
import pathlib


def digest(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=pathlib.Path, required=True,
                    help="directory to hash (recursively)")
    ap.add_argument("--out", type=pathlib.Path, required=True)
    ap.add_argument("--exclude", nargs="*", default=["MANIFEST.sha256", "README.md"])
    args = ap.parse_args()

    rows = []
    for p in sorted(args.root.rglob("*")):
        if not p.is_file() or p.name in args.exclude:
            continue
        rows.append(f"{digest(p)}  {p.relative_to(args.root)}")
    args.out.write_text("\n".join(rows) + "\n")
    print(f"{len(rows)} files hashed -> {args.out}")


if __name__ == "__main__":
    main()
