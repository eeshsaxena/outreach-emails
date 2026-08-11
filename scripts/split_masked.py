#!/usr/bin/env python3
"""Quarantine contacts whose email address is masked or redacted.

Scraped sources sometimes yield an obscured address rather than a real one --
`m***@bayut.com` from a directory that hides the local part behind a paywall, or
`***REMOVED***` left behind by a sanitiser. Neither can be sent to, so they sit
in the send pool inflating counts and failing at send time.

This moves those rows out of the source sheets into
`industry/masked_contacts.csv`, tagged with the file they came from. They are
quarantined rather than deleted: each keeps its company, name, title and
LinkedIn URL, so the address can be resolved later (most carry an Action note
naming the tool to use) and the row promoted back into its source sheet.

Only rows whose *only* email is masked are moved. `industry/emails.csv` is left
alone on purpose: its two masked values sit in the secondary `HR Person Direct
Email` column while `General Contact Email` still holds a deliverable address,
so those companies remain contactable and dropping the rows would lose them.

Rows are removed by physical line, not by rewriting the CSV, because
`hr_contacts.csv` contains a field with an unquoted `"` that a rewrite would
re-quote -- churning a line that has nothing to do with this change.

Usage:
    python scripts/split_masked.py [--dry-run]
"""

import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INDUSTRY = os.path.join(ROOT, "industry")

# dataniti_contacts.csv is the upstream sheet that feeds extra_contacts.csv, so
# it is scanned too -- quarantining only the downstream copy would let the next
# import walk the masked row straight back in.
SOURCES = ["hr_contacts.csv", "extra_contacts.csv", "dataniti_contacts.csv"]
QUARANTINE = os.path.join(INDUSTRY, "masked_contacts.csv")
FIELDS = ["Company", "Name", "Title", "Email", "LinkedIn", "Action"]

# These sheets do not share one schema: hr_contacts/extra_contacts carry
# LinkedIn + Action, dataniti_contacts carries neither and records provenance in
# Source instead. Fold whichever free-text column exists into Action so the
# quarantine sheet stays one shape and no provenance is dropped.
NOTE_COLUMNS = ["Action", "Source", "Notes"]


def is_masked(email):
    return "*" in (email or "")


def scan(path):
    """Yield (record, first_line, last_line) for masked rows, 1-indexed.

    csv.reader.line_num tracks the last physical line consumed, which lets a
    record that wraps across lines map back to the exact span to delete.
    """
    found = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        email_at = header.index("Email")
        prev = reader.line_num
        for record in reader:
            first, last = prev + 1, reader.line_num
            prev = reader.line_num
            if len(record) > email_at and is_masked(record[email_at]):
                found.append((record, header, first, last))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would move without writing any file")
    args = ap.parse_args()

    moved = []
    removals = {}

    for name in SOURCES:
        path = os.path.join(INDUSTRY, name)
        hits = scan(path)
        if not hits:
            print(f"{name}: no masked emails")
            continue
        drop = set()
        for record, header, first, last in hits:
            row = dict(zip(header, record))
            entry = {"SourceFile": name, **{k: row.get(k, "") for k in FIELDS}}
            if not entry["Action"]:
                entry["Action"] = next(
                    (row[c] for c in NOTE_COLUMNS if row.get(c)), "")
            moved.append(entry)
            drop.update(range(first, last + 1))
            print(f"{name}:{first}: {row.get('Company','')} / "
                  f"{row.get('Name','')} -- {row.get('Email','')}")
        removals[path] = drop

    if not moved:
        print("nothing to quarantine")
        return 0

    print(f"\n{len(moved)} rows -> industry/masked_contacts.csv")

    if args.dry_run:
        print("dry run: no files written")
        return 0

    # Append to the quarantine sheet, creating it with a header if new.
    exists = os.path.exists(QUARANTINE)
    with open(QUARANTINE, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["SourceFile"] + FIELDS,
                                lineterminator="\n")
        if not exists:
            writer.writeheader()
        writer.writerows(moved)
    print(f"wrote {QUARANTINE}")

    # Drop the quarantined rows from each source, preserving every other byte.
    for path, drop in removals.items():
        with open(path, encoding="utf-8", newline="") as f:
            lines = f.readlines()
        kept = [ln for i, ln in enumerate(lines, 1) if i not in drop]
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.writelines(kept)
        print(f"removed {len(lines) - len(kept)} line(s) from {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
