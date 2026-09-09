#!/usr/bin/env python3
"""
career_watch.py — Monitor company career pages and alert on NEW entries.

Reads career_pages.csv (Company, URL, Location, EntryLevel, Notes), fetches each
page, extracts job-like entries (anchor text + lines matching role keywords),
and diffs against the saved snapshot in career_state.json. New entries are
written to career_alerts.md (consumed by the GitHub Action to open an issue) and
appended to career_alerts.log. State is updated in place so the next run only
reports genuinely new postings.

Region split:
  - Every posting is classified from its Location (falling back to Company /
    Notes) into 🇮🇳 India, 🌍 Outside India, or 📍 Unspecified, and the alert
    is grouped under those headings so India and non-India roles are separated
    at a glance. Outside-India markers (Dubai, Singapore, USA, ...) win over
    India markers.

Fresher focus:
  - Entries that look like 0-experience roles (fresher/graduate/trainee/intern/
    entry level/0-1 yr/campus) are flagged with 🎓.
  - If a row sets EntryLevel=yes (the default for every page), ONLY those
    fresher entries are alerted. A title is dropped even when it matches the
    fresher wording if it also carries a seniority marker (senior/lead/manager/
    architect/...) or asks for 2+ years of experience — so "Senior Associate"
    and "Graduate Engineer, 3-5 years" stay out of the inbox.

City & software focus (all default ON, env-overridable):
  - CITY_FOCUS=1 restricts to TARGET_CITIES (default Hyderabad, Pune,
    Bengaluru) plus pan-India portals when ALLOW_NATIONAL=1. Sources for any
    other explicit city are skipped before fetching, cutting render time.
  - ALLOW_PRIORITY=1 exempts curated global sources (YC startups, marquee
    MNCs, EPAM) from the city filter — tag their Notes with "[priority]".
  - REMOTE_OR_INDIA=1 keeps only remote or Indian-city postings and drops
    foreign on-site roles (a US-based YC page then only surfaces its remote
    or India openings).
  - SOFTWARE_ONLY=1 keeps only software-engineering / dev / AI-ML roles for
    every source and drops non-technical openings (HR, sales, BPO, ...);
    entry-tagged sources additionally require a fresher / 0-exp signal.
  - Widen again with CITY_FOCUS=0 / SOFTWARE_ONLY=0 / TARGET_CITIES=... .

Rendering:
  - Default: static fetch (requests). Fast, but JS-rendered/SPA career pages
    (most large MNC portals) return 0 entries.
  - Set RENDER=1 (and `pip install playwright && playwright install chromium`)
    to render JavaScript so SPA pages yield listings.

Run:
    pip install requests
    python career_watch.py

Optional email alert (set all five env vars):
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ALERT_TO
"""
import asyncio
import csv
import json
import os
import re
import sys
import smtplib
import datetime as dt
from email.mime.text import MIMEText
from html.parser import HTMLParser

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: pip install requests")

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_CSV = os.path.join(_ROOT, "industry", "career_pages.csv")
STATE_FILE = os.path.join(_ROOT, "state", "career_state.json")
ALERTS_MD = os.path.join(_ROOT, "state", "career_alerts.md")
ALERTS_LOG = os.path.join(_ROOT, "state", "career_alerts.log")

UA = "Mozilla/5.0 (compatible; CareerWatch/1.0; internship-outreach)"
TIMEOUT = 25
RENDER = os.getenv("RENDER") == "1"
CONCURRENCY = int(os.getenv("CONCURRENCY", "6"))

# --- Focus knobs (all default ON; override via env to widen again) --------
# CITY_FOCUS restricts the watch to the target cities below (plus, when
# ALLOW_NATIONAL, pan-India portals). Sources for any other explicit city
# (Ahmedabad, Gandhinagar, Gurugram, Chennai, Dubai, ...) are skipped BEFORE
# fetching, which also cuts the render time / Actions minutes.
CITY_FOCUS = os.getenv("CITY_FOCUS", "1") == "1"
TARGET_CITIES = [c.strip().lower() for c in
                 os.getenv("TARGET_CITIES", "hyderabad,pune,bengaluru,bangalore").split(",")
                 if c.strip()]
