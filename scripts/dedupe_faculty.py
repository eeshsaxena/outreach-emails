#!/usr/bin/env python3
"""Merge duplicate faculty entries in research/faculty_master.csv.

A "duplicate" here is two or more rows describing the *same person at the same
institute* that differ only in the guessed email spelling, e.g.

    Punit Gupta | IIIT Gwalior | pgupta@iiitm.ac.in
    Punit Gupta | IIIT Gwalior | punitg@iiitm.ac.in

Matching is deliberately conservative, because a wrong merge silently deletes a
real contact. Two rows are merged only when *both* hold:

  1. normalized (name, institute) match, and
  2. their `personal_site` values do not disagree -- i.e. at most one distinct
     non-blank URL across the group.

Rule 2 is what keeps distinct people apart. `research/faculty_master.csv`
contains rows whose `name` was mis-scraped as the institute name (two different
NIT Trichy faculty both stored as name="NIT Trichy"); they share a (name,
institute) key but point at different faculty profile pages, so rule 2 holds
them apart. It likewise separates same-name colleagues with their own profiles.

Both email spellings are guesses and either may be the deliverable one, so the
extra rows are *merged*, not dropped: the first row is kept and the competing
emails are appended to its `notes` column as `alt email: ...`. The one exception
is scraped placeholders like `my-first-name@cse.iitb.ac.in`, which are
anti-scraping text rather than addresses and are discarded.

Usage:
    python scripts/dedupe_faculty.py [--dry-run]
"""

import argparse
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MASTER = os.path.join(ROOT, "research", "faculty_master.csv")

# Faculty pages sometimes print an instruction instead of an address, e.g.
# "my-first-name@cse.iitb.ac.in". These are not deliverable and are not kept.
PLACEHOLDER = re.compile(
    r"my-first-name|first-?name|last-?name|your-?name|example\.(com|org)|@example",
    re.IGNORECASE,
)


def norm(value):
    """Collapse a name/institute to comparable letters only."""
    return re.sub(r"[^a-z]", "", (value or "").lower())


def site_of(row):
    return (row.get("personal_site") or "").strip().rstrip("/").lower()


def mergeable(group, candidate):
    """True when candidate describes the same person as everything in group.

    Guards against merging distinct people who share a (name, institute) key by
    requiring that the group's non-blank personal_site URLs stay consistent.
    """
    sites = {site_of(r) for r in group + [candidate]}
    return len({s for s in sites if s}) <= 1


def merge_notes(notes, alt_email):
    """Append an `alt email:` entry to a notes cell without duplicating it."""
    if not alt_email or alt_email in (notes or ""):
        return notes
    return f"{notes}; alt email: {alt_email}" if notes else f"alt email: {alt_email}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change without writing the file")
    args = ap.parse_args()

    with open(MASTER, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        rows = list(reader)

    kept = []
    groups = {}          # (name, institute) -> list of rows already kept
    merged = dropped = held = 0

    for row in rows:
        key = (norm(row["name"]), norm(row["institute"]))
        group = groups.get(key)

        # No reliable identity, or no prior row to merge into: keep it.
        if not key[0] or not key[1] or not group:
            if key[0] and key[1]:
                groups[key] = [row]
            kept.append(row)
            continue

        if not mergeable(group, row):
            held += 1
            print(f"held apart: {row['name']} @ {row['institute']} "
                  f"({row['email']}) -- personal_site differs, treating as a "
                  f"distinct person")
            group.append(row)
            kept.append(row)
            continue

        target = group[0]
        alt = (row["email"] or "").strip()
        if PLACEHOLDER.search(alt):
            print(f"merged:     {row['name']} @ {row['institute']} "
                  f"-- discarded placeholder {alt}")
            dropped += 1
        elif alt and alt.lower() != (target["email"] or "").strip().lower():
            target["notes"] = merge_notes(target["notes"], alt)
            print(f"merged:     {row['name']} @ {row['institute']} "
                  f"({target['email']} <- {alt})")
        else:
            print(f"merged:     {row['name']} @ {row['institute']} "
                  f"-- identical email")
        merged += 1

    print(f"\n{len(rows)} rows in -> {len(kept)} rows out "
          f"({merged} merged, {dropped} placeholder emails discarded, "
          f"{held} held apart)")

    if args.dry_run:
        print("dry run: no file written")
        return 0

    if not merged:
        print("nothing to do")
        return 0

    with open(MASTER, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        writer.writerows(kept)
    print(f"wrote {MASTER}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
