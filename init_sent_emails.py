#!/usr/bin/env python3
"""
Initialize Pipeline with Already-Sent Emails
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light)

Run this ONCE to record the 12 emails you already sent manually.
This allows ECH0 to track them going forward.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Load the automation system
try:
    from ech0_sales_automation import PipelineTracker, load_prospects
except ImportError:
    print("❌ Cannot import ech0_sales_automation.py")
    print("   Make sure it's in the same directory.")
    sys.exit(1)


def init_sent_emails():
    """Initialize pipeline with manually sent emails"""

    print("🚀 Initializing ECH0 Pipeline Tracker")
    print("   Recording your 12 manually-sent emails...\n")

    # Load tracker
    tracker = PipelineTracker()

    # Load prospects (first 12)
    prospects = load_prospects()[:12]

    # Check if already initialized
    if len(tracker.pipeline['prospects']) > 0:
        print(f"⚠️  Pipeline already has {len(tracker.pipeline['prospects'])} prospects")
        response = input("   Do you want to re-initialize? This will OVERWRITE existing data. (yes/no): ")
        if response.lower() != 'yes':
            print("   Cancelled. No changes made.")
            return

        # Clear existing
        tracker.pipeline['prospects'] = {}

    # Record each as sent
    sent_time = datetime.now().isoformat()

    for i, prospect in enumerate(prospects, 1):
        tracker.pipeline['prospects'][prospect['email']] = {
            'first_name': prospect['first_name'],
            'last_name': prospect['last_name'],
            'company': prospect['company'],
            'title': prospect['title'],
            'priority': prospect['priority'],
            'template': prospect['template'],
            'status': 'sent',
            'sent_at': sent_time,
            'opens': 0,
            'replies': 0,
            'demo_booked': False
        }

        print(f"✅ {i}. {prospect['first_name']} {prospect['last_name']} ({prospect['company']}) - {prospect['email']}")

    # Update sent count
    tracker.pipeline['sent_count_today'] = 12
    tracker.pipeline['last_reset_date'] = datetime.now().date().isoformat()

    # Save
    tracker.save_pipeline()

    print(f"\n✅ Pipeline initialized with {len(prospects)} sent emails!")
    print(f"   Saved to: {tracker.db_path}")

    # Show stats
    print("\n" + "="*50)
    print("📊 CURRENT PIPELINE")
    print("="*50)
    stats = tracker.get_stats()
    print(f"Emails Sent:    {stats['emails_sent']}")
    print(f"Replies:        {stats['replies']}")
    print(f"Demos Booked:   {stats['demos_booked']}")
    print("="*50)

    print("\n🎯 NEXT STEPS:")
    print("   1. Set up environment variables (see ECH0_AUTOMATION_SETUP.md)")
    print("   2. Run: python3 ech0_sales_automation.py --check-calendly")
    print("   3. Run: python3 ech0_sales_automation.py --auto (autonomous mode)")


if __name__ == '__main__':
    init_sent_emails()