ALLOW_NATIONAL = os.getenv("ALLOW_NATIONAL", "1") == "1"
# ALLOW_PRIORITY keeps curated global sources (YC startups, marquee MNCs, EPAM)
# regardless of city: tag their Notes with "[priority]" and they are always
# watched even when the Location is blank or outside the target cities. Their
# postings are still run through the software / fresher gates below.
ALLOW_PRIORITY = os.getenv("ALLOW_PRIORITY", "1") == "1"
# REMOTE_OR_INDIA drops postings whose title names a foreign on-site location:
# a role is kept only when it is remote or in an Indian city (titles with no
# location are kept for India-based sources and dropped for global ones).
REMOTE_OR_INDIA = os.getenv("REMOTE_OR_INDIA", "1") == "1"
# SOFTWARE_ONLY keeps only software-engineering / dev / AI-ML roles and drops
# non-technical openings (HR, sales, BPO, marketing, ...). Entry-tagged sources
# additionally require a fresher / 0-exp signal.
SOFTWARE_ONLY = os.getenv("SOFTWARE_ONLY", "1") == "1"

ROLE_RE = re.compile(
    r"\b(engineer|developer|intern(ship)?|manager|designer|analyst|lead|architect|"
    r"consultant|executive|associate|specialist|trainee|qa|sde|devops|scientist|"
    r"recruiter|fresher|hiring|vacancy|opening|apply|graduate)\b",
    re.I,
)
# Looks like a 0-experience / early-career role.
ENTRY_RE = re.compile(
    r"\b(fresher|freshers|graduate|trainee|intern(ship)?|entry[ -]?level|"
    r"campus|off[ -]?campus|associate|junior|0[ -]?1\s*year|0\s*-\s*1|"
    r"no experience|0\s*yr|new grad)\b",
    re.I,
)
# AI/ML roles.
AIML_RE = re.compile(
    r"\b(ai|ml|machine learning|deep learning|data scien(ce|tist)|nlp|"
    r"computer vision|gen(?:erative)?\s?ai|llm|mlops|artificial intelligence)\b",
    re.I,
)
# Software-engineering / dev roles.
SDE_RE = re.compile(
    r"\b(sde|sdet|software (engineer|developer|development)|back[ -]?end|"
    r"front[ -]?end|full[ -]?stack|web developer|programmer)\b",
    re.I,
)
# Seniority markers — disqualify an entry even if it matches ENTRY_RE
# ("Senior Associate", "Associate Director", "Lead Graduate Engineer").
SENIOR_RE = re.compile(
    r"\b(sr\.?|senior|lead|leader|principal|staff engineer|manager|head of|"
    r"director|vice[ -]president|vp|architect|chief|expert|mentor|"
    r"experienced|mid[ -]level)\b",
    re.I,
)
# Any "N years" / "N-M yrs" ask in the title.
EXP_RE = re.compile(
    r"\b(\d{1,2})\s*(?:\+|-|–|to)?\s*(\d{1,2})?\s*(?:\+)?\s*(?:years?|yrs?)\b",
    re.I,
)
NOISE_RE = re.compile(
    r"^(home|about|contact|privacy|terms|cookie|login|sign in|menu|careers?|"
    r"life at|why join|benefits|culture|search|apply now|view all|learn more)$",
    re.I,
)
# Broad software-engineering / dev role match (AIML_RE also counts as software).
SOFTWARE_RE = re.compile(
    r"\b(sde|sdet|software\s+(?:engineer|developer|development|programmer)|"
    r"back[ -]?end|front[ -]?end|full[ -]?stack|web\s+(?:developer|development)|"
    r"mobile\s+(?:app\s+)?(?:developer|development)|android|ios|programmer|"
    r"devops|site\s+reliability|\bsre\b|cloud\s+engineer|data\s+engineer|"
    r"platform\s+engineer|application\s+(?:developer|engineer)|python|java\b|"
    r"javascript|golang|\.net|react|angular|node\.?js|test\s+automation|"
    r"automation\s+engineer|qa\s+(?:engineer|automation))\b",
    re.I,
)
# Non-software fresher roles to exclude even when they carry fresher wording.
NONSOFTWARE_RE = re.compile(
    r"\b(recruit(er|ment)|talent acquisition|\bhr\b|human resources|"
    r"\bsales\b|business development|\bbde\b|\bbdm\b|marketing|\bseo\b|\bsmm\b|"
    r"content writer|copywriter|tele[ -]?caller|customer (support|service|success)|"
    r"\bbpo\b|\bkpo\b|voice process|non[ -]?voice|account(s|ant)|finance|"
    r"admin(istrator|istration)?|receptionist|operations|logistics|procurement|"
    r"mechanical|civil engineer|electrical engineer|graphic designer|"
    r"digital marketing|social media)\b",
    re.I,
)
# Target-city focus (default Hyderabad / Pune / Bengaluru).
TARGET_CITY_RE = re.compile(
    r"\b(" + "|".join(re.escape(c) for c in TARGET_CITIES) + r")\b", re.I
) if TARGET_CITIES else None
# Pan-India / national portals (kept when ALLOW_NATIONAL) — they surface the
# target cities even though the source Location is just "India".
NATIONAL_RE = re.compile(
    r"\b(india|pan[ -]?india|all[ -]?india|across india|multiple locations|"
    r"remote[ -]?india)\b",
    re.I,
)
# Curated priority sources (YC startups, marquee MNCs) carry a "[priority]" tag
# in their Notes and bypass the city filter — they are watched wherever based.
PRIORITY_RE = re.compile(r"\[priority\]", re.I)

