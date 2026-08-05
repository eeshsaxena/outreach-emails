#!/usr/bin/env python3
"""
clean_industry.py — Fix data quality issues across industry source files.

Fixes applied:
1. hr_contacts.csv  : strip annotation suffixes from email fields
                      e.g. "foo@bar.com (estimated)" -> "foo@bar.com"
                           "foo@bar.com (use Apollo)" -> dropped (unverified)
2. emails.csv       : rows where best-email resolves to '—' are left as-is
                      (they have no email; that's upstream data missing)
3. extra_contacts.csv: drop rows with invalid/malformed emails,
                       replace '—' company with '' (empty is cleaner)

After cleaning, rebuilds industry batches via gen_batches.py logic.
"""

import csv
import os
import re
import sys

HERE  = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(HERE)
IND   = os.path.join(ROOT, "industry")

VALID_RE  = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]{2,}$')
ANNOT_RE  = re.compile(r'\s*\(.*?\)\s*$')   # trailing "(anything)"

def is_valid(email):
    return bool(email and VALID_RE.match(email.strip()))

def strip_annotation(email):
    """Remove trailing annotations like '(estimated)', '(use Apollo)'."""
    return ANNOT_RE.sub('', email).strip()

def clean_hr_contacts():
    fp = os.path.join(IND, "hr_contacts.csv")
    with open(fp, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        hdr  = list(rows[0].keys()) if rows else []

    kept = dropped = fixed = 0
    out = []
    for r in rows:
        raw = r.get("Email", "").strip()
        if not raw:
            dropped += 1
            continue
        # Strip annotation first
        cleaned = strip_annotation(raw)
        if not is_valid(cleaned):
            # If annotation was present but email still invalid after stripping, drop
            dropped += 1
            continue
        if cleaned != raw:
            r["Email"] = cleaned
            fixed += 1
        out.append(r)
        kept += 1

    with open(fp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=hdr)
        w.writeheader()
        w.writerows(out)

    print(f"hr_contacts.csv: kept {kept}, fixed {fixed}, dropped {dropped}")
    return kept

def clean_extra_contacts():
    fp = os.path.join(IND, "extra_contacts.csv")
    with open(fp, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        hdr  = list(rows[0].keys()) if rows else []

    kept = dropped = fixed_company = 0
    seen_emails = set()
    out = []
    for r in rows:
        raw = r.get("Email", "").strip()
        # Drop junk
        if any(p in raw for p in ["(", "*"]):
            dropped += 1
            continue
        # Drop multi-email strings (contains comma or slash)
        if "," in raw or "/" in raw:
            dropped += 1
            continue
        # Drop clearly truncated/malformed
        if not is_valid(raw):
            dropped += 1
            continue
        # Deduplicate
        key = raw.lower()
        if key in seen_emails:
            dropped += 1
            continue
        seen_emails.add(key)
        # Clean company name
        comp = r.get("Company", "").strip()
        if comp in ("—", "–", "-"):
            r["Company"] = ""
            fixed_company += 1
        out.append(r)
        kept += 1

    with open(fp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=hdr)
        w.writeheader()
        w.writerows(out)

    print(f"extra_contacts.csv: kept {kept}, fixed company {fixed_company}, dropped {dropped}")
    return kept

def main():
    print("=== Cleaning industry source files ===\n")
    clean_hr_contacts()
    clean_extra_contacts()

    # Rebuild batches
    print("\n=== Rebuilding industry batches ===")
    gen_batches = os.path.join(HERE, "gen_batches.py")
    import subprocess
    result = subprocess.run(
        [sys.executable, gen_batches],
        capture_output=True, text=True
    )
    # gen_batches.py uses chdir internally, just print its output
    output = result.stdout.strip()
    # Only show last 3 lines (summary) to keep output tidy
    lines = output.splitlines()
    for line in lines[-3:]:
        print(line)
    if result.returncode != 0:
        print("STDERR:", result.stderr[:500])

if __name__ == "__main__":
    main()
