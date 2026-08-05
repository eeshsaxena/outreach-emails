#!/usr/bin/env python3
"""Print institutes with fewer than 10 rows."""
import csv, os, glob

fac_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "research", "faculty")
under = []
for fp in sorted(glob.glob(os.path.join(fac_dir, "**", "*.csv"), recursive=True)):
    with open(fp, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    n = len(rows)
    rel = os.path.relpath(fp, fac_dir)
    if n < 10:
        under.append((n, rel))
under.sort()
print(str(len(under)) + " institutes under 10 rows:")
for n, rel in under:
    print("  [" + str(n) + "] " + rel)
