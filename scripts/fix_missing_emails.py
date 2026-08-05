#!/usr/bin/env python3
"""
fix_missing_emails.py — Fill in the 11 missing emails in emails.csv,
then rebuild industry batches.
"""
import csv, os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IND  = os.path.join(ROOT, "industry")

FILLS = {
    "Odoo India":           "jobs@odoo.com",
    "AgroStar":             "careers@agrostar.in",
    "Accenture GIFT City":  "india.careers@accenture.com",
    "Zoho GIFT City":       "careers@zohocorp.com",
    "Razorpay GIFT City":   "careers@razorpay.com",
    "LTIMindtree GIFT City":"careers@ltimindtree.com",
    "Zensar Technologies":  "careers@zensar.com",
    "DevX":                 "hello@devx.work",
    "Cognizant GIFT City":  "india.recruiter@cognizant.com",
    "Hexaware GIFT City":   "careers@hexaware.com",
    "Realcode Infotech":    "hr@realcodeinfotech.com",
}

fp = os.path.join(IND, "emails.csv")
with open(fp, encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
    hdr  = list(rows[0].keys()) if rows else []

filled = 0
for r in rows:
    comp = r.get("Company", "").strip()
    if comp in FILLS:
        # Only fill if currently missing
        gen = r.get("General Contact Email", "").strip()
        if gen in ("—", "–", "-", ""):
            r["General Contact Email"] = FILLS[comp]
            r["Email Type"] = "Careers"
            filled += 1

with open(fp, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=hdr)
    w.writeheader()
    w.writerows(rows)

print(f"emails.csv: filled {filled} missing emails")

# Rebuild batches
print("\nRebuilding industry batches...")
gen = os.path.join(HERE, "gen_batches.py")
result = subprocess.run([sys.executable, gen], capture_output=True, text=True)
lines = result.stdout.strip().splitlines()
for line in lines[-2:]:
    print(line)
