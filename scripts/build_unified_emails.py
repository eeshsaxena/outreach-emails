#!/usr/bin/env python3
"""Build the root-level unified email list from every industry (non-research)
CSV.

Scans ``industry/**/*.csv``, pulls out (Company, Email, Person, Title,
Location, Notes) from whatever column shape each sheet uses, de-duplicates by
email address, and writes ``unified_emails.csv`` at the repo root.

Research faculty emails are deliberately excluded (only ``industry/`` is
scanned). Run from anywhere:  ``python scripts/build_unified_emails.py``.
The career-watch workflow regenerates this file automatically on every push
that changes an industry sheet.
"""
import csv
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDUSTRY = os.path.join(ROOT, "industry")
OUT = os.path.join(ROOT, "unified_emails.csv")

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
OUT_COLS = ["Company", "Email", "Person", "Title", "Location", "Source", "Notes"]


def pick(header, *wants):
    """Return the first header cell that matches one of the wanted keywords."""
    low = {h.lower(): h for h in header}
    # exact match first
    for w in wants:
        if w in low:
            return low[w]
    # then substring match
    for h in header:
        hl = h.lower()
        if any(w in hl for w in wants):
            return h
    return None


def main():
    rows = {}          # email(lower) -> row dict
    files = 0
    for path in sorted(glob.glob(os.path.join(INDUSTRY, "**", "*.csv"),
                                 recursive=True)):
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        try:
            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                header = reader.fieldnames or []
                ecol = pick(header, "email")           # Email / Best Email / General Contact Email
                if not ecol:
                    continue
                ccol = pick(header, "company", "name")
                pcol = pick(header, "person", "contact person", "hr person name")
                tcol = pick(header, "title", "role")
                lcol = pick(header, "city", "region", "location")
                ncol = pick(header, "notes")
                files += 1
                for r in reader:
                    email = (r.get(ecol) or "").strip()
                    if not email or not EMAIL_RE.match(email):
                        continue
                    key = email.lower()
                    if key in rows:
                        continue                       # first sheet wins
                    rows[key] = {
                        "Company": (r.get(ccol) or "").strip() if ccol else "",
                        "Email": email,
                        "Person": (r.get(pcol) or "").strip() if pcol else "",
                        "Title": (r.get(tcol) or "").strip() if tcol else "",
                        "Location": (r.get(lcol) or "").strip() if lcol else "",
                        "Source": rel,
                        "Notes": (r.get(ncol) or "").strip() if ncol else "",
                    }
        except Exception as e:  # noqa: BLE001 - one bad sheet must not stop the build
            print(f"  ! skipped {rel}: {e}", file=sys.stderr)

    out = sorted(rows.values(), key=lambda r: (r["Company"].lower(), r["Email"]))
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=OUT_COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print(f"unified_emails.csv: {len(out)} unique emails from {files} industry sheets")


if __name__ == "__main__":
    main()
