#!/usr/bin/env python3
"""Structure guard. Run by CI (see .github/workflows/ci.yml).

The repo is organized into tracks: data lives under industry/ and research/,
scripts under scripts/, watcher state under state/. Contributors' tools often
still drop new files (city_*.csv, batch_*.csv, add_*.py, ...) at the repo ROOT,
which breaks the layout. This check fails the build when that happens and tells
the contributor exactly where the file belongs.

Usage:
    python scripts/check_structure.py
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Files that are allowed to sit at the repo root.
ALLOWED = {
    "README.md", "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
    "CONTRIBUTORS.md", "requirements.txt", ".gitignore", ".gitattributes",
    # Intentional root deliverables: the de-duplicated master email lists,
    # auto-maintained by scripts/build_unified_emails.py + the unified-emails
    # workflow. Kept at the root on purpose (one A->Z, one Z->A).
    "unified_emails.csv", "unified_emails_z_to_a.csv",
}

# (regex on the root filename) -> where it should live instead.
RULES = [
    (re.compile(r"^batch_\d+\.csv$", re.I), "industry/batches/"),
    (re.compile(r"^city_.+\.csv$", re.I), "industry/city/"),
    (re.compile(r"^unsorted_.+\.csv$", re.I), "industry/unsorted/"),
    (re.compile(r"^add_.+\.py$", re.I), "scripts/"),
    (re.compile(r".+\.py$", re.I), "scripts/"),
    (re.compile(r"^(emails_.+|.+_emails)$", re.I), "industry/"),
    (re.compile(r".+\.csv$", re.I), "industry/  (or research/ for faculty data)"),
    (re.compile(r".+\.xlsx$", re.I), "industry/"),
]


def destination(name):
    for rx, dest in RULES:
        if rx.match(name):
            return dest
    return None


def main():
    offenders = []
    for name in sorted(os.listdir(ROOT)):
        path = os.path.join(ROOT, name)
        if not os.path.isfile(path) or name in ALLOWED or name.startswith("."):
            continue
        dest = destination(name)
        if dest:
            offenders.append((name, dest))

    if offenders:
        print("STRUCTURE CHECK FAILED: data files must not live at the repo root.\n")
        for name, dest in offenders:
            print(f"  - {name}  ->  move it into  {dest}")
        print("\nSee CONTRIBUTING.md (Repository layout). Move the file(s) into the\n"
              "right folder and update your PR. City batches go in industry/city/,\n"
              "faculty data in research/faculty/<type>/<state>/<city>/.")
        sys.exit(1)

    print("OK: repo root is clean (no stray data files).")


if __name__ == "__main__":
    main()