# --- India vs outside-India classification -------------------------------
# A page's Location (falling back to Company / Notes) decides which bucket its
# new postings land in. Outside markers win over India markers, so "Dubai
# office of an Indian firm" is correctly Outside India.
OUTSIDE_RE = re.compile(
    r"\b(dubai|u\.?a\.?e|united arab emirates|sharjah|abu dhabi|ajman|"
    r"singapore|qatar|doha|saudi|riyadh|jeddah|oman|muscat|bahrain|manama|"
    r"kuwait|usa|u\.?s\.?a|united states|new york|san francisco|silicon valley|"
    r"uk|united kingdom|london|ireland|dublin|canada|toronto|vancouver|"
    r"germany|berlin|munich|netherlands|amsterdam|france|paris|"
    r"australia|sydney|melbourne|europe|remote[ -]?(us|usa|eu|global))\b",
    re.I,
)
INDIA_RE = re.compile(
    r"\b(india|bengaluru|bangalore|ahmedabad|gurugram|gurgaon|pune|hyderabad|"
    r"chennai|noida|gandhinagar|mumbai|navi mumbai|jaipur|indore|delhi|new delhi|"
    r"kolkata|kochi|cochin|lucknow|vadodara|baroda|kanpur|prayagraj|allahabad|"
    r"mohali|chandigarh|surat|rajkot|kota|nashik|thiruvananthapuram|trivandrum|"
    r"coimbatore|dehradun|nagpur|bhubaneswar|agra|anand|ludhiana|thrissur|"
    r"visakhapatnam|vizag|madurai|varanasi|meerut|ghaziabad|tirupati|vijayawada|"
    r"bhopal|gwalior|udaipur|jodhpur|deoria|gorakhpur|basti|bikaner|bhilwara|"
    r"ajmer|biharsharif|mysuru|mysore|gujarat|maharashtra|karnataka|telangana|"
    r"tamil nadu|kerala|rajasthan|uttar pradesh|west bengal|odisha|punjab|"
    r"haryana|madhya pradesh|uttarakhand|andhra|bihar|jharkhand|chhattisgarh|"
    r"goa|assam)\b",
    re.I,
)

# Remote markers (a remote role is acceptable wherever the company is based).
# Remote-US / remote-EU / remote-global are treated as foreign by OUTSIDE_RE.
REMOTE_RE = re.compile(
    r"\b(remote|work[ -]?from[ -]?home|wfh|anywhere|distributed|hybrid[ -]?india)\b",
    re.I,
)

