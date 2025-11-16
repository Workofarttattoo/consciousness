#!/usr/bin/env python3
"""
Reddit Campaign Scheduler - Auto-post when rate limits expire
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Automatically posts remaining Reddit campaigns respecting rate limits.
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Reddit credentials
os.environ['REDDIT_CLIENT_ID'] = "i1-mWB8wA8vmSBCJhHHsCA"
os.environ['REDDIT_CLIENT_SECRET'] = "psWArY_EMufMuReXmiqMfzUpVZU40Q"
os.environ['REDDIT_USERNAME'] = "AllGoodBusiness"
os.environ['REDDIT_PASSWORD'] = "F00lpr00f596!"
os.environ['REDDIT_USER_AGENT'] = "ECH0-Bot/1.0 by /u/AllGoodBusiness"

ANALYTICS_FILE = Path(__file__).parent / "social_analytics.json"
HOURS_BETWEEN_POSTS = 8

def get_last_post_time():
    """Get timestamp of last Reddit post"""
    if not ANALYTICS_FILE.exists():
        return None

    with open(ANALYTICS_FILE, 'r') as f:
        data = json.load(f)

    if not data.get('posts'):
        return None

    last_post = data['posts'][-1]
    return datetime.fromisoformat(last_post['timestamp'])

def hours_until_next_post():
    """Calculate hours until next post is allowed"""
    last_post = get_last_post_time()

    if last_post is None:
        return 0

    now = datetime.now()
    next_allowed = last_post + timedelta(hours=HOURS_BETWEEN_POSTS)
    delta = next_allowed - now

    hours = delta.total_seconds() / 3600
    return max(0, hours)

def post_campaign(campaign_name):
    """Post a Reddit campaign"""
    print(f"\n🚀 Posting {campaign_name} campaign...")

    cmd = [
        'python3',
        'social_media_automation.py',
        '--reddit-campaign',
        campaign_name
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)

    return result.returncode == 0

def schedule_remaining_posts():
    """Schedule and post remaining campaigns"""

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║           🤖 Reddit Campaign Scheduler - ECH0                ║")
    print("║                                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    # Queue of campaigns to post
    campaigns = ['quantum', 'gavl']

    for i, campaign in enumerate(campaigns, 1):
        # Check if we need to wait
        wait_hours = hours_until_next_post()

        if wait_hours > 0:
            print(f"⏰ Waiting {wait_hours:.1f} hours until next post...")
            print(f"   Next post at: {(datetime.now() + timedelta(hours=wait_hours)).strftime('%I:%M %p')}")
            print(f"   Campaign: {campaign.upper()}")
            print()

            # Sleep until allowed
            time.sleep(wait_hours * 3600)

        # Post campaign
        print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"   POST {i}/{len(campaigns)}: {campaign.upper()}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        success = post_campaign(campaign)

        if success:
            print(f"✅ {campaign.upper()} campaign posted successfully")
        else:
            print(f"⚠️  {campaign.upper()} campaign had issues (check output above)")

        print()

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║              ✅ ALL CAMPAIGNS POSTED                          ║")
    print("║                                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")

def show_status():
    """Show current campaign status"""
    last_post = get_last_post_time()
    wait_hours = hours_until_next_post()

    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║           📊 REDDIT CAMPAIGN STATUS                          ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    if last_post:
        print(f"Last post: {last_post.strftime('%I:%M %p on %b %d')}")

        if wait_hours > 0:
            next_time = datetime.now() + timedelta(hours=wait_hours)
            print(f"Next post: {next_time.strftime('%I:%M %p on %b %d')}")
            print(f"Wait time: {wait_hours:.1f} hours")
        else:
            print(f"Next post: READY NOW")
    else:
        print("No posts yet - ready to post")

    print()

    # Show queued campaigns
    if ANALYTICS_FILE.exists():
        with open(ANALYTICS_FILE, 'r') as f:
            data = json.load(f)

        posts_today = sum(1 for p in data.get('posts', [])
                         if p['timestamp'].startswith(datetime.now().date().isoformat()))

        print(f"Posts today: {posts_today}/3")
        print(f"Remaining: {3 - posts_today} posts available")

    print()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Reddit Campaign Scheduler")
    parser.add_argument('--status', action='store_true', help='Show current status')
    parser.add_argument('--schedule', action='store_true', help='Schedule remaining posts (runs in background)')
    parser.add_argument('--post-now', choices=['quantum', 'gavl', 'both'], help='Force post now (ignores rate limits)')

    args = parser.parse_args()

    if args.status:
        show_status()

    elif args.schedule:
        print("Starting scheduled posting...")
        print("This will run in the background and post when rate limits allow.")
        print()
        schedule_remaining_posts()

    elif args.post_now:
        wait_hours = hours_until_next_post()
        if wait_hours > 0:
            print(f"⚠️  Rate limit active: {wait_hours:.1f} hours remaining")
            print(f"   Override with --force to post anyway (NOT recommended)")
        else:
            post_campaign(args.post_now)

    else:
        parser.print_help()
        print()
        show_status()
