#!/usr/bin/env python3
"""
enrich_yc_js.py - JS-rendering email enrichment for the YC company master list.

Renders each company's own site with headless Chromium (so emails injected by
JavaScript are visible), extracts addresses that live on the company's OWN
domain, and writes one best role-inbox per company in the batch schema
(Company,Email,Person,Title,Notes).

Why this exists: the plain HTML fetch only sees ~5% of sites; a rendered pass
gets ~4-5x more, but naively firing 700+ renders at once wedges the browser.
This version is built to run start-to-finish on a real machine:

  * bounded worker pool (a fixed number of tabs, fed from a queue - never
    hundreds of coroutines at once)
  * a fresh browser every CHUNK sites, so memory/handles can't pile up
  * a fresh context per site (no cookie/state carryover), always closed
  * hard per-navigation timeouts and image/font/css blocking for speed
  * resumable: every attempted company is logged to <out>.processed, so if you
    stop it (Ctrl+C) or it dies, just run it again and it picks up where it left

Setup (once):
    python -m venv .venv && . .venv/bin/activate    # Windows: .venv\\Scripts\\activate
    pip install playwright
    python -m playwright install chromium

Run (from the repo root):
    python scripts/enrich_yc_js.py \\
        --input industry/yc_companies.csv \\
        --out industry/batches/yc_js_enriched.csv \\
        --skip industry/batches/batch_145.csv \\
        --concurrency 8

Then review the output CSV and, when happy, use it with mailer/send.py
(dry-run first, then --send).
"""
from __future__ import annotations

import argparse
import asyncio
import csv
import re
import sys
import urllib.parse
from pathlib import Path

from playwright.async_api import async_playwright

# --- tunables -------------------------------------------------------------
PATHS = ("", "/contact", "/careers", "/about")   # pages checked per company
NAV_TIMEOUT_MS = 15000        # per navigation
SETTLE_MS = 1500              # let JS inject content after DOM load
DEFAULT_CONCURRENCY = 8       # tabs in flight at once
CHUNK = 120                   # recycle the whole browser every this many sites
BLOCK = {"image", "media", "font", "stylesheet"}

EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
ROLE = (
    "careers", "jobs", "hiring", "hire", "hello", "hi", "hey", "contact",
    "team", "info", "founders", "founder", "join", "work", "people",
    "talent", "recruit",
)
GENERIC = ("sales", "support")   # accepted but ranked low for job outreach
JUNK = re.compile(
    r"(sentry|wixpress|\.png|\.jpg|\.jpeg|\.svg|\.gif|\.webp|@2x|example\.|"
    r"yourname|your-email|domain\.com|test@|godaddy|cloudflare|wordpress|"
    r"squarespace|w3\.org|schema\.org|@email\.)",
    re.I,
)


def reg_domain(host: str) -> str:
    host = host.lower().split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def role_rank(local: str) -> int:
    if local.startswith("founder"):
        return 0
    if local.startswith(("career", "job", "hiring", "hire", "join", "recruit", "talent", "people", "work")):
        return 1
    if local.startswith(("hello", "hi", "hey", "contact", "team")):
        return 2
    if local.startswith("info"):
        return 3
    if local.startswith(GENERIC):
        return 4
    return 3


def person_for(local: str) -> str:
    if local.startswith("founder"):
        return "Founders"
    if local.startswith(("career", "job", "hiring", "hire", "join", "recruit", "talent", "people", "work")):
        return "Hiring Team"
    if local.startswith(GENERIC):
        return "General inbox"
    return "Team"


async def _block(route):
    try:
        if route.request.resource_type in BLOCK:
            await route.abort()
        else:
            await route.continue_()
    except Exception:
        pass