INDIA = "India"
OUTSIDE = "Outside India"
UNSPECIFIED = "Unspecified"
REGION_ORDER = [INDIA, OUTSIDE, UNSPECIFIED]
REGION_HDR = {
    INDIA: "🇮🇳 India",
    OUTSIDE: "🌍 Outside India",
    UNSPECIFIED: "📍 Unspecified location",
}


def region_of(location, company="", notes=""):
    """Classify a posting as India / Outside India / Unspecified."""
    blob = " ".join(x for x in (location, company, notes) if x)
    if OUTSIDE_RE.search(blob):
        return OUTSIDE
    if INDIA_RE.search(blob):
        return INDIA
    return UNSPECIFIED


def location_ok(entry, source_region):
    """Keep a posting only if it is remote or in an Indian city.

    A title naming a foreign on-site location (San Francisco, London, ...) is
    dropped; remote or India-city titles are kept. When the title carries no
    location, it is kept for India-based sources and dropped for global ones
    (YC / overseas boards), since an untagged role there is most likely abroad.
    """
    if not REMOTE_OR_INDIA:
        return True
    if OUTSIDE_RE.search(entry) and not INDIA_RE.search(entry):
        return False
    if REMOTE_RE.search(entry):
        return True
    if INDIA_RE.search(entry):
        return True
    return source_region == INDIA


def city_focus_ok(location, company="", notes=""):
    """True if the source belongs to a target city (or a pan-India portal).

    When CITY_FOCUS is off, every source qualifies (original behaviour).
    """
    if not CITY_FOCUS:
        return True
    # Curated priority sources (YC startups, marquee MNCs) are watched wherever
    # they are based — their postings are still software / fresher filtered.
    if ALLOW_PRIORITY and PRIORITY_RE.search(notes or ""):
        return True
    # The Location column is authoritative: a target/national Location keeps
    # the source; any other named place is off-focus even if Company/Notes
    # happen to mention India or another city.
    loc = location or ""
    if TARGET_CITY_RE and TARGET_CITY_RE.search(loc):
        return True
    if ALLOW_NATIONAL and NATIONAL_RE.search(loc):
        return True
    if loc.strip():
        return False
    # Only when Location is blank do we fall back to Company / Notes hints.
    blob = " ".join(x for x in (company, notes) if x)
    if TARGET_CITY_RE and TARGET_CITY_RE.search(blob):
        return True
    if ALLOW_NATIONAL and NATIONAL_RE.search(blob):
        return True
    return False


def is_software(s):
    """True for software-engineering / dev / AI-ML roles, excluding non-tech."""
    if NONSOFTWARE_RE.search(s):
        return False
    return bool(SOFTWARE_RE.search(s) or AIML_RE.search(s))


class TextLinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chunks = []
        self._skip = 0
        self._in_a = False
        self._a_text = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self._skip += 1
        if tag == "a":
            self._in_a = True
            self._a_text = []

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self._skip:
            self._skip -= 1
        if tag == "a" and self._in_a:
            self._in_a = False
            t = " ".join(self._a_text).strip()
            if t:
                self.chunks.append(t)

    def handle_data(self, data):
        if self._skip:
            return
        text = data.strip()
        if not text:
            return
        if self._in_a:
            self._a_text.append(text)
        else:
            self.chunks.append(text)


def normalize(s):
    return re.sub(r"\s+", " ", s).strip()


def extract_entries(html):
    parser = TextLinkExtractor()
    try:
        parser.feed(html)
    except Exception:
        pass
    entries = set()
    for raw in parser.chunks:
        s = normalize(raw)
        if not (3 < len(s) < 140):
            continue
        if NOISE_RE.match(s):
            continue
        if ROLE_RE.search(s):
            entries.add(s)
    return sorted(entries)


def is_entry_level(s):
    return bool(ENTRY_RE.search(s))


def demands_experience(s):
    """True if the entry asks for 2+ years — "0-1 years" and "1 year" stay in."""
    for m in EXP_RE.finditer(s):
        nums = [int(n) for n in m.groups() if n]
        if nums and max(nums) >= 2:
            return True
    return False


