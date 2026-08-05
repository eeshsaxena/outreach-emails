#!/usr/bin/env python3
"""
gen_research_batches.py — Split faculty_master.csv into sendable research batches.

Batching strategy:
    1. Priority 1, queued → first batches (main targets)
    2. Priority 2, queued → later batches
    3. Within each priority: sorted by institute_type (IIT > NIT > IIIT),
       then institute name, then name — so each batch is diverse across institutes.

Batch size: 30 rows  (research emails need heavy personalization; keep batches small)

Output:
    research/batches/research_batch_001.csv  …  research_batch_NNN.csv

Each batch CSV schema:
    name, institute, institute_type, department, email, research_area,
    personal_site, priority, status, state, city, notes

Usage:
    python scripts/gen_research_batches.py
    python scripts/gen_research_batches.py --size 50   # custom batch size
    python scripts/gen_research_batches.py --dry-run   # print summary only
"""

import csv
import os
import re
import sys

HERE    = os.path.dirname(os.path.abspath(__file__))
ROOT    = os.path.dirname(HERE)
MASTER  = os.path.join(ROOT, "research", "faculty_master.csv")
OUT_DIR = os.path.join(ROOT, "research", "batches")

BATCH_SIZE = 30

HEADER = [
    "name", "institute", "institute_type", "department",
    "email", "research_area", "personal_site",
    "priority", "status", "state", "city", "notes",
]

ITYPE_ORDER = {"IIT": 0, "NIT": 1, "IIIT": 2}
_BATCH_RE   = re.compile(r"^research_batch_\d{3}\.csv$")


def sort_key(row):
    itype   = ITYPE_ORDER.get(row.get("institute_type", ""), 9)
    pri     = int(row.get("priority", "9") or "9")
    return (pri, itype, row.get("institute", ""), row.get("name", ""))


def load_queued():
    if not os.path.exists(MASTER):
        print(f"ERROR: {MASTER} not found.")
        sys.exit(1)
    rows = []
    with open(MASTER, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r.get("status", "").strip().lower() == "queued":
                rows.append(r)
    return rows


def write_batches(rows, batch_size, dry_run=False):
    # Clean old auto-generated batches
    os.makedirs(OUT_DIR, exist_ok=True)
    if not dry_run:
        for old in os.listdir(OUT_DIR):
            if _BATCH_RE.match(old):
                os.remove(os.path.join(OUT_DIR, old))

    total   = 0
    n_batch = (len(rows) + batch_size - 1) // batch_size
    for i in range(0, len(rows), batch_size):
        batch     = rows[i : i + batch_size]
        batch_num = i // batch_size + 1
        fname     = f"research_batch_{batch_num:03d}.csv"
        fpath     = os.path.join(OUT_DIR, fname)

        # Summary line
        itypes = {}
        for r in batch:
            k = r.get("institute_type", "?")
            itypes[k] = itypes.get(k, 0) + 1
        summary = "  ".join(f"{k}:{v}" for k, v in sorted(itypes.items()))
        print(f"  {fname}  ({len(batch)} rows)  [{summary}]")

        if not dry_run:
            with open(fpath, "w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=HEADER, extrasaction="ignore")
                w.writeheader()
                w.writerows(batch)
        total += len(batch)

    return total, n_batch


def main():
    batch_size = BATCH_SIZE
    dry_run    = False
    args       = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--size" and i + 1 < len(args):
            batch_size = int(args[i + 1])
            i += 2
        elif args[i] == "--dry-run":
            dry_run = True
            i += 1
        else:
            i += 1

    rows = load_queued()
    rows.sort(key=sort_key)

    print(f"\nfaculty_master.csv  →  {len(rows)} queued rows")
    by_type = {}
    for r in rows:
        k = r.get("institute_type", "?")
        by_type[k] = by_type.get(k, 0) + 1
    for k, v in sorted(by_type.items()):
        print(f"  {k}: {v}")
    print(f"\nBatch size : {batch_size}")
    print(f"Output dir : {os.path.relpath(OUT_DIR, ROOT)}")
    print(f"{'(dry run — no files written)' if dry_run else ''}\n")

    total, n = write_batches(rows, batch_size, dry_run)
    print(f"\n{'Would generate' if dry_run else 'Generated'}  {total} rows  across  {n} batches.")
    if not dry_run:
        print(f"Batches written to  research/batches/")


if __name__ == "__main__":
    main()
