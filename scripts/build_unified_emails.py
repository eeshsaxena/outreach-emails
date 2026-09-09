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
# Two root-level views of the same de-duplicated list: A->Z by company, and the
# same rows reversed (Z->A / bottom-to-top). Both are regenerated together.
OUT = os.path.join(ROOT, "unified_emails.csv")
OUT_REV = os.path.join(ROOT, "unified_emails_z_to_a.csv")

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

    # Stable ordering: keep the order each list already has and only append the
    # newly-seen emails at the END (so recent additions are easy to find at the
    # bottom), rather than re-sorting the whole list on every rebuild.
    #  - unified_emails.csv         seeds A->Z the first time it is created.
    #  - unified_emails_z_to_a.csv  seeds Z->A the first time it is created.
    # After that each file keeps its own order and new emails land at the end.
    by_email = {k: v for k, v in rows.items()}  # email(lower) -> row
    az_sorted = [
        r["Email"].lower()
        for r in sorted(by_email.values(), key=lambda r: (r["Company"].lower(), r["Email"]))
    ]

    def existing_order(path):
        if not os.path.exists(path):
            return None
        try:
            with open(path, encoding="utf-8") as f:
                ecol = pick(next(csv.reader(f)), "email") or "Email"
            with open(path, encoding="utf-8") as f:
                return [(r.get(ecol) or "").strip().lower() for r in csv.DictReader(f)]
        except Exception:  # noqa: BLE001
            return None

    def assemble(seed_order):
        # keep the established order (dropping emails no longer present), then
        # append any email not already listed, in A->Z order for determinism.
        body = [e for e in seed_order if e in by_email]
        placed = set(body)
        tail = [e for e in az_sorted if e not in placed]
        return [by_email[e] for e in body + tail]

    az_existing = existing_order(OUT)
    az_seed = az_existing if az_existing is not None else az_sorted
    rev_existing = existing_order(OUT_REV)
    if rev_existing is not None:
        rev_seed = rev_existing
    elif az_existing is not None:
        # First creation of the reverse file: seed from the OLD A->Z body
        # reversed (not from the current full set), so this run's new emails
        # are appended at the end here too, not sorted into Z->A positions.
        rev_seed = list(reversed(az_existing))
    else:
        rev_seed = list(reversed(az_sorted))

    for path, ordered in ((OUT, assemble(az_seed)), (OUT_REV, assemble(rev_seed))):
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            w = csv.DictWriter(f, fieldnames=OUT_COLS, lineterminator="\n")
            w.writeheader()
            w.writerows(ordered)
    print(
        f"unified_emails.csv (A->Z, new appended) + unified_emails_z_to_a.csv "
        f"(Z->A, new appended): {len(by_email)} unique emails from {files} sheets"
    )


if __name__ == "__main__":
    main()
