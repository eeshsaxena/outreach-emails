import csv
import os
import re

# Splits the same contact pool as gen_batches.py into CITY-WISE batches instead of
# one flat numbered sequence, so a send can be targeted at one city at a time.
# Output: city_<city>_<NN>.csv  (a city with more than BATCH_SIZE contacts rolls
# over into _02, _03, ...). Contacts with no detectable city go to city_other_NN.csv.

BATCH_SIZE = 100

# Order matters: first match wins, so put more specific markers before broader ones.
CITY_RULES = [
    (
        "Bengaluru",
        (
            "bengaluru",
            "bangalore",
            "bellandur",
            "koramangala",
            "hsr layout",
            "indiranagar",
            "whitefield",
            "electronic city",
        ),
    ),
    ("Gandhinagar", ("gandhinagar", "gift city", "kudasan", "infocity", "sargasan")),
    ("Ahmedabad", ("ahmedabad", "motera", "prahlad nagar", "bodakdev", "satellite")),
    ("Rajkot", ("rajkot",)),
    ("Surat", ("surat",)),
    ("Vadodara", ("vadodara", "baroda")),
    ("Navi Mumbai", ("navi mumbai",)),
    ("Mumbai", ("mumbai", "andheri", "bkc", "powai")),
    ("Pune", ("pune", "pimpri", "chinchwad", "hinjewadi", "kharadi", "baner")),
    ("Nashik", ("nashik",)),
    ("Nagpur", ("nagpur",)),
    ("Noida", ("noida", "greater noida")),
    ("Ghaziabad", ("ghaziabad",)),
    ("Gurugram", ("gurugram", "gurgaon")),
    ("Delhi", ("new delhi", "delhi", "ncr")),
    ("Meerut", ("meerut",)),
    ("Agra", ("agra",)),
    ("Varanasi", ("varanasi", "banaras")),
    ("Kanpur", ("kanpur",)),
    ("Lucknow", ("lucknow", "vibhuti khand", "gomti nagar")),
    ("Prayagraj", ("prayagraj", "allahabad")),
    ("Gorakhpur", ("gorakhpur",)),
    ("Deoria", ("deoria",)),
    ("Indore", ("indore",)),
    ("Bhopal", ("bhopal",)),
    ("Gwalior", ("gwalior",)),
    ("Jabalpur", ("jabalpur",)),
    ("Ujjain", ("ujjain",)),
    ("Kota", ("kota",)),
    ("Jaipur", ("jaipur",)),
    ("Hyderabad", ("hyderabad", "secunderabad", "gachibowli", "hitec city")),
    ("Tirupati", ("tirupati",)),
    ("Visakhapatnam", ("visakhapatnam", "vizag")),
    ("Vijayawada", ("vijayawada",)),
    ("Chennai", ("chennai", "madras", "omr")),
    ("Coimbatore", ("coimbatore",)),
    ("Madurai", ("madurai",)),
    ("Mysuru", ("mysuru", "mysore")),
    ("Kochi", ("kochi", "cochin", "ernakulam", "infopark")),
    ("Thiruvananthapuram", ("thiruvananthapuram", "trivandrum", "technopark")),
    ("Thrissur", ("thrissur",)),
    ("Kolkata", ("kolkata", "calcutta", "salt lake")),
    ("Bhubaneswar", ("bhubaneswar",)),
    ("Dehradun", ("dehradun",)),
    ("Mohali", ("mohali", "chandigarh")),
    ("Ludhiana", ("ludhiana",)),
    ("Aurangabad", ("aurangabad", "chhatrapati sambhajinagar", "sambhajinagar")),
    ("Dubai/UAE", ("dubai", "uae", "sharjah", "abu dhabi")),
    ("Singapore", ("singapore",)),
]


def city_of(*texts):
    blob = " ".join(t or "" for t in texts).lower()
    for city, markers in CITY_RULES:
        for m in markers:
            if re.search(r"\b" + re.escape(m) + r"\b", blob):
                return city
    return "Other"


def slug(city):
    return re.sub(r"[^a-z0-9]+", "_", city.lower()).strip("_")


seen = set()
rows = []

with open("emails.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        direct = r["HR Person Direct Email"].strip()
        general = r["General Contact Email"].strip()
        email = (
            direct
            if "@" in direct and "(" not in direct and "*" not in direct
            else general
        )
        email = email.strip()
        if "@" not in email:
            continue
        key = email.lower()
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            {
                "#": r["#"],
                "Company": r["Company"],
                "Email": email,
                "Person": r["HR Person Name"] or "Hiring Team",
                "Title": r["HR Person Title"] or "-",
                "City": city_of(r["Notes"], r["Company"]),
                "Notes": r["Notes"][:120],
            }
        )

contact_files = ["hr_contacts.csv"]
if os.path.exists("extra_contacts.csv"):
    contact_files.append("extra_contacts.csv")
for cf in contact_files:
    with open(cf, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            email = r["Email"].strip()
            if "@" not in email or "(" in email or "*" in email or " " in email:
                continue
            key = email.lower()
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                {
                    "#": "",
                    "Company": r["Company"],
                    "Email": email,
                    "Person": r["Name"],
                    "Title": r["Title"],
                    "City": city_of(r["Action"], r["Company"]),
                    "Notes": r["Action"][:120],
                }
            )

for old in os.listdir("."):
    if re.match(r"(city_.+|unsorted)_\d+\.csv$", old):
        os.remove(old)

by_city = {}
for r in rows:
    by_city.setdefault(r["City"], []).append(r)

fields = ["#", "Company", "Email", "Person", "Title", "City", "Notes"]
total = 0
files = 0
for city in sorted(by_city, key=lambda c: (-len(by_city[c]), c)):
    group = by_city[city]
    # "Other" is not a city - these rows never had a location recorded, so label
    # the files unsorted_* rather than implying a place.
    prefix = "unsorted" if city == "Other" else f"city_{slug(city)}"
    for i in range(0, len(group), BATCH_SIZE):
        part = group[i : i + BATCH_SIZE]
        name = f"{prefix}_{i // BATCH_SIZE + 1:02d}.csv"
        with open(name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(part)
        total += len(part)
        files += 1
    print(
        f"{city:22} {len(group):5} emails -> {(len(group) + BATCH_SIZE - 1) // BATCH_SIZE} file(s)"
    )

print(f"TOTAL: {total} unique emails across {files} city files / {len(by_city)} cities")