def is_fresher(s):
    """0-experience role: fresher wording, no seniority marker, no 2+ yr ask."""
    if s.rstrip().endswith("?"):
        return False  # FAQ boilerplate on aggregator/portal pages
    # FIX (Bug 5): wrap the entire boolean expression in a single return statement
    # so all three conditions are evaluated together, not independently.
    return (
        bool(ENTRY_RE.search(s))
        and not SENIOR_RE.search(s)
        and not demands_experience(s)
    )


def is_software_fresher(s):
    """0-experience AND software-engineering / dev / AI-ML role."""
    return is_fresher(s) and is_software(s)


def tags(s):
    t = ""
    if ENTRY_RE.search(s):
        t += "🎓 "
    if AIML_RE.search(s):
        t += "🧪 "
    if SDE_RE.search(s):
        t += "💻 "
    return t


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False, sort_keys=True)


def read_pages():
    with open(PAGES_CSV, encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r.get("URL", "").strip()]


def fetch_static(url):
    r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.text


def fetch_all_static(urls):
    """Fetch URLs concurrently with threads (requests is thread-safe)."""
    from concurrent.futures import ThreadPoolExecutor
    results = {}

    def one(u):
        try:
            return u, fetch_static(u)
        except Exception as e:  # noqa: BLE001
            return u, e

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        for u, res in ex.map(one, urls):
            results[u] = res
    return results


async def _fetch_all_rendered(urls):
    """Render URLs concurrently sharing one Playwright browser."""
    from playwright.async_api import async_playwright
    results = {}
    sem = asyncio.Semaphore(CONCURRENCY)
    async with async_playwright() as p:
        # --disable-http2 avoids ERR_HTTP2_PROTOCOL_ERROR on some corporate sites.
        browser = await p.chromium.launch(args=["--disable-http2"])

        async def one(u):
            async with sem:
                page = await browser.new_page(user_agent=UA)
                try:
                    # domcontentloaded + a short settle beats networkidle, which
                    # never fires on SPAs with polling/analytics/websockets.
                    await page.goto(u, wait_until="domcontentloaded",
                                    timeout=TIMEOUT * 1000)
                    await page.wait_for_timeout(3500)  # let JS render listings
                    results[u] = await page.content()
                except Exception as e:  # noqa: BLE001
                    results[u] = e
                finally:
                    await page.close()

        await asyncio.gather(*(one(u) for u in urls))
        await browser.close()
    return results


def fetch_all(urls):
    """Return {url: html or Exception}. Renders JS when RENDER=1."""
    if RENDER:
        try:
            import playwright  # noqa: F401
        except ImportError:
            print("RENDER=1 but Playwright not installed; using static fetch.",
                  file=sys.stderr)
        else:
            return asyncio.run(_fetch_all_rendered(urls))
    return fetch_all_static(urls)


def truthy(v):
    return str(v).strip().lower() in ("yes", "true", "1", "y")


def send_email(subject, body):
    # FIX (Bug 4): SMTP_PORT was missing from the guard check, causing a
    # TypeError crash when SMTP_PORT is unset. It is now required alongside
    # the other four SMTP env vars before attempting any connection.
    if not all(os.getenv(k) for k in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "ALERT_TO")):
        return False
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = os.getenv("ALERT_TO")
    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT", "587"))) as s:
        s.starttls()
        s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        s.sendmail(msg["From"], [msg["To"]], msg.as_string())
    return True


