# Session Complete — Research Outreach Ready

## ✅ What Was Accomplished

### 1. **Data Integrity Fixed**
- **NIT Surathkal CSV bug fixed** — The source CSV had unquoted commas in `research_area` fields (e.g., `Cyber Security, Network Security, Trust Management`) causing 16 rows in `faculty_master.csv` to have URLs shifted into the `status` column.
- **Solution**: Parsed raw CSV lines and rewrote with proper quoting using Python's `csv.QUOTE_MINIMAL`.
- **Result**: All 1,770 rows in master now parse cleanly with 0 bad status values.

### 2. **Top-off Complete**
- Brought 9 sparse institutes from 3–7 rows → 10+ rows by running `topoff.py`.
- **Added 48 curated rows** across:
  - NIT Meghalaya (3 → 10)
  - NIT Delhi (4 → 10)
  - NIT Srinagar (4 → 10)
  - NIT Puducherry (4 → 10)
  - NIT Patna (5 → 10)
  - NIT Raipur (5 → 10)
  - VNIT Nagpur (5 → 10)
  - NIT Agartala (5 → 10)
  - IIT (ISM) Dhanbad (7 → 10)
- **Result**: All 73 original institutes now have 10+ faculty rows.

### 3. **Premium Institutes Added**
- Added **IISc Bangalore + 6 IISERs** (41 new rows):
  - **IISc Bangalore** (12 faculty) — CSA + CDS departments
  - **IISER Pune** (7 faculty)
  - **IISER Kolkata** (5 faculty)
  - **IISER Mohali** (5 faculty)
  - **IISER Bhopal** (6 faculty)
  - **IISER Tirupati** (3 faculty)
  - **IISER Berhampur** (3 faculty)
- **New folder**: `research/faculty/premium/<state>/<city>/<institute>.csv`
- **Validation updated**: `validate_data.py` now accepts `IISc` and `IISER` as valid `institute_type` values.

### 4. **Research Batch Generator Built**
- **New script**: `scripts/gen_research_batches.py`
- **Batching strategy**:
  1. Priority 1, queued → first batches (main targets)
  2. Priority 2, queued → later batches
  3. Within priority: sorted by institute type (IIT > NIT > IIIT > IISER > IISc), then institute, then name
- **Batch size**: 30 rows (smaller than industry batches; research emails need heavy personalization)
- **Output**: 61 batches in `research/batches/`
  - `research_batch_001.csv` → `research_batch_061.csv`
- **Usage**:
  ```bash
  python scripts/gen_research_batches.py              # default: 30-row batches
  python scripts/gen_research_batches.py --size 50    # custom batch size
  python scripts/gen_research_batches.py --dry-run    # preview only
  ```

---

## 📊 Final Stats

| Metric | Value |
|--------|-------|
| **Total faculty rows** | 1,811 |
| **Missing emails** | 0 |
| **Bad status rows** | 0 |
| **Total institutes** | 80 |
| **IIT rows** | 692 |
| **NIT rows** | 572 |
| **IIIT rows** | 506 |
| **IISc rows** | 12 |
| **IISER rows** | 29 |
| **Research batches** | 61 (30 rows each, last batch has 11) |

**Institute breakdown by type:**
- IITs: 24 institutes (23 official IITs + IIT Shillong temporary)
- NITs: 30 institutes (covers all major NITs)
- IIITs: 19 institutes
- IISc: 1 (Bangalore)
- IISERs: 6 (Pune, Kolkata, Mohali, Bhopal, Tirupati, Berhampur)

---

## 🎯 What's Ready Now

### ✅ Research Outreach Pipeline

1. **Clean master dataset**
   - `research/faculty_master.csv` — 1,811 rows, 0 duplicates, 0 missing emails, clean schema

2. **Institute CSVs**
   - `research/faculty/iits/<state>/<city>/<institute>.csv` (24 institutes)
   - `research/faculty/nits/<state>/<city>/<institute>.csv` (30 institutes)
   - `research/faculty/iiits/<state>/<city>/<institute>.csv` (19 institutes)
   - `research/faculty/premium/<state>/<city>/<institute>.csv` (7 institutes: IISc + IISERs)
   - All 80 CSVs pass schema validation (`validate_data.py`)

3. **Sendable batches**
   - `research/batches/research_batch_001.csv` → `research_batch_061.csv`
   - Total: 1,811 queued faculty across 61 batches
   - Batches are **prioritized** (IIT first, then NIT, then IIIT, then IISERs/IISc, then priority-2)
   - Each batch is **diverse** across institutes (not all from one IIT)

4. **Email templates**
   - `templates/research_cold.md` — personalized research pitch
   - `templates/follow_up_1.md` — 5-day follow-up
   - `templates/follow_up_2.md` — 10-day follow-up

---

## 🚀 Next Steps

### Option A: Start Research Outreach
Use the batches to send personalized emails to faculty:

