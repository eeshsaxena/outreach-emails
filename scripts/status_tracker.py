#!/usr/bin/env python3
"""
status_tracker.py — Track outreach campaign status across research & industry.

Shows live stats: total contacts, sent, replied, accepted, bounced, queued.

Usage:
    python scripts/status_tracker.py               # show current status
    python scripts/status_tracker.py --update      # interactive status update CLI
    python scripts/status_tracker.py --bounce <email>  # mark email as bounced
    python scripts/status_tracker.py --set <email> <status>  # set status for one email
"""

import csv
import os
import sys
from collections import Counter

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.dirname(HERE)
MASTER_RESEARCH = os.path.join(ROOT, "research", "faculty_master.csv")
MASTER_INDUSTRY = os.path.join(ROOT, "industry", "all_emails.csv")
DEAD_RESEARCH   = os.path.join(ROOT, "research", "dead_removed.csv")
DEAD_INDUSTRY   = os.path.join(ROOT, "industry", "dead_removed.csv")

HEADER_RESEARCH = [
    "name", "state", "city", "institute", "institute_type",
    "department", "email", "research_area", "personal_site",
    "priority", "status", "notes",
]
HEADER_INDUSTRY = [
    "Company", "Email", "Person", "Title", "Notes"
]

VALID_STATUSES = {
    "queued", "sent", "emailed", "follow-up-1", "follow-up-2",
    "replied", "responded", "accepted", "rejected", "no-response", "bounced"
}


def load_research():
    if not os.path.exists(MASTER_RESEARCH):
        return []
    with open(MASTER_RESEARCH, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_industry():
    if not os.path.exists(MASTER_INDUSTRY):
        return []
    with open(MASTER_INDUSTRY, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save_research(rows):
    with open(MASTER_RESEARCH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER_RESEARCH)
        w.writeheader()
        w.writerows(rows)


def save_industry(rows):
    with open(MASTER_INDUSTRY, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER_INDUSTRY)
        w.writeheader()
        w.writerows(rows)


def show_stats():
    """Display campaign stats for both tracks."""
    print("="*70)
    print("OUTREACH CAMPAIGN STATUS")
    print("="*70)
    
    # Research track
    rrows = load_research()
    if rrows:
        print("\n🎓 RESEARCH TRACK (faculty outreach)")
        print("-" * 70)
        statuses = Counter(r.get("status", "").strip().lower() for r in rrows)
        total = len(rrows)
        print(f"  Total contacts   : {total:,}")
        print(f"  Queued           : {statuses.get('queued', 0):,}")
        print(f"  Sent/Emailed     : {statuses.get('sent', 0) + statuses.get('emailed', 0):,}")
        print(f"  Follow-up 1      : {statuses.get('follow-up-1', 0):,}")
        print(f"  Follow-up 2      : {statuses.get('follow-up-2', 0):,}")
        print(f"  Replied          : {statuses.get('replied', 0) + statuses.get('responded', 0):,}")
        print(f"  Accepted         : {statuses.get('accepted', 0):,}")
        print(f"  Rejected         : {statuses.get('rejected', 0):,}")
        print(f"  No response      : {statuses.get('no-response', 0):,}")
        print(f"  Bounced          : {statuses.get('bounced', 0):,}")
        
        # By institute type
        by_type = Counter(r.get("institute_type", "") for r in rrows)
        print(f"\n  By type:")
        for itype in sorted(by_type, key=lambda x: -by_type[x]):
            print(f"    {itype:10s} : {by_type[itype]:,}")
    
    # Industry track (no native status column, just show total)
    irows = load_industry()
    if irows:
        print("\n💼 INDUSTRY TRACK (company outreach)")
        print("-" * 70)
        print(f"  Total contacts   : {len(irows):,}")
        print(f"  (Track status manually in external sheet / CRM)")
    
    # Dead/bounced summary
    if os.path.exists(DEAD_RESEARCH):
        with open(DEAD_RESEARCH, encoding="utf-8", newline="") as f:
            dead_r = sum(1 for _ in csv.DictReader(f))
    else:
        dead_r = 0
    if os.path.exists(DEAD_INDUSTRY):
        with open(DEAD_INDUSTRY, encoding="utf-8", newline="") as f:
            dead_i = sum(1 for _ in csv.DictReader(f))
    else:
        dead_i = 0
    
    if dead_r or dead_i:
        print(f"\n❌ DEAD/BOUNCED EMAILS")
        print("-" * 70)
        print(f"  Research : {dead_r:,}")
        print(f"  Industry : {dead_i:,}")
    
    print("\n" + "="*70)


def mark_bounced(email):
    """Move a bounced email from master to dead_removed."""
    email = email.strip().lower()
    rrows = load_research()
    found = False
    kept = []
    moved = None
    for r in rrows:
        if r.get("email", "").strip().lower() == email:
            moved = r
            found = True
        else:
            kept.append(r)
    
    if found:
        save_research(kept)
        # Append to dead_removed
        os.makedirs(os.path.dirname(DEAD_RESEARCH), exist_ok=True)
        write_header = not os.path.exists(DEAD_RESEARCH)
        with open(DEAD_RESEARCH, "a", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=HEADER_RESEARCH)
            if write_header:
                w.writeheader()
            w.writerow(moved)
        print(f"✓ Moved {email} to research/dead_removed.csv")
        return
    
    print(f"✗ Email {email} not found in research master")


def set_status(email, status):
    """Update status for a research faculty email."""
    email = email.strip().lower()
    status = status.strip().lower()
    if status not in VALID_STATUSES:
        print(f"✗ Invalid status '{status}'. Valid: {', '.join(sorted(VALID_STATUSES))}")
        return
    
    rrows = load_research()
    found = False
    for r in rrows:
        if r.get("email", "").strip().lower() == email:
            old = r.get("status", "")
            r["status"] = status
            found = True
            print(f"✓ Updated {email}: {old} → {status}")
            break
    
    if found:
        save_research(rrows)
    else:
        print(f"✗ Email {email} not found in research master")


def main():
    args = sys.argv[1:]
    
    if not args:
        show_stats()
        return
    
    cmd = args[0]
    
    if cmd == "--bounce" and len(args) == 2:
        mark_bounced(args[1])
    elif cmd == "--set" and len(args) == 3:
        set_status(args[1], args[2])
    elif cmd == "--update":
        print("Interactive status update (TODO: implement batch CSV upload)")
        print("For now, edit research/faculty_master.csv directly.")
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