def main():
    now = dt.datetime.now().isoformat(timespec="seconds")
    state = load_state()
    all_pages = read_pages()
    pages = [r for r in all_pages
             if city_focus_ok(r.get("Location", ""), r.get("Company", ""),
                              r.get("Notes", ""))]
    skipped_city = len(all_pages) - len(pages)
    alerts = []    # (label, url, [entries])
    errors = []

    # Fetch every unique URL once, concurrently.
    unique_urls = list(dict.fromkeys(row["URL"].strip() for row in pages))
    htmls = fetch_all(unique_urls)

    for row in pages:
        company = row.get("Company", "").strip() or row["URL"]
        location = row.get("Location", "").strip()
        label = f"{company} — {location}" if location else company
        url = row["URL"].strip()
        entry_only = truthy(row.get("EntryLevel", ""))
        region = region_of(location, company, row.get("Notes", ""))

        res = htmls.get(url)
        if not isinstance(res, str):
            errors.append((label, url, str(res)[:120] if res else "no result"))
            continue
        entries = extract_entries(res)

        prev = set(state.get(url, {}).get("entries", []))
        first_run = url not in state
        new = [e for e in entries if e not in prev]
        if entry_only:
            keep = is_software_fresher if SOFTWARE_ONLY else is_fresher
            new = [e for e in new if keep(e)]
        elif SOFTWARE_ONLY:
            # Non-entry sources (YC / MNC boards that don't tag seniority) still
            # get software-only filtering, so sales / HR / ops don't leak in.
            new = [e for e in new if is_software(e)]
        # Keep only remote or Indian-city roles (drops foreign on-site).
        new = [e for e in new if location_ok(e, region)]

        if new and not first_run:
            alerts.append((region, label, url, new))

        state[url] = {
            "company": company,
            "location": location,
            "region": region,
            "entry_only": entry_only,
            "entries": entries,
            "count": len(entries),
            "last_checked": now,
        }

    save_state(state)

    # Group new postings into India / Outside India / Unspecified sections.
    by_region = {}
    for region, label, url, items in alerts:
        by_region.setdefault(region, []).append((label, url, items))

    md_lines = []
    if alerts:
        md_lines.append(f"# 📢 New career-page entries — {now}\n")
        counts = {r: sum(len(i) for _, _, i in by_region.get(r, [])) for r in REGION_ORDER}
        summary = " · ".join(f"{REGION_HDR[r]}: {counts[r]}" for r in REGION_ORDER if counts[r])
        md_lines.append(f"**{summary}**\n")
        for region in REGION_ORDER:
            group = by_region.get(region)
            if not group:
                continue
            md_lines.append(f"## {REGION_HDR[region]} — {counts[region]} new\n")
            for label, url, items in group:
                md_lines.append(f"### {label}\n<{url}>\n")
                for entry in items:
                    md_lines.append(f"- {tags(entry)}{entry}")
                md_lines.append("")
    md = "\n".join(md_lines)

    with open(ALERTS_MD, "w", encoding="utf-8") as f:
        f.write(md)

    if alerts:
        with open(ALERTS_LOG, "a", encoding="utf-8") as f:
            f.write(md + "\n")
        total = sum(len(items) for _, _, _, items in alerts)
        region_counts = {
            r: sum(len(i) for _, _, i in by_region.get(r, [])) for r in REGION_ORDER
        }
        breakdown = ", ".join(
            f"{r}: {region_counts[r]}" for r in REGION_ORDER if region_counts[r]
        )
        sent = send_email(f"[CareerWatch] {total} new posting(s)", md)
        print(f"ALERT: {total} new entries across {len(alerts)} pages "
              f"({breakdown}){'  (emailed)' if sent else ''}")
    else:
        print("No new entries.")

    for label, url, err in errors:
        print(f"  ! fetch failed: {label} <{url}> — {err}", file=sys.stderr)

    mode = "RENDER" if RENDER else "static"
    focus = []
    if CITY_FOCUS:
        focus.append("cities=" + "/".join(TARGET_CITIES)
                     + ("+national" if ALLOW_NATIONAL else "")
                     + ("+priority" if ALLOW_PRIORITY else ""))
    if SOFTWARE_ONLY:
        focus.append("software-only")
    if REMOTE_OR_INDIA:
        focus.append("remote/india-only")
    focus_note = ("; ".join(focus) + f"; skipped {skipped_city} off-focus sources") if focus else ""
    print(f"Checked {len(pages)} pages ({mode}), {len(errors)} errors, {now}"
          + (f" [{focus_note}]" if focus_note else ""))


if __name__ == "__main__":
    main()
