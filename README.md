# Internship Outreach - Email Database
Public repository containing scraped company emails and HR contacts for paid internship outreach.
Designed to streamline internship outreach by combining verified contact data with automated career-page monitoring for faster application opportunities.
## Files

- `emails.csv` - 198 companies with general contact emails, categories, priority levels
- `hr_contacts.csv` - 53 named HR/TA/founder contacts with direct emails and LinkedIn profiles
- `make_sheet.py` - Python script to generate formatted Excel spreadsheet

## Stats

- **402** companies (Dubai/UAE, Gandhinagar/GIFT City, and pan-India)
- **1,305** named HR contacts with direct emails
- **~130** High-priority targets
- **~25** verified direct HR/careers/recruitment inboxes

## Regions

- **Rounds 1-3**: Dubai/UAE tech companies (#1-143)
- **Rounds 4-8**: GIFT City, Infocity, Kudasan, Sargasan, Gandhinagar (#144-191)
- **Round 9**: PDPU corridor, Infocity expansion, Arrow/eInfochips (#192-198)
- **Round 10+**: pan-India expansion — Bengaluru, Hyderabad, Pune, Jaipur, Lucknow, Kota, Deoria, and other cities (see `city_*.csv` batches)

## Categories

Fintech, PropTech, HealthTech, EdTech, AI/ML, SaaS, Web Dev, App Dev, FoodTech, Logistics, Payments, Cybersecurity, Digital Marketing, IoT, Embedded, ERP, SAP

## Usage

```bash
pip install openpyxl
python make_sheet.py
```

Generates `Dubai_Internship_Outreach.xlsx` with 4 sheets:
1. All Companies
2. Priority Dubai Companies (High only)
3. Named HR Contacts
4. Email Template

## Career-page alert system

Monitors company career pages and alerts when **new postings** appear.

- `career_pages.csv` - pages to watch (`Company, URL, Notes`)
- `career_watch.py` - fetches each page, extracts job-like entries, diffs vs `career_state.json`, writes new entries to `career_alerts.md` / `career_alerts.log`
- `.github/workflows/career-watch.yml` - runs every 12h, opens a GitHub **issue** on new entries, commits updated state

```bash
pip install requests playwright && playwright install chromium
python career_watch.py          # first run seeds state silently
```

Optional email alerts: set repo secrets `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `ALERT_TO`.

**Coverage** - `career_pages.csv` columns: `Company, URL, Location, EntryLevel, Notes`
- GIFT City / Gandhinagar SMEs (DRC, Infibeam/AvenuesAI, Silver Touch, Dev IT, eInfochips, TIS…)
- Well-established MNCs across multiple locations: **Infosys, Accenture, Capgemini, IBM, TCS, Cognizant, Wipro, HCLTech** (Bengaluru, Hyderabad, Pune, Gurugram, Chandigarh, India-wide).

**Entry-level (0 experience) focus**
- Postings that look like fresher/graduate/trainee/intern/entry-level/0–1 yr are flagged with 🎓.
- Rows with `EntryLevel=yes` only alert on entry-level postings (all MNC rows are set this way).

**Rendering JS (SPA / MNC portals)**
- Default static fetch can't read SPA portals (Infosys joblist, TCS iBegin, etc.).
- The GitHub Action installs Playwright and runs with `RENDER=1` so JS pages render.
- Locally: `pip install playwright && playwright install chromium`, then `RENDER=1 python career_watch.py`.

**Known limits**
- Heuristic role-keyword matching; per-page state means stable noise won't re-alert.
- Some portals bot-block (HTTP 403) even with rendering; swap to their public job-search API or an aggregator URL if so.
- Add/maintain URLs in `career_pages.csv`.
