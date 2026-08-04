#!/usr/bin/env python3
"""
scrape_faculty.py — Scrape ALL IIT / NIT / IIIT CSE faculty pages and
merge new contacts into the per-institute CSV + faculty_master.csv.

Strategy
--------
* requests + BeautifulSoup for static HTML pages  (fast, no overhead)
* Playwright headless Chromium for JS-rendered pages (SPA / React / Angular)
* Per-institute scraper functions defined in SCRAPERS dict:
    key  = relative path used in research/faculty/  (same key as populate script)
    value = callable(session) -> list[dict]   (each dict = one faculty row)
* Deduplication: rows already in the CSV (matched by email) are skipped.
* After all institutes run, faculty_master.csv is rebuilt.

Usage
-----
    python scripts/scrape_faculty.py               # scrape everything
    python scripts/scrape_faculty.py iit-bombay    # single institute by name
    python scripts/scrape_faculty.py --dry-run     # print rows, don't write

Dependencies: requests, beautifulsoup4, lxml, playwright (chromium)
    pip install requests beautifulsoup4 lxml playwright
    python -m playwright install chromium
"""

import csv
import os
import re
import sys
import time
import warnings
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")  # suppress SSL warnings for .ac.in certs

# ── paths ──────────────────────────────────────────────────────────────────
HERE     = os.path.dirname(os.path.abspath(__file__))
ROOT     = os.path.dirname(HERE)
RESEARCH = os.path.join(ROOT, "research")
FAC_DIR  = os.path.join(RESEARCH, "faculty")
MASTER   = os.path.join(RESEARCH, "faculty_master.csv")

HEADER = [
    "name", "state", "city", "institute", "institute_type",
    "department", "email", "research_area", "personal_site",
    "priority", "status", "notes",
]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36")

# ── helpers ─────────────────────────────────────────────────────────────────

def make_session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    s.verify = False
    return s

def get_html(session, url, timeout=20):
    """Fetch URL with requests. Returns (html_str, final_url) or ('', url)."""
    try:
        r = session.get(url, timeout=timeout, allow_redirects=True)
        r.raise_for_status()
        return r.text, r.url
    except Exception as e:
        print(f"    [WARN] requests failed {url}: {e}")
        return "", url

_PW_BROWSER = None
_PW_INSTANCE = None

def _get_browser():
    """Lazy-init a single shared Playwright browser (call close_browser() at end)."""
    global _PW_BROWSER, _PW_INSTANCE
    if _PW_BROWSER is None:
        from playwright.sync_api import sync_playwright
        _PW_INSTANCE = sync_playwright().start()
        _PW_BROWSER = _PW_INSTANCE.chromium.launch(headless=True)
    return _PW_BROWSER

def close_browser():
    global _PW_BROWSER, _PW_INSTANCE
    try:
        if _PW_BROWSER:
            _PW_BROWSER.close()
            _PW_BROWSER = None
        if _PW_INSTANCE:
            _PW_INSTANCE.stop()
            _PW_INSTANCE = None
    except Exception:
        pass

def get_html_js(url, wait_sel=None, timeout=15000):
    """Fetch JS-rendered page via shared Playwright browser. Returns html string."""
    from playwright.sync_api import TimeoutError as PWTimeout
    html = ""
    try:
        browser = _get_browser()
        page = browser.new_page(user_agent=UA)
        page.goto(url, timeout=timeout, wait_until='domcontentloaded')
        if wait_sel:
            try:
                page.wait_for_selector(wait_sel, timeout=6000)
            except PWTimeout:
                pass
        else:
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except PWTimeout:
                pass
        html = page.content()
        page.close()
    except Exception as e:
        print(f"    [WARN] playwright failed {url}: {e}")
        try:
            page.close()
        except Exception:
            pass
    return html

def soup(html):
    return BeautifulSoup(html, "lxml")

EMAIL_RE = re.compile(r'[\w.+\-]+@[\w.\-]+\.[a-z]{2,}', re.I)

def find_emails(text):
    """Return list of unique lowercase institutional emails, skip generic/admin."""
    skip_locals = {
        'webmaster', 'admin', 'info', 'contact', 'office', 'support',
        'noreply', 'no-reply', 'helpdesk', 'example', 'chairman',
        'director', 'registrar', 'dean', 'hod', 'dept', 'department',
        'reception', 'library', 'accounts', 'finance', 'hostel',
        'placement', 'alumni', 'newsletter', 'notification', 'cse',
        'ece', 'eee', 'mech', 'civil', 'general', 'phdsection',
        'pgsection', 'ugsection', 'phd', 'research', 'scholarship',
        'academicclaims', 'complaints', 'feedback', 'helpline',
    }
    skip_domains = {'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
                    'rediffmail.com', 'yahoo.co.in'}
    raw = EMAIL_RE.findall(text)
    seen = set()
    out = []
    for e in raw:
        el = e.lower().rstrip('.')
        local = el.split('@')[0]
        domain = el.split('@')[1] if '@' in el else ''
        if local in skip_locals:
            continue
        if domain in skip_domains:
            continue
        if el in seen:
            continue
        seen.add(el)
        out.append(el)
    return out

# Faculty name patterns: lines that look like headings, not section labels
_NOT_NAME_RE = re.compile(
    r'(?i)^(field|academic|qualification|specializ|section|department|'
    r'research interest|area of|email|phone|designation|position|'
    r'professor|associate|assistant|home|faculty|staff|people|'
    r'page|click|view|more|dr\.\s*$|profile)', re.I
)

def looks_like_name(text):
    """Return True if text plausibly is a person's name."""
    t = text.strip()
    if not t or len(t) < 4 or len(t) > 80:
        return False
    if _NOT_NAME_RE.match(t):
        return False
    # Must have at least one word that starts with capital
    words = t.split()
    if not any(w[0].isupper() for w in words if w):
        return False
    return True

