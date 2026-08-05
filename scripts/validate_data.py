#!/usr/bin/env python3
"""Validate repository data files. Run by CI (see .github/workflows/ci.yml).

Checks that every research faculty CSV, plus faculty_master.csv and the research
dead_removed.csv, carries the canonical schema header, and that any populated
institute_type value is one of IIT / NIT / IIIT / IISc / IISER / BITS. Exits
non-zero on any problem so
CI fails loudly instead of letting a malformed row into the dataset.

Usage:
    python scripts/validate_data.py
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESEARCH = os.path.join(ROOT, "research")

FACULTY_HEADER = [
    "name", "state", "city", "institute", "institute_type",
    "department", "email", "research_area", "personal_site",
    "priority", "status", "notes",
]
VALID_TYPES = {"IIT", "NIT", "IIIT", "IISc", "IISER", "BITS"}

errors = []


def header_of(path):
    with open(path, encoding="utf-8", newline="") as f:
        return [c.strip() for c in next(csv.reader(f), [])]


targets = []
faculty_dir = os.path.join(RESEARCH, "faculty")
for dirpath, _, files in os.walk(faculty_dir):
    for fn in files:
        if fn.endswith(".csv"):
            targets.append(os.path.join(dirpath, fn))
for extra in ("faculty_master.csv", "dead_removed.csv"):
    p = os.path.join(RESEARCH, extra)
    if os.path.exists(p):
        targets.append(p)

if not targets:
    errors.append("no research CSVs found to validate")

for path in sorted(targets):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    hdr = header_of(path)
    if hdr != FACULTY_HEADER:
        errors.append(
            f"{rel}: header mismatch\n"
            f"      expected: {FACULTY_HEADER}\n"
            f"      found:    {hdr}"
        )
        continue
    with open(path, encoding="utf-8", newline="") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            t = (row.get("institute_type") or "").strip()
            if t and t not in VALID_TYPES:
                errors.append(f"{rel}:{i}: invalid institute_type {t!r} (want one of {sorted(VALID_TYPES)})")

if errors:
    print("DATA VALIDATION FAILED:\n")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print(f"OK: {len(targets)} research CSV(s) validated (schema + institute_type clean).")
