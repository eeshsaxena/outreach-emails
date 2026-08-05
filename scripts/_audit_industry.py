#!/usr/bin/env python3
"""Quick audit of industry data quality."""
import csv, os, re

HERE  = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(HERE)
IND   = os.path.join(ROOT, "industry")

valid_re = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]{2,}$')

def audit(filename):
    fp = os.path.join(IND, filename)
    if not os.path.exists(fp):
        print(f"{filename}: NOT FOUND"); return
    with open(fp, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print(f"{filename}: EMPTY"); return

    # detect email column
    email_col = next((k for k in rows[0] if "email" in k.lower()), None)
    if not email_col:
        print(f"{filename}: no email column"); return

    emails = [r.get(email_col,"").strip() for r in rows]
    no_email   = sum(1 for e in emails if not e)
    invalid    = [e for e in emails if e and not valid_re.match(e)]
    junk       = [e for e in emails if any(p in e.lower() for p in ["(","*","example.com","noreply","no-reply"])]

    dash_company = sum(1 for r in rows if r.get("Company","").strip() in ("—","-","–",""))

    print(f"\n{filename}  ({len(rows)} rows)")
    print(f"  no email       : {no_email}")
    print(f"  invalid email  : {len(invalid)}")
    print(f"  junk email     : {len(junk)}")
    print(f"  blank company  : {dash_company}")
    if invalid:
        print("  invalid samples:")
        for e in invalid[:5]:
            print(f"    {e!r}")

audit("emails.csv")
audit("hr_contacts.csv")
audit("extra_contacts.csv")

# industry batches summary
batch_dir = os.path.join(IND, "batches")
batches = sorted(f for f in os.listdir(batch_dir) if f.endswith(".csv"))
total_rows = 0
seen = set()
for fn in batches:
    with open(os.path.join(batch_dir, fn), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            e = r.get("Email","").strip().lower()
            if e:
                seen.add(e)
                total_rows += 1
print(f"\nIndustry batches: {len(batches)} files, {total_rows} rows, {len(seen)} unique emails")

# coverage check — emails in extra_contacts not in batches
fp_extra = os.path.join(IND, "extra_contacts.csv")
with open(fp_extra, encoding="utf-8", newline="") as f:
    extra_rows = list(csv.DictReader(f))
extra_emails = {r.get("Email","").strip().lower() for r in extra_rows if r.get("Email","").strip()}
not_batched = extra_emails - seen
print(f"extra_contacts emails NOT in any batch: {len(not_batched)}")