def clean(text):
    """Strip whitespace, collapse internal spaces."""
    return re.sub(r'\s+', ' ', (text or '').strip())

def make_row(name, state, city, institute, itype, dept, email,
             area='', site='', priority='1', status='queued', notes=''):
    return {
        'name': clean(name), 'state': state, 'city': city,
        'institute': institute, 'institute_type': itype,
        'department': dept, 'email': email.lower().strip(),
        'research_area': clean(area), 'personal_site': site.strip(),
        'priority': priority, 'status': status, 'notes': notes,
    }

def load_existing_emails(csv_path):
    """Return set of lowercase emails already in the CSV."""
    if not os.path.exists(csv_path):
        return set()
    with open(csv_path, encoding='utf-8', newline='') as f:
        return {r['email'].lower().strip()
                for r in csv.DictReader(f) if r.get('email')}

def append_rows(csv_path, rows):
    """Append new rows to CSV (create with header if absent)."""
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    write_header = not os.path.exists(csv_path)
    with open(csv_path, 'a', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        if write_header:
            w.writeheader()
        w.writerows(rows)

# ── generic scrapers (reusable patterns) ────────────────────────────────────

def scrape_nitt_style(session, base_url, state, city, institute, itype):
    """
    NIT Trichy style: listing page -> individual faculty profile pages.
    Picks up name from page title/h1/h2, email from page body.
    """
    rows = []
    html, _ = get_html(session, base_url)
    if not html:
        # try JS render
        html = get_html_js(base_url)
    if not html:
        return rows
    s = soup(html)
    links = []
    for a in s.find_all('a', href=True):
        href = a['href']
        link_text = clean(a.get_text())
        # Individual faculty pages: typically short slug under /faculty/
        full = urljoin(base_url, href)
        if (full.startswith(base_url) and full != base_url and
                full not in links and
                re.search(r'/faculty/\w+/?$', full)):
            links.append(full)
    # Also accept any .ac.in faculty links on page
    for a in s.find_all('a', href=True):
        href = a['href']
        full = urljoin(base_url, href)
        if (full not in links and full != base_url and
                re.search(r'\/(faculty|people|staff)\/\w', full)):
            links.append(full)

    for link in links[:100]:
        time.sleep(0.4)
        fhtml, _ = get_html(session, link)
        if not fhtml:
            continue
        fs = soup(fhtml)
        emails = find_emails(fhtml)
        if not emails:
            continue
        # Name: try title tag, then h1, h2, h3
        name = ''
        for tag in [fs.find('title'), fs.find('h1'), fs.find('h2'), fs.find('h3')]:
            if tag:
                candidate = clean(tag.get_text())
                # Strip site name from title (e.g. "NIT Trichy - Dr. X")
                if ' - ' in candidate:
                    candidate = candidate.split(' - ', 1)[1].strip()
                if looks_like_name(candidate):
                    name = candidate
                    break
        if not name:
            continue
        # Research area
        area = ''
        for tag in fs.find_all(['p', 'li', 'div', 'td', 'span']):
            txt = clean(tag.get_text())
            if re.search(r'research\s+(interest|area|specializ)', txt, re.I):
                sib = tag.find_next_sibling()
                area = clean(sib.get_text()) if sib else txt
                area = area[:250]
                break
        for email in emails[:2]:   # at most 2 per page (inst + personal)
            rows.append(make_row(name, state, city, institute, itype,
                                 'CSE', email, area, link))
    return rows

def scrape_profile_list(session, url, state, city, institute, itype,
                        name_sel, email_sel=None, area_sel=None,
                        link_sel=None, use_js=False):
    """
    Generic: page has a list of faculty cards.
    name_sel  = CSS selector for name element
    email_sel = CSS selector for email element (optional)
    area_sel  = CSS selector for research area (optional)
    link_sel  = CSS selector for link to individual profile (optional)
    """
    rows = []
    html = get_html_js(url) if use_js else get_html(session, url)[0]
    if not html:
        return rows
    s = soup(html)
    cards = s.select(name_sel)
    for card in cards:
        name = clean(card.get_text())
        if not name or len(name) < 3:
            continue
        email = ''
        if email_sel:
            el = card.find_parent().select_one(email_sel) if email_sel else None
            if el:
                email = clean(el.get_text())
        if not email:
            # try to find email in surrounding container
            container = card.find_parent(['div', 'li', 'tr', 'article'])
            if container:
                emails = find_emails(container.decode_contents())
                email = emails[0] if emails else ''
        area = ''
        if area_sel:
            el = card.find_parent().select_one(area_sel) if area_sel else None
            if el:
                area = clean(el.get_text())
        site = ''
        if link_sel:
            la = card.find_parent().select_one(link_sel) if link_sel else None
            if la and la.get('href'):
                site = urljoin(url, la['href'])
        if name and email:
            rows.append(make_row(name, state, city, institute, itype,
                                 'CSE', email, area, site))
    return rows

def scrape_table(session, url, state, city, institute, itype,
                 name_col=0, email_col=None, area_col=None, use_js=False):
    """Scrape HTML tables where faculty = rows."""
    rows = []
    html = get_html_js(url) if use_js else get_html(session, url)[0]
    if not html:
        return rows
    s = soup(html)
    for table in s.find_all('table'):
        for tr in table.find_all('tr')[1:]:
            cells = [clean(td.get_text()) for td in tr.find_all(['td', 'th'])]
            if len(cells) <= name_col:
                continue
            name = cells[name_col]
            if not name or len(name) < 3:
                continue
            email = cells[email_col] if email_col and email_col < len(cells) else ''
            if not email:
                emails = find_emails(tr.decode_contents())
                email = emails[0] if emails else ''
            area = cells[area_col] if area_col and area_col < len(cells) else ''
            if email:
                rows.append(make_row(name, state, city, institute, itype,
                                     'CSE', email, area))
    return rows

def scrape_email_grep(session, url, state, city, institute, itype,
                      domain_hint, name_sel=None, use_js=False):
    """
    Fallback: just grab page HTML, find all emails matching domain_hint,
    try to find adjacent name text.
    """
    rows = []
    html = get_html_js(url) if use_js else get_html(session, url)[0]
    if not html:
        return rows
    s = soup(html)
    # Find elements containing emails from this domain
    text = html
    emails = [e for e in find_emails(text) if domain_hint in e]
    for email in emails:
        # Find the email in BS4 tree and look for nearby name
        name = ''
        for el in s.find_all(string=re.compile(re.escape(email.split('@')[0]), re.I)):
            parent = el.find_parent(['td', 'li', 'div', 'p', 'tr'])
            if parent:
                # Look for a bold/heading nearby
                heading = parent.find(['b', 'strong', 'h3', 'h4', 'a'])
                if heading:
                    name = clean(heading.get_text())
                    break
        if not name:
            name = email.split('@')[0].replace('.', ' ').title()
        rows.append(make_row(name, state, city, institute, itype,
                             'CSE', email))
    return rows

def scrape_iit_guwahati(session):
    """IIT Guwahati CSE – JS-rendered page with faculty cards."""
    st, ci, inst, it = 'assam', 'guwahati', 'IIT Guwahati', 'IIT'
    url = 'https://www.iitg.ac.in/cse/people.html'
    html = get_html_js(url, wait_sel='.faculty-name, h3, .card')
    rows = []
    if not html:
        return rows
    s = soup(html)
    # Try card-based layout
    for card in s.select('div.card, div.team-item, div.faculty-card, article'):
        emails = find_emails(card.decode_contents())
        if not emails:
            continue
        name_el = card.find(['h3', 'h4', 'h5', 'strong', 'b'])
        name = clean(name_el.get_text()) if name_el else ''
        area_el = card.find(string=re.compile(r'research|interest|area', re.I))
        area = ''
        if area_el:
            p = area_el.find_parent(['p', 'div', 'li'])
            area = clean(p.get_text()) if p else ''
        link_el = card.find('a', href=True)
        site = urljoin(url, link_el['href']) if link_el else ''
        for email in emails[:1]:
            if name:
                rows.append(make_row(name, st, ci, inst, it, 'CSE',
                                     email, area, site))
    # Fallback: email grep
    if not rows:
        rows = scrape_email_grep(session, url, st, ci, inst, it,
                                 'iitg.ac.in', use_js=False)
        # Also try the dept page
        url2 = 'https://www.iitg.ac.in/cse/'
        rows2 = scrape_email_grep(session, url2, st, ci, inst, it,
                                  'iitg.ac.in')
        rows += rows2
    return rows

def scrape_iit_kanpur(session):
    """IIT Kanpur CSE – static faculty list page."""
    st, ci, inst, it = 'uttar-pradesh', 'kanpur', 'IIT Kanpur', 'IIT'
    url = 'https://www.cse.iitk.ac.in/pages/Faculty.html'
    html, _ = get_html(session, url)
    rows = []
    if not html:
        return rows
    s = soup(html)
    # Each faculty in a separate section/card
    for el in s.select('div.faculty, section, div.profile, li.faculty'):
        emails = find_emails(el.decode_contents())
        if not emails:
            continue
        name_el = el.find(['h2', 'h3', 'h4', 'strong', 'b'])
        name = clean(name_el.get_text()) if name_el else ''
        for email in emails[:1]:
            rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
    if not rows:
        rows = scrape_email_grep(session, url, st, ci, inst, it, 'iitk.ac.in')
    return rows

def scrape_iit_bombay(session):
    """IIT Bombay CSE – scrape individual faculty profile pages."""
    st, ci, inst, it = 'maharashtra', 'mumbai', 'IIT Bombay', 'IIT'
    base = 'https://www.cse.iitb.ac.in'
    url = f'{base}/people/faculty'
    html = get_html_js(url, wait_sel='a[href*="people"], .faculty')
    rows = []
    if not html:
        return rows
    s = soup(html)
    prof_links = []
    for a in s.find_all('a', href=True):
        href = a['href']
        if '/people/' in href or '/faculty/' in href or '/~' in href:
            full = urljoin(base, href)
            if full not in prof_links:
                prof_links.append(full)
    for link in prof_links[:80]:
        time.sleep(0.3)
        phtml, _ = get_html(session, link)
        if not phtml:
            continue
        emails = [e for e in find_emails(phtml) if 'iitb.ac.in' in e]
        if not emails:
            continue
        ps = soup(phtml)
        name_el = ps.find('h1') or ps.find('h2') or ps.find('title')
        name = clean(name_el.get_text()) if name_el else ''
        area = ''
        for tag in ps.find_all(['p', 'li', 'div']):
            txt = clean(tag.get_text())
            if re.search(r'research interest|area of research', txt, re.I):
                area = txt[:200]
                break
        for email in emails[:1]:
            rows.append(make_row(name, st, ci, inst, it, 'CSE',
                                 email, area, link))
    return rows

def scrape_iit_delhi(session):
    """IIT Delhi CSE – faculty list with individual profile links."""
    st, ci, inst, it = 'delhi', 'new-delhi', 'IIT Delhi', 'IIT'
    url = 'https://www.cse.iitd.ac.in/index.php/people/faculty'
    html = get_html_js(url, wait_sel='.faculty-info, .people-list, h3')
    rows = []
    if not html:
        html, _ = get_html(session, url)
    if not html:
        return rows
    s = soup(html)
    emails_in_page = [e for e in find_emails(html) if 'iitd.ac.in' in e]
    for email in emails_in_page:
        local = email.split('@')[0]
        # Find name near this email
        name_found = ''
        for el in s.find_all(string=re.compile(re.escape(local), re.I)):
            parent = el.find_parent(['tr', 'div', 'li', 'td'])
            if parent:
                hel = parent.find(['b', 'strong', 'h3', 'h4', 'a'])
                if hel:
                    name_found = clean(hel.get_text())
                    break
        if not name_found or not looks_like_name(name_found):
            name_found = local.replace('.', ' ').title()
        rows.append(make_row(name_found, st, ci, inst, it, 'CSE', email))
    return rows

def scrape_iit_madras(session):
    """IIT Madras CSE – faculty listing."""
    st, ci, inst, it = 'tamil-nadu', 'chennai', 'IIT Madras', 'IIT'
    urls = [
        'https://www.cse.iitm.ac.in/faculty.php',
        'https://www.cse.iitm.ac.in/people.php',
        'https://www.cse.iitm.ac.in/',
    ]
    rows = []
    for url in urls:
        html, _ = get_html(session, url)
        if not html:
            continue
        emails = [e for e in find_emails(html) if 'iitm.ac.in' in e
                  or 'cse.iitm' in e]
        if emails:
            s = soup(html)
            for email in emails:
                local = email.split('@')[0]
                name = local.replace('.', ' ').title()
                # Try to find actual name
                for el in s.find_all(string=re.compile(re.escape(local), re.I)):
                    parent = el.find_parent(['tr', 'div', 'li', 'td'])
                    if parent:
                        hel = parent.find(['b', 'strong', 'h3', 'a'])
                        if hel:
                            name = clean(hel.get_text())
                            break
                rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
            break
    if not rows:
        html = get_html_js('https://www.cse.iitm.ac.in/faculty.php')
        emails = [e for e in find_emails(html) if 'iitm.ac.in' in e]
        s = soup(html)
        for email in emails:
            local = email.split('@')[0]
            name = local.replace('.', ' ').title()
            rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
    return rows

def scrape_iit_kharagpur(session):
    """IIT Kharagpur CSE – JS-rendered."""
    st, ci, inst, it = 'west-bengal', 'kharagpur', 'IIT Kharagpur', 'IIT'
    url = 'https://cse.iitkgp.ac.in/faculty.html'
    html = get_html_js(url, wait_sel='.faculty, h3, table')
    rows = []
    if not html:
        html, _ = get_html(session, url)
    emails = [e for e in find_emails(html or '') if 'iitkgp.ac.in' in e]
    s = soup(html or '')
    for email in emails:
        local = email.split('@')[0]
        name = local.replace('.', ' ').title()
        for el in s.find_all(string=re.compile(re.escape(local), re.I)):
            parent = el.find_parent(['tr', 'div', 'li', 'td', 'article'])
            if parent:
                hel = parent.find(['b', 'strong', 'h3', 'h4', 'a'])
                if hel:
                    name = clean(hel.get_text())
                    break
        rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
    return rows

def scrape_nit_trichy(session):
    """NIT Trichy – follow each faculty profile link."""
    st, ci, inst, it = 'tamil-nadu', 'tiruchirappalli', 'NIT Trichy', 'NIT'
    return scrape_nitt_style(session,
        'https://www.nitt.edu/home/academics/departments/cse/faculty/',
        st, ci, inst, it)

def scrape_nit_warangal(session):
    """NIT Warangal CSE faculty."""
    st, ci, inst, it = 'telangana', 'warangal', 'NIT Warangal', 'NIT'
    rows = []
    url = 'https://nitw.ac.in/page/it/2/'
    html = get_html_js(url, wait_sel='.faculty, .card, table, h3')
    if not html:
        html, _ = get_html(session, url)
    emails = [e for e in find_emails(html or '') if 'nitw.ac.in' in e]
    s = soup(html or '')
    for email in emails:
        local = email.split('@')[0]
        name = local.replace('.', ' ').title()
        for el in s.find_all(string=re.compile(re.escape(local), re.I)):
            parent = el.find_parent(['tr', 'div', 'td', 'li'])
            if parent:
                hel = parent.find(['b', 'strong', 'h3', 'a', 'h4'])
                if hel:
                    name = clean(hel.get_text())
                    break
        rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
    return rows

def scrape_nit_surathkal(session):
    """NIT Surathkal CSE."""
    st, ci, inst, it = 'karnataka', 'surathkal', 'NIT Surathkal', 'NIT'
    urls = [
        'https://cse.nitk.ac.in/faculty',
        'https://nitk.edu.in/faculty/department/computer-science-and-engineering',
        'https://www.nitk.edu.in/departments/cse/faculty',
    ]
    rows = []
    for url in urls:
        html = get_html_js(url, wait_sel='.faculty, .card, table')
        if not html:
            html, _ = get_html(session, url)
        emails = [e for e in find_emails(html or '')
                  if 'nitk' in e and 'nitk.ac.in' in e]
        if emails:
            s = soup(html)
            for email in emails:
                local = email.split('@')[0]
                name = local.replace('.', ' ').title()
                for el in s.find_all(string=re.compile(re.escape(local), re.I)):
                    parent = el.find_parent(['tr', 'div', 'td', 'li'])
                    if parent:
                        hel = parent.find(['b', 'strong', 'h3', 'a'])
                        if hel:
                            name = clean(hel.get_text())
                            break
                rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
            break
    return rows

def scrape_nit_calicut(session):
    """NIT Calicut CSE faculty."""
    st, ci, inst, it = 'kerala', 'kozhikode', 'NIT Calicut', 'NIT'
    rows = []
    for url in [
        'https://minerva.nitc.ac.in/index.php/cse/faculty',
        'https://www.nitc.ac.in/index.php/component/content/article?id=52',
        'https://cse.nitc.ac.in/faculty/',
    ]:
        html, _ = get_html(session, url)
        if not html:
            continue
        emails = [e for e in find_emails(html) if 'nitc.ac.in' in e]
        if emails:
            s = soup(html)
            for email in emails:
                local = email.split('@')[0]
                name = local.replace('.', ' ').title()
                for el in s.find_all(string=re.compile(re.escape(local), re.I)):
                    parent = el.find_parent(['tr', 'div', 'td', 'li'])
                    if parent:
                        hel = parent.find(['b', 'strong', 'h3', 'a'])
                        if hel:
                            name = clean(hel.get_text())
                            break
                rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
            break
    return rows

def scrape_nit_rourkela(session):
    """NIT Rourkela CSE."""
    st, ci, inst, it = 'odisha', 'rourkela', 'NIT Rourkela', 'NIT'
    url = 'https://www.nitrkl.ac.in/CS/Faculty'
    html = get_html_js(url, wait_sel='table, .faculty, .card')
    if not html:
        html, _ = get_html(session, url)
    rows = scrape_email_grep(session, url, st, ci, inst, it,
                             'nitrkl.ac.in', use_js=False)
    return rows

def scrape_iiit_hyderabad(session):
    """IIIT Hyderabad faculty – JS-rendered."""
    st, ci, inst, it = 'telangana', 'hyderabad', 'IIIT Hyderabad', 'IIIT'
    url = 'https://www.iiit.ac.in/people/faculty/'
    html = get_html_js(url, wait_sel='.faculty-name, .people-card, h3')
    rows = []
    if not html:
        return rows
    s = soup(html)
    # IIIT-H uses cards with name + email obfuscated
    emails = [e for e in find_emails(html) if 'iiit.ac.in' in e]
    for email in emails:
        local = email.split('@')[0]
        name = local.replace('.', ' ').title()
        for el in s.find_all(string=re.compile(re.escape(local), re.I)):
            parent = el.find_parent(['div', 'li', 'td', 'article'])
            if parent:
                hel = parent.find(['h2', 'h3', 'h4', 'strong', 'b'])
                if hel:
                    name = clean(hel.get_text())
                    break
        # research area
        area = ''
        for el in s.find_all(string=re.compile(re.escape(local), re.I)):
            parent = el.find_parent(['div', 'li', 'td', 'article'])
            if parent:
                atag = parent.find(string=re.compile(r'research|interest', re.I))
                if atag:
                    ap = atag.find_parent(['p', 'div', 'li'])
                    area = clean(ap.get_text())[:200] if ap else ''
                break
        rows.append(make_row(name, st, ci, inst, it, 'CSE', email, area))
    return rows

def scrape_iiit_delhi(session):
    """IIIT Delhi CSE faculty – JS page."""
    st, ci, inst, it = 'delhi', 'new-delhi', 'IIIT Delhi', 'IIIT'
    url = 'https://www.iiitd.ac.in/cse/faculty'
    html = get_html_js(url, wait_sel='.faculty, .card, h3')
    rows = []
    if not html:
        return rows
    emails = [e for e in find_emails(html) if 'iiitd.ac.in' in e]
    s = soup(html)
    for email in emails:
        local = email.split('@')[0]
        name = local.replace('.', ' ').title()
        for el in s.find_all(string=re.compile(re.escape(local), re.I)):
            parent = el.find_parent(['div', 'li', 'td', 'article'])
            if parent:
                hel = parent.find(['h2', 'h3', 'h4', 'strong'])
                if hel:
                    name = clean(hel.get_text())
                    break
        rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
    return rows

def scrape_iiit_allahabad(session):
    """IIIT Allahabad IT/CSE faculty."""
    st, ci, inst, it = 'uttar-pradesh', 'prayagraj', 'IIIT Allahabad', 'IIIT'
    rows = []
    for url in [
        'https://www.iiita.ac.in/information-technology/',
        'https://profile.iiita.ac.in/listing/faculty',
        'https://www.iiita.ac.in/it-faculty/',
    ]:
        html, _ = get_html(session, url)
        if not html:
            continue
        emails = [e for e in find_emails(html) if 'iiita.ac.in' in e]
        if emails:
            s = soup(html)
            for email in emails:
                local = email.split('@')[0]
                name = local.replace('.', ' ').title()
                for el in s.find_all(string=re.compile(re.escape(local), re.I)):
                    parent = el.find_parent(['tr', 'div', 'td', 'li'])
                    if parent:
                        hel = parent.find(['b', 'strong', 'h3', 'a'])
                        if hel:
                            name = clean(hel.get_text())
                            break
                rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
            break
    return rows

def scrape_iiit_bangalore(session):
    """IIIT Bangalore faculty."""
    st, ci, inst, it = 'karnataka', 'bengaluru', 'IIIT Bangalore', 'IIIT'
    url = 'https://www.iiitb.ac.in/faculty'
    html = get_html_js(url, wait_sel='.faculty, .card, h3')
    rows = []
    if not html:
        html, _ = get_html(session, url)
    emails = [e for e in find_emails(html or '') if 'iiitb.ac.in' in e]
    s = soup(html or '')
    for email in emails:
        local = email.split('@')[0]
        name = local.replace('.', ' ').title()
        for el in s.find_all(string=re.compile(re.escape(local), re.I)):
            parent = el.find_parent(['div', 'li', 'td', 'article'])
            if parent:
                hel = parent.find(['h2', 'h3', 'h4', 'strong'])
                if hel:
                    name = clean(hel.get_text())
                    break
        rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
    return rows

def scrape_iit_roorkee(session):
    """IIT Roorkee CSE."""
    st, ci, inst, it = 'uttarakhand', 'roorkee', 'IIT Roorkee', 'IIT'
    rows = []
    for url in [
        'https://www.iitr.ac.in/departments/CSE/pages/People+Faculty.html',
        'https://faculty.iitr.ac.in/cs/',
        'https://www.iitr.ac.in/cse/pages/Faculty.html',
    ]:
        html, _ = get_html(session, url)
        if not html:
            continue
        emails = [e for e in find_emails(html) if 'iitr.ac.in' in e]
        if emails:
            s = soup(html)
            for email in emails:
                local = email.split('@')[0]
                name = local.replace('.', ' ').title()
                for el in s.find_all(string=re.compile(re.escape(local), re.I)):
                    parent = el.find_parent(['tr', 'div', 'td', 'li'])
                    if parent:
                        hel = parent.find(['b', 'strong', 'h3', 'a'])
                        if hel:
                            name = clean(hel.get_text())
                            break
                rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
            break
    return rows

def scrape_iit_hyderabad(session):
    """IIT Hyderabad CSE."""
    st, ci, inst, it = 'telangana', 'hyderabad', 'IIT Hyderabad', 'IIT'
    rows = []
    for url in [
        'https://cse.iith.ac.in/people/faculty.html',
        'https://www.iith.ac.in/cse/people/',
        'https://cse.iith.ac.in/faculty/',
    ]:
        html = get_html_js(url, wait_sel='.faculty, .card, h3')
        if not html:
            html, _ = get_html(session, url)
        emails = [e for e in find_emails(html or '')
                  if 'iith.ac.in' in e or 'cse.iith' in e]
        if emails:
            s = soup(html)
            for email in emails:
                local = email.split('@')[0]
                name = local.replace('.', ' ').title()
                for el in s.find_all(string=re.compile(re.escape(local), re.I)):
                    parent = el.find_parent(['tr', 'div', 'td', 'li'])
                    if parent:
                        hel = parent.find(['b', 'strong', 'h3', 'a'])
                        if hel:
                            name = clean(hel.get_text())
                            break
                rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
            break
    return rows

def scrape_iit_gandhinagar(session):
    """IIT Gandhinagar CSE."""
    st, ci, inst, it = 'gujarat', 'gandhinagar', 'IIT Gandhinagar', 'IIT'
    url = 'https://iitgn.ac.in/faculty/cse'
    html = get_html_js(url, wait_sel='.faculty, .card, h3, .people')
    rows = []
    if not html:
        html, _ = get_html(session, url)
    emails = [e for e in find_emails(html or '') if 'iitgn.ac.in' in e]
    s = soup(html or '')
    for email in emails:
        local = email.split('@')[0]
        name = local.replace('.', ' ').title()
        for el in s.find_all(string=re.compile(re.escape(local), re.I)):
            parent = el.find_parent(['div', 'li', 'td', 'article'])
            if parent:
                hel = parent.find(['h2', 'h3', 'h4', 'strong', 'b'])
                if hel:
                    name = clean(hel.get_text())
                    break
        rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
    return rows

def scrape_mnit_jaipur(session):
    st, ci, inst, it = 'rajasthan', 'jaipur', 'MNIT Jaipur', 'NIT'
    return scrape_email_grep(session,
        'https://mnit.ac.in/dept_cse/faculty',
        st, ci, inst, it, 'mnit.ac.in')

def scrape_mnnit_allahabad(session):
    st, ci, inst, it = 'uttar-pradesh', 'allahabad', 'MNNIT Allahabad', 'NIT'
    rows = []
    for url in [
        'https://www.mnnit.ac.in/index.php/department-of-cse/faculty',
        'https://www.mnnit.ac.in/index.php/academics/departments/computer-science-and-engineering',
    ]:
        html = get_html_js(url, wait_sel='.faculty, table, .card')
        if not html:
            html, _ = get_html(session, url)
        emails = [e for e in find_emails(html or '') if 'mnnit.ac.in' in e]
        if emails:
            s = soup(html)
            for email in emails:
                local = email.split('@')[0]
                name = local.replace('.', ' ').title()
                for el in s.find_all(string=re.compile(re.escape(local), re.I)):
                    parent = el.find_parent(['tr', 'div', 'td', 'li'])
                    if parent:
                        hel = parent.find(['b', 'strong', 'h3', 'a'])
                        if hel:
                            name = clean(hel.get_text())
                            break
                rows.append(make_row(name, st, ci, inst, it, 'CSE', email))
            break
    return rows

def scrape_nit_kurukshetra(session):
    st, ci, inst, it = 'haryana', 'kurukshetra', 'NIT Kurukshetra', 'NIT'
    return scrape_email_grep(session,
        'https://nitkkr.ac.in/faculty/cse',
        st, ci, inst, it, 'nitkkr.ac.in')

def scrape_svnit_surat(session):
    st, ci, inst, it = 'gujarat', 'surat', 'SVNIT Surat', 'NIT'
    return scrape_email_grep(session,
        'https://www.svnit.ac.in/web/department/cse/',
        st, ci, inst, it, 'svnit.ac.in')

def scrape_manit_bhopal(session):
    st, ci, inst, it = 'madhya-pradesh', 'bhopal', 'MANIT Bhopal', 'NIT'
    return scrape_email_grep(session,
        'https://www.manit.ac.in/content/faculty-computer-science',
        st, ci, inst, it, 'manit.ac.in')

def scrape_nit_durgapur(session):
    st, ci, inst, it = 'west-bengal', 'durgapur', 'NIT Durgapur', 'NIT'
    return scrape_email_grep(session,
        'https://nitdgp.ac.in/department/CS/faculty',
        st, ci, inst, it, 'nitdgp.ac.in')

def scrape_nit_jalandhar(session):
    st, ci, inst, it = 'punjab', 'jalandhar', 'NIT Jalandhar', 'NIT'
    return scrape_email_grep(session,
        'https://csed.nitj.ac.in/index.php/faculty',
        st, ci, inst, it, 'nitj.ac.in')

def scrape_nit_hamirpur(session):
    st, ci, inst, it = 'himachal-pradesh', 'hamirpur', 'NIT Hamirpur', 'NIT'
    return scrape_email_grep(session,
        'https://www.nith.ac.in/faculty/cse',
        st, ci, inst, it, 'nith.ac.in')

def scrape_nit_jamshedpur(session):
    st, ci, inst, it = 'jharkhand', 'jamshedpur', 'NIT Jamshedpur', 'NIT'
    return scrape_email_grep(session,
        'https://nitjsr.ac.in/backend/uploads/Faculty/cs',
        st, ci, inst, it, 'nitjsr.ac.in')

def scrape_iiit_gwalior(session):
    st, ci, inst, it = 'madhya-pradesh', 'gwalior', 'IIIT Gwalior', 'IIIT'
    return scrape_email_grep(session,
        'https://www.iiitm.ac.in/index.php/academics/faculty',
        st, ci, inst, it, 'iiitm.ac.in')

def scrape_iit_ropar(session):
    st, ci, inst, it = 'punjab', 'ropar', 'IIT Ropar', 'IIT'
    return scrape_email_grep(session,
        'https://www.iitrpr.ac.in/cse/faculty',
        st, ci, inst, it, 'iitrpr.ac.in')

def scrape_iit_mandi(session):
    st, ci, inst, it = 'himachal-pradesh', 'mandi', 'IIT Mandi', 'IIT'
    return scrape_email_grep(session,
        'https://www.iitmandi.ac.in/academics/faculty_list.php?dept=CS',
        st, ci, inst, it, 'iitmandi.ac.in')

def scrape_iit_jodhpur(session):
    st, ci, inst, it = 'rajasthan', 'jodhpur', 'IIT Jodhpur', 'IIT'
    return scrape_email_grep(session,
        'https://iitj.ac.in/department/index.php?id=cse',
        st, ci, inst, it, 'iitj.ac.in')

def scrape_iit_bhubaneswar(session):
    st, ci, inst, it = 'odisha', 'bhubaneswar', 'IIT Bhubaneswar', 'IIT'
    return scrape_email_grep(session,
        'https://www.iitbbs.ac.in/dept_cse.php',
        st, ci, inst, it, 'iitbbs.ac.in')

def scrape_iit_patna(session):
    st, ci, inst, it = 'bihar', 'patna', 'IIT Patna', 'IIT'
    return scrape_email_grep(session,
        'https://www.iitp.ac.in/~cse/faculty.html',
        st, ci, inst, it, 'iitp.ac.in')

def scrape_iit_tirupati(session):
    st, ci, inst, it = 'andhra-pradesh', 'tirupati', 'IIT Tirupati', 'IIT'
    return scrape_email_grep(session,
        'https://www.iittp.ac.in/faculty',
        st, ci, inst, it, 'iittp.ac.in')

def scrape_iit_dharwad(session):
    st, ci, inst, it = 'karnataka', 'dharwad', 'IIT Dharwad', 'IIT'
    return scrape_email_grep(session,
        'https://www.iitdh.ac.in/faculty',
        st, ci, inst, it, 'iitdh.ac.in')

def scrape_iit_bhilai(session):
    st, ci, inst, it = 'chhattisgarh', 'raipur', 'IIT Bhilai', 'IIT'
    return scrape_email_grep(session,
        'https://www.iitbhilai.ac.in/index.php?pid=cse_faculty',
        st, ci, inst, it, 'iitbhilai.ac.in')

def scrape_iit_palakkad(session):
    st, ci, inst, it = 'kerala', 'palakkad', 'IIT Palakkad', 'IIT'
    return scrape_email_grep(session,
        'https://iitpkd.ac.in/people',
        st, ci, inst, it, 'iitpkd.ac.in')

def scrape_iit_jammu(session):
    st, ci, inst, it = 'jammu-kashmir', 'jammu', 'IIT Jammu', 'IIT'
    return scrape_email_grep(session,
        'https://www.iitjammu.ac.in/academics/departments/cse/faculty',
        st, ci, inst, it, 'iitjammu.ac.in')

def scrape_iit_goa(session):
    st, ci, inst, it = 'goa', 'ponda', 'IIT Goa', 'IIT'
    return scrape_email_grep(session,
        'https://www.iitgoa.ac.in/faculty',
        st, ci, inst, it, 'iitgoa.ac.in')

# ── SCRAPERS registry ────────────────────────────────────────────────────────
# Maps relative CSV key -> (scraper_fn, csv_path)
# CSV path relative to FAC_DIR

SCRAPERS = {
    # IITs
    'iits/maharashtra/mumbai/iit-bombay':          scrape_iit_bombay,
    'iits/delhi/new-delhi/iit-delhi':               scrape_iit_delhi,
    'iits/tamil-nadu/chennai/iit-madras':           scrape_iit_madras,
    'iits/uttar-pradesh/kanpur/iit-kanpur':         scrape_iit_kanpur,
    'iits/west-bengal/kharagpur/iit-kharagpur':     scrape_iit_kharagpur,
    'iits/assam/guwahati/iit-guwahati':             scrape_iit_guwahati,
    'iits/uttarakhand/roorkee/iit-roorkee':         scrape_iit_roorkee,
    'iits/telangana/hyderabad/iit-hyderabad':       scrape_iit_hyderabad,
    'iits/gujarat/gandhinagar/iit-gandhinagar':     scrape_iit_gandhinagar,
    'iits/rajasthan/jodhpur/iit-jodhpur':           scrape_iit_jodhpur,
    'iits/punjab/ropar/iit-ropar':                  scrape_iit_ropar,
    'iits/himachal-pradesh/mandi/iit-mandi':        scrape_iit_mandi,
    'iits/odisha/bhubaneswar/iit-bhubaneswar':      scrape_iit_bhubaneswar,
    'iits/bihar/patna/iit-patna':                   scrape_iit_patna,
    'iits/chhattisgarh/raipur/iit-bhilai':          scrape_iit_bhilai,
    'iits/goa/ponda/iit-goa':                       scrape_iit_goa,
    'iits/karnataka/dharwad/iit-dharwad':           scrape_iit_dharwad,
    'iits/jammu-kashmir/jammu/iit-jammu':           scrape_iit_jammu,
    'iits/andhra-pradesh/tirupati/iit-tirupati':    scrape_iit_tirupati,
    'iits/kerala/palakkad/iit-palakkad':            scrape_iit_palakkad,
    # NITs
    'nits/tamil-nadu/tiruchirappalli/nit-trichy':   scrape_nit_trichy,
    'nits/telangana/warangal/nit-warangal':         scrape_nit_warangal,
    'nits/odisha/rourkela/nit-rourkela':            scrape_nit_rourkela,
    'nits/kerala/kozhikode/nit-calicut':            scrape_nit_calicut,
    'nits/karnataka/surathkal/nit-surathkal':       scrape_nit_surathkal,
    'nits/west-bengal/durgapur/nit-durgapur':       scrape_nit_durgapur,
    'nits/madhya-pradesh/bhopal/manit-bhopal':      scrape_manit_bhopal,
    'nits/uttar-pradesh/allahabad/mnnit-allahabad': scrape_mnnit_allahabad,
    'nits/rajasthan/jaipur/mnit-jaipur':            scrape_mnit_jaipur,
    'nits/gujarat/surat/svnit-surat':               scrape_svnit_surat,
    'nits/haryana/kurukshetra/nit-kurukshetra':     scrape_nit_kurukshetra,
    'nits/himachal-pradesh/hamirpur/nit-hamirpur':  scrape_nit_hamirpur,
    'nits/punjab/jalandhar/nit-jalandhar':          scrape_nit_jalandhar,
    'nits/jharkhand/jamshedpur/nit-jamshedpur':     scrape_nit_jamshedpur,
    # IIITs
    'iiits/telangana/hyderabad/iiit-hyderabad':     scrape_iiit_hyderabad,
    'iiits/delhi/new-delhi/iiit-delhi':             scrape_iiit_delhi,
    'iiits/uttar-pradesh/prayagraj/iiit-allahabad': scrape_iiit_allahabad,
    'iiits/karnataka/bengaluru/iiit-bangalore':     scrape_iiit_bangalore,
    'iiits/madhya-pradesh/gwalior/iiit-gwalior':    scrape_iiit_gwalior,
}

# ── rebuild master ───────────────────────────────────────────────────────────

def rebuild_master():
    all_rows = []
    seen_emails = set()
    for dirpath, _, files in os.walk(FAC_DIR):
        for fn in sorted(files):
            if fn.endswith('.csv'):
                fp = os.path.join(dirpath, fn)
                with open(fp, encoding='utf-8', newline='') as f:
                    for r in csv.DictReader(f):
                        email = r.get('email', '').strip().lower()
                        if email and email in seen_emails:
                            continue
                        if email:
                            seen_emails.add(email)
                        # Ensure all header fields present
                        row = {k: r.get(k, '') for k in HEADER}
                        all_rows.append(row)
    with open(MASTER, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(all_rows)
    print(f"  faculty_master.csv rebuilt: {len(all_rows)} rows")
    return len(all_rows)

# ── main ─────────────────────────────────────────────────────────────────────

def main():
    dry_run = '--dry-run' in sys.argv
    filter_name = next((a for a in sys.argv[1:] if not a.startswith('--')), None)

    session = make_session()
    total_new = 0

    targets = {k: v for k, v in SCRAPERS.items()
               if not filter_name or filter_name in k}
    if not targets:
        print(f"No scrapers matched '{filter_name}'. Available:")
        for k in SCRAPERS:
            print(f"  {k}")
        return

    for key, scraper_fn in targets.items():
        parts = key.split('/')
        csv_rel = key + '.csv'
        csv_path = os.path.join(FAC_DIR, *csv_rel.split('/'))
        existing = load_existing_emails(csv_path)

        print(f"\n[{parts[-1]}] scraping ...")
        try:
            rows = scraper_fn(session)
        except Exception as e:
            print(f"  ERROR: {e}")
            rows = []

        if not rows:
            print(f"  no rows returned")
            continue

        # deduplicate against existing
        new_rows = []
        seen_this_run = set()
        for r in rows:
            email = r.get('email', '').lower().strip()
            if not email:
                continue
            if email in existing or email in seen_this_run:
                continue
            seen_this_run.add(email)
            new_rows.append(r)

        print(f"  {len(rows)} scraped, {len(new_rows)} new (skipped {len(rows)-len(new_rows)} duplicates)")

        if dry_run:
            for r in new_rows:
                print(f"    {r['name']!r:40s} {r['email']}")
        else:
            if new_rows:
                append_rows(csv_path, new_rows)
                total_new += len(new_rows)
                print(f"  -> wrote {len(new_rows)} rows to {os.path.relpath(csv_path, ROOT)}")

    if not dry_run:
        print(f"\n=== rebuilding faculty_master.csv ===")
        total = rebuild_master()
        print(f"\nDone. Added {total_new} new rows across all institutes. "
              f"Master total: {total}")
    else:
        print(f"\n[dry-run] would have written {total_new} new rows")

    close_browser()

if __name__ == '__main__':
    main()
