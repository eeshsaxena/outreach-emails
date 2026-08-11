# Internship Outreach

[![ci](https://github.com/eeshsaxena/outreach-emails/actions/workflows/ci.yml/badge.svg)](https://github.com/eeshsaxena/outreach-emails/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A database and toolkit for cold-outreach internship hunting, split into two tracks:

- **`industry/`** : paid-internship outreach to companies (HR / recruiter contacts) plus a scheduled career-page watcher that alerts on new entry-level postings.
- **`research/`** : research-internship outreach to faculty at IITs, NITs, and IIITs, organized by institute type, then state, then city.

Shared **`templates/`** hold the email copy, **`scripts/`** hold all automation, and **`state/`** holds the career-watcher's saved state.

> **Contains personal data.** The CSVs hold scraped company emails, named HR/recruiter contacts, faculty emails, and LinkedIn profiles. Use the data responsibly, keep it accurate, and follow anti-spam / consent norms when contacting anyone.

---

## Repository layout

```
outreach-emails/
├── README.md                       # this file
├── requirements.txt
│
├── industry/                       # TRACK 1 : company / HR outreach
│   ├── emails.csv                  # ~400 companies (source)
│   ├── hr_contacts.csv             # ~1,300 named HR contacts (source)
│   ├── extra_contacts.csv          # externally imported contacts (source)
│   ├── career_pages.csv            # pages the watcher monitors
│   ├── all_emails.csv              # merged reference pool
│   ├── dead_removed.csv            # pruned / bounced contacts
│   ├── masked_contacts.csv         # quarantined: email masked/redacted, not sendable
│   ├── *_companies.csv             # per-city company source sheets
│   ├── location_sheets/            # regional reference data
│   ├── batches/                    # GENERATED: batch_NN.csv (100 contacts each)
│   ├── city/                       # GENERATED: city_<city>_NN.csv (per-city sends)
│   └── unsorted/                   # GENERATED: unsorted_NN.csv (no city detected)
│
├── research/                       # TRACK 2 : faculty / research outreach
│   ├── README.md                   # research-track details + schema
│   ├── faculty_master.csv          # single source of truth (merged + deduped)
│   ├── dead_removed.csv
│   ├── batches/                    # GENERATED: research_batch_NN.csv
│   └── faculty/
│       ├── iits/   <state>/<city>/<institute>.csv
│       ├── nits/   <state>/<city>/<institute>.csv
│       └── iiits/  <state>/<city>/<institute>.csv
│
├── templates/                      # email copy for both tracks
│   ├── research_cold.md
│   ├── follow_up_1.md
│   └── follow_up_2.md
│
├── scripts/                        # all Python automation
│   ├── gen_batches.py              # industry -> industry/batches/
│   ├── gen_city_batches.py         # industry -> industry/city/ + industry/unsorted/
│   ├── gen_csv.py                  # rebuild emails.csv + hr_contacts.csv
│   ├── import_external.py          # import external sheets -> extra_contacts.csv
│   ├── make_sheet.py               # build the Excel workbook
│   ├── career_watch.py             # career-page watcher
│   └── add_*.py                    # one-off contributor batch appenders
│
├── state/                          # career-watcher state (do not hand-edit)
│   ├── career_state.json
│   ├── career_alerts.md
│   └── career_alerts.log
│
└── .github/workflows/career-watch.yml   # runs scripts/career_watch.py twice a day
```

**Why two tracks?** The data shape and the pitch differ. Industry outreach targets *companies* by hiring need (HR contacts). Research outreach targets *professors* by research area. Keeping them separate means each has its own schema, templates, and batch pipeline without cross-contaminating the other.

**How the scripts find their data.** Every script in `scripts/` resolves paths relative to its own location, not the current working directory, so you can run them from anywhere:

```bash
python scripts/gen_batches.py
python scripts/career_watch.py
```

They read from `industry/` and write generated output into `industry/batches/`, `industry/city/`, and `industry/unsorted/`. The career watcher reads `industry/career_pages.csv` and writes its state to `state/`.

---

## Track 1: industry (company / HR)

### Stats
- **~400** companies (Dubai/UAE, Gandhinagar/GIFT City, and pan-India)
- **~1,300** named HR contacts with direct emails
- **~130** high-priority targets
- **~25** verified direct HR/careers/recruitment inboxes

### Source data

| File | Rows | Schema |
|------|------|--------|
| `industry/emails.csv` | ~400 companies | `#, Company, Website, Category, General Contact Email, Email Type, HR Person Name, HR Person Title, HR Person Direct Email, LinkedIn Profile, Priority, Notes` |
| `industry/hr_contacts.csv` | ~1,300 | `Company, Name, Title, Email, LinkedIn, Action` |
| `industry/extra_contacts.csv` | ~12,900 | same schema as `hr_contacts.csv` (externally imported) |
| `industry/career_pages.csv` | ~1,000 | `Company, URL, Location, EntryLevel, Notes` |

**Categories:** Fintech, PropTech, HealthTech, EdTech, AI/ML, SaaS, Web Dev, App Dev, FoodTech, Logistics, Payments, Cybersecurity, Digital Marketing, IoT, Embedded, ERP, SAP.

**Regions covered:** Dubai/UAE, GIFT City / Gandhinagar / Infocity, and Indian metros (Bengaluru, Delhi NCR, Hyderabad, Pune, Chennai, Mumbai, Lucknow, and more via `industry/location_sheets/`).

### The pipeline

```
external sheets ──import_external.py──┐
pasted lists ────add_*.py────────────┤──► industry/extra_contacts.csv
                                      │
industry/emails.csv + hr_contacts.csv + extra_contacts.csv
                                      │
              ┌───────────────────────┼───────────────────────┐
       gen_batches.py          gen_city_batches.py        make_sheet.py
              │                        │                        │
     industry/batches/         industry/city/ +          Excel workbook
      batch_NN.csv             industry/unsorted/         (4 sheets)
```

| Script | What it does |
|--------|--------------|
| `gen_csv.py` | Rebuilds `industry/emails.csv` + `industry/hr_contacts.csv` from data embedded in `make_sheet.py`. |
| `import_external.py` | Imports external contact files into `industry/extra_contacts.csv`, deduping against existing rows. |
| `add_*.py` | One-off appenders for hand-pasted / per-city contributor lists. |
| `gen_batches.py` | Splits the merged pool into `industry/batches/batch_NN.csv` of 100 each. |
| `gen_city_batches.py` | Same pool split per city into `industry/city/`, with location-less rows in `industry/unsorted/`. |
| `make_sheet.py` | Builds the Excel workbook (All Companies, Priority, Named HR Contacts, Email Template). |
| `career_watch.py` | Career-page watcher (see below). |
| `split_masked.py` | Moves contacts whose email is masked/redacted into `industry/masked_contacts.csv`. |
| `dedupe_faculty.py` | Merges same-person-same-institute duplicates in `research/faculty_master.csv`. |

### Career-page alert system

Monitors company career pages and alerts when new postings appear, focusing on entry-level / fresher roles.

- `industry/career_pages.csv` : pages to watch (`Company, URL, Location, EntryLevel, Notes`).
- `scripts/career_watch.py` : fetches each page, extracts job-like entries, diffs against `state/career_state.json`, and writes new entries to `state/career_alerts.md` (consumed by the Action) and `state/career_alerts.log`.
- `.github/workflows/career-watch.yml` : runs twice a day, opens a GitHub issue on new entries, and commits the updated state.

```bash
python scripts/career_watch.py          # first run seeds state silently
```

**Entry-level focus:** postings that look like fresher/graduate/trainee/intern/0-1 yr are flagged. Rows with `EntryLevel=yes` only alert on entry-level postings.

**Rendering JS (SPA / MNC portals):** static fetch cannot read SPA portals (Infosys joblist, TCS iBegin, etc.). The Action installs Playwright and runs with `RENDER=1`. Locally:

```bash
pip install playwright && playwright install chromium
RENDER=1 python scripts/career_watch.py
```

**Optional email alerts:** set repo secrets `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `ALERT_TO`.

---

## Track 2: research (faculty)

Cold-outreach to faculty at IITs, NITs, and IIITs for research internships. Full details and the CSV schema live in [`research/README.md`](research/README.md).

### Layout: institute type, then state, then city

```
research/faculty/
├── iits/   <state>/<city>/<institute>.csv
├── nits/   <state>/<city>/<institute>.csv
└── iiits/  <state>/<city>/<institute>.csv
```

Example: `research/faculty/iits/maharashtra/mumbai/iit-bombay.csv`

### CSV schema (identical in every faculty file)

```
name,state,city,institute,institute_type,department,email,research_area,personal_site,priority,status,notes
```

- `institute_type` : `IIT` | `NIT` | `IIIT`
- `status` : `queued / sent / follow-up-1 / replied / accepted / rejected / no-response`

`state`, `city`, and `institute_type` are columns as well as folders, so `faculty_master.csv` stays the single source that a batch generator reads from, and the folders are just a convenient view.

---

## Setup

```bash
pip install -r requirements.txt
```

Generate the sendable industry batches / spreadsheet:

```bash
python scripts/gen_batches.py        # -> industry/batches/batch_001.csv, ...
python scripts/gen_city_batches.py   # -> industry/city/city_bengaluru_01.csv, ...
python scripts/make_sheet.py         # -> Excel workbook
```

---

## Sending email (mailer)

`mailer/` is a small CSV-to-email sender for the outreach itself. It renders a
template once per recipient and sends over SMTP. **Dry run is the default**, so
nothing is sent unless you pass `--send`. Full details in [`mailer/GUIDE.md`](mailer/GUIDE.md).

### One-time setup

1. Credentials (for real sends). Copy the env template and fill it in:
   ```bash
   cp mailer/.env.example mailer/.env
   ```
   For Gmail, `SMTP_PASS` is an **App Password** (16 chars), not your account
   password. `.env` is gitignored and must never be committed.
2. Put your resume at `mailer/resume.pdf` (gitignored) so it gets attached, then
   set `from_name`, `reply_to`, and `template_vars` in `mailer/settings.json`,
   and edit `mailer/templates/*.txt` to your own words.

### Send

```bash
# preview what would go out (sends nothing):
python mailer/send.py --file industry/batches/batch_001.csv

# actually send, capped, resume attached:
python mailer/send.py --file industry/batches/batch_001.csv --limit 50 --send

# follow-up template:
python mailer/send.py --file industry/batches/batch_001.csv --template followup --send
```

Every send is logged to `mailer/sent_log.csv` (gitignored); addresses already in
it are skipped, so re-running a batch never double-sends.

### Run it from GitHub Actions (optional)

[`.github/workflows/mailer.yml`](.github/workflows/mailer.yml) lets you trigger a
send from the **Actions** tab (`workflow_dispatch`), so you don't need your
laptop. It is **manual only and dry-run by default** (no cron, to avoid
accidental sends).

Add these repository secrets (**Settings -> Secrets and variables -> Actions**):

| Secret | What |
|---|---|
| `SMTP_USER` | the sending address |
| `SMTP_PASS` | the Gmail App Password |
| `RESUME_PDF_BASE64` | your resume, base64-encoded, so it stays out of git |

Encode the resume once:

```bash
base64 -w0 resume.pdf        # paste the output into the RESUME_PDF_BASE64 secret
```

Then **Run workflow** with inputs: `file` (e.g. `industry/batches/batch_001.csv`),
`template`, `limit`, and `dry_run` (leave `true` to preview, set `false` to
send). The dedup log is per-run on Actions (it is not committed back, to keep
recipient addresses out of the repo), so send each batch in a single run.

---

## Best practices

- Personalize every outreach email for higher response rates.
- Verify contact information before sending.
- Avoid bulk / spam sends; respect unsubscribe requests and anti-spam rules.

---

## Notes

- `industry/batches/`, `industry/city/`, `industry/unsorted/`, and the `.xlsx` are generated. Recreate them any time from the source CSVs with the commands above.
- `industry/dead_removed.csv` and `research/dead_removed.csv` track contacts pruned as dead/bounced.
- `industry/masked_contacts.csv` holds contacts whose address came through masked (`m***@bayut.com`) or redacted (`***REMOVED***`). They are quarantined rather than deleted: each keeps its company, name, title and LinkedIn URL, so once the real address is resolved the row can be promoted back into its source sheet. Run `python scripts/split_masked.py` after any import to keep them out of the send pool.
- Scripts resolve their own paths, so they work regardless of the directory you run them from.