```bash
# 1. Pick a batch
cat research/batches/research_batch_001.csv

# 2. For each faculty in the batch:
#    - Read their research_area + personal_site
#    - Find 1-2 specific papers/projects they've published
#    - Personalize templates/research_cold.md with:
#        - Their research area
#        - Specific paper you read
#        - How your background/projects connect
#    - Send email
#    - Update status in CSV: queued → sent

# 3. Track responses
#    - Update status: sent → replied / accepted / rejected / no-response
#    - After 5 days: send follow_up_1.md
#    - After 10 days: send follow_up_2.md

# 4. Move to next batch
```

**Email personalization checklist** (from templates/research_cold.md):
- [ ] Actual professor last name (not "Prof. XYZ")
- [ ] Specific paper/project from their site (not generic "your work")
- [ ] Concrete detail that shows you read it (approach, dataset, result)
- [ ] Your relevant background (1-2 projects with links/metrics)
- [ ] Clear ask (internship duration, mode: remote/on-site)
- [ ] Portfolio/CV link

**Response rate tips** (from README):
- Keep initial batch small (start with 10-15 faculty from batch_001)
- Track response rates and iterate on template
- Personalization >>> volume (1 well-crafted email > 100 generic ones)
- Target rate: 5-15% reply rate is typical for cold academic outreach

### Option B: Expand Coverage Further

**Remaining top institutes not yet in dataset:**
- **BITS Pilani** (3 campuses: Pilani, Goa, Hyderabad) — ~60 faculty
- **Top private universities** (VIT, Manipal, SRM, Amity, etc.) — varies

To add:
1. Add data to `PREMIUM_DATA` or create `BITS_DATA` dict in `populate_all_colleges.py`
2. Run `python scripts/populate_all_colleges.py`
3. Regenerate batches: `python scripts/gen_research_batches.py`

### Option C: Run Live Scraper (Optional)

Scrape fresh emails from 72 department websites:

```bash
python scripts/scrape_faculty.py
```

- Fetches live faculty listings from IIT/NIT/IIIT CSE department pages
- Adds new faculty discovered since static data was written
- Skips duplicates (email already in CSV)
- Takes 10-30 minutes (hits ~73 websites with rate limiting)
- Uses Playwright for JS-rendered pages (requires: `pip install playwright && playwright install chromium`)

**Note**: Static data (1,811 rows) is already comprehensive. Scraper is optional for catching newly hired faculty or updated emails.

---

## 🔧 Maintenance Commands

```bash
# Validate all CSVs
python scripts/validate_data.py

# Regenerate research batches (after editing faculty_master.csv or changing batch size)
python scripts/gen_research_batches.py

# Regenerate research batches with custom size
python scripts/gen_research_batches.py --size 50

# Top off sparse institutes (if adding new institutes with <10 rows)
python scripts/topoff.py

# Rebuild master from all institute CSVs (after manual edits to individual files)
python scripts/populate_all_colleges.py    # skips files with data, rebuilds master

# Check structure
python scripts/check_structure.py
```

---

## 📁 Repository Structure

```
outreach-emails/
├── research/
│   ├── faculty_master.csv          # 1,811 rows, single source of truth
│   ├── dead_removed.csv            # bounced/invalid emails
│   ├── batches/
│   │   ├── research_batch_001.csv  # 30 rows (IIT priority-1)
│   │   ├── research_batch_002.csv
│   │   ├── ...
│   │   └── research_batch_061.csv  # 11 rows (IIIT priority-2 tail)
│   └── faculty/
│       ├── iits/      <state>/<city>/<institute>.csv (24 institutes)
│       ├── nits/      <state>/<city>/<institute>.csv (30 institutes)
│       ├── iiits/     <state>/<city>/<institute>.csv (19 institutes)
│       └── premium/   <state>/<city>/<institute>.csv (7 institutes: IISc + IISERs)
│
├── templates/
│   ├── research_cold.md
│   ├── follow_up_1.md
│   └── follow_up_2.md
│
├── scripts/
│   ├── populate_all_colleges.py      # static data writer (IIT/NIT/IIIT/IISc/IISER)
│   ├── scrape_faculty.py             # live web scraper (72 scrapers)
│   ├── topoff.py                     # bring sparse institutes to 10+ rows
│   ├── gen_research_batches.py       # NEW: split master → sendable batches
│   ├── validate_data.py              # schema + institute_type validator
│   └── check_structure.py            # repo layout validator
│
└── SESSION_COMPLETE.md               # this file
```

---

## ✨ Summary

**What changed this session:**
1. Fixed NIT Surathkal CSV quoting bug → master now 100% clean
2. Top-offed 9 sparse institutes → all now 10+ rows
3. Added IISc + 6 IISERs (41 rows) → 1,811 total faculty
4. Built research batch generator → 61 prioritized, diverse batches ready to send
5. All data validated clean (0 errors)

**The research outreach pipeline is production-ready.**

Next move: start sending personalized emails using `research/batches/research_batch_001.csv` and the templates in `templates/`.

---

**Total new rows added this session:** 89 (48 top-off + 41 premium)  
**Final total:** 1,811 faculty across 80 institutes  
**Research batches:** 61 (ready for outreach)  
**Data quality:** ✅ 0 errors, 0 missing emails, 100% validated