async def scrape_one(browser, row: dict) -> str | None:
    """Return the best on-domain email for one company, or None."""
    site = (row.get("Website") or "").strip()
    if not site:
        return None
    pu = urllib.parse.urlparse(site if "://" in site else "https://" + site)
    if not pu.netloc:
        return None
    dom = reg_domain(pu.netloc)
    base = f"{pu.scheme or 'https'}://{pu.netloc}"

    ctx = await browser.new_context(user_agent="Mozilla/5.0 (contact-lookup)")
    found: dict[str, int] = {}
    try:
        page = await ctx.new_page()
        await page.route("**/*", _block)
        for path in PATHS:
            try:
                await page.goto(base + path, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
                await page.wait_for_timeout(SETTLE_MS)
                html = await page.content()
                try:
                    mailtos = await page.eval_on_selector_all(
                        'a[href^="mailto:"]', "els => els.map(e => e.getAttribute('href'))"
                    )
                except Exception:
                    mailtos = []
                blob = html + " " + " ".join(m or "" for m in mailtos)
                for m in EMAIL.findall(blob):
                    e = m.lower().strip(".").replace("mailto:", "")
                    if JUNK.search(e):
                        continue
                    edom = e.split("@", 1)[1]
                    if edom == dom or edom.endswith("." + dom):
                        found[e] = min(found.get(e, 9), role_rank(e.split("@", 1)[0]))
            except Exception:
                pass
            if any(v == 0 for v in found.values()):   # a founders@ is as good as it gets
                break
    finally:
        try:
            await ctx.close()
        except Exception:
            pass
    if not found:
        return None
    return sorted(found, key=lambda e: (found[e], len(e)))[0]


async def worker(name, browser, queue, results, processed_fp, out_writer, out_fp, lock, meta_note):
    while True:
        row = await queue.get()
        try:
            email = await scrape_one(browser, row)
        except Exception:
            email = None
        finally:
            company = row["Company"]
            async with lock:
                processed_fp.write(company + "\n")
                processed_fp.flush()
                if email:
                    out_writer.writerow([company, email, person_for(email.split("@", 1)[0]),
                                         "—", meta_note(row)])
                    out_fp.flush()
                    results["hit"] += 1
                results["done"] += 1
                if results["done"] % 25 == 0:
                    print(f"  {results['done']}/{results['total']}  hits={results['hit']}", flush=True)
            queue.task_done()


def meta_note(row: dict) -> str:
    note = f"YC {row.get('Batch','')} · {row.get('Vertical','')}"
    if (row.get("Hiring") or "").lower() == "yes":
        note += " · hiring"
    return note + " · cold email for opportunity; ask to forward to hiring manager"


def load_names(path: Path, col: str = "Company") -> set:
    names = set()
    if path and path.exists():
        with path.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r.get(col):
                    names.add(r[col].strip())
    return names


async def run(args):
    inp = Path(args.input)
    out = Path(args.out)
    processed_path = out.with_suffix(out.suffix + ".processed")

    all_rows = list(csv.DictReader(inp.open(encoding="utf-8", newline="")))
    already = load_names(Path(args.skip)) if args.skip else set()
    if processed_path.exists():
        already |= {ln.strip() for ln in processed_path.read_text(encoding="utf-8").splitlines() if ln.strip()}
    pending = [r for r in all_rows if r.get("Company") and r["Company"].strip() not in already]
    if args.limit:
        pending = pending[: args.limit]
    print(f"input={len(all_rows)}  already done/skipped={len(already)}  to process={len(pending)}", flush=True)
    if not pending:
        print("nothing to do.")
        return

    out_is_new = not out.exists()
    out_fp = out.open("a", encoding="utf-8", newline="")
    out_writer = csv.writer(out_fp)
    if out_is_new:
        out_writer.writerow(["Company", "Email", "Person", "Title", "Notes"])
        out_fp.flush()
    processed_fp = processed_path.open("a", encoding="utf-8")
    lock = asyncio.Lock()
    results = {"done": 0, "hit": 0, "total": len(pending)}

    async with async_playwright() as p:
        for i in range(0, len(pending), CHUNK):
            chunk = pending[i : i + CHUNK]
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
            try:
                queue: asyncio.Queue = asyncio.Queue()
                for row in chunk:
                    queue.put_nowait(row)
                workers = [
                    asyncio.create_task(
                        worker(w, browser, queue, results, processed_fp, out_writer, out_fp, lock, meta_note)
                    )
                    for w in range(args.concurrency)
                ]
                await queue.join()
                for wk in workers:
                    wk.cancel()
                await asyncio.gather(*workers, return_exceptions=True)
            finally:
                await browser.close()   # recycle the browser between chunks
            print(f"[chunk {i // CHUNK + 1}] browser recycled  ({results['done']}/{results['total']}, hits={results['hit']})", flush=True)

    out_fp.close()
    processed_fp.close()
    print(f"DONE. processed={results['done']}  emails found={results['hit']}  ->  {out}", flush=True)


def main():
    ap = argparse.ArgumentParser(description="JS-rendering YC email enrichment (resumable).")
    ap.add_argument("--input", default="industry/yc_companies.csv", help="master CSV (needs Company,Website,Batch,Vertical,Hiring columns)")
    ap.add_argument("--out", default="industry/batches/yc_js_enriched.csv", help="output batch CSV (appended; resumable)")
    ap.add_argument("--skip", default="", help="optional CSV of companies already done (skipped by Company name)")
    ap.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY, help="tabs in flight (default 8)")
    ap.add_argument("--limit", type=int, default=0, help="cap number of companies this run (0 = all)")
    args = ap.parse_args()
    try:
        asyncio.run(run(args))
    except KeyboardInterrupt:
        print("\ninterrupted - progress saved to the .processed log; re-run to resume.", file=sys.stderr)


if __name__ == "__main__":
    main()
