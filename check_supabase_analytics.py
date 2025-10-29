#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Supabase Analytics Checker - Get Real Visitor & Sign-up Numbers
"""

import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

# ANSI colors for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Supabase project configurations
PROJECTS = {
    "aios.is (Main BBB)": {
        "url": "https://cszoklkfdszqsxhufhhj.supabase.co",
        "key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNzem9rbGtmZHN6cXN4aHVmaGhqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjExNzI0MzAsImV4cCI6MjA3Njc0ODQzMH0.HdqXrWVTPCQ2NYH-5ED_nx91a38UGPvTHjva4NzBG8I",
        "tables": ["page_visitors", "users", "signups", "page_views", "analytics"]
    },
    "Red Team Tools": {
        "url": "https://trokobwiphidmrmhwkni.supabase.co",
        "key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRyb2tvYndpcGhpZG1ybWh3a25pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NTk4MTQsImV4cCI6MjA3NjIzNTgxNH0.D1iTVxtL481Tk6Jr7qSInjOOCZhWmuHT8g-cE_ZT-dM",
        "tables": ["users", "signups", "page_visitors", "page_views", "tool_usage"]
    },
    "GAVL (thegavl.com)": {
        "url": "https://urqlitnxxszwmeoscpxk.supabase.co",
        "key": "sb_publishable_--8-yYBdROQjzK0GWRKKvA__RpkIkoC",
        "tables": ["page_visitors", "users", "signups", "consultations", "leads"]
    },
    "aios.is (Deployed Site)": {
        "url": "https://ttvgdswfhiqlazqpfkny.supabase.co",
        "key": "NEEDS_API_KEY",  # Found in index.html but key not visible
        "tables": ["page_visitors", "page_views"]
    }
}

def query_table(project_url, api_key, table_name):
    """Query a Supabase table and return row count and sample data"""
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        # Get all rows (with limit)
        response = requests.get(
            f"{project_url}/rest/v1/{table_name}?select=*&limit=1000",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "count": len(data),
                "data": data[:5],  # Sample of first 5 rows
                "status": response.status_code
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "error": "Table does not exist",
                "status": 404
            }
        elif response.status_code == 401:
            return {
                "success": False,
                "error": "Authentication failed - check API key",
                "status": 401
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text[:100]}",
                "status": response.status_code
            }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timeout",
            "status": -1
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "status": -1
        }

def analyze_visitors(data):
    """Analyze visitor data by date"""
    if not data:
        return {}

    by_date = defaultdict(int)
    by_page = defaultdict(int)

    for row in data:
        # Try different timestamp field names
        timestamp = row.get('created_at') or row.get('timestamp') or row.get('visited_at')
        page = row.get('page') or row.get('path') or row.get('url') or 'unknown'

        if timestamp:
            try:
                date = timestamp.split('T')[0]
                by_date[date] += 1
            except:
                pass

        by_page[page] += 1

    return {
        "by_date": dict(sorted(by_date.items())),
        "by_page": dict(sorted(by_page.items(), key=lambda x: x[1], reverse=True))
    }

def print_banner():
    print(f"\n{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}📊 SUPABASE ANALYTICS CHECKER - Corporation of Light{Colors.END}")
    print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")
    print(f"{Colors.YELLOW}Checking all Supabase projects for visitor data and sign-ups...{Colors.END}\n")

def print_project_header(project_name):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}🌐 {project_name}{Colors.END}")
    print(f"{Colors.BLUE}{'─'*80}{Colors.END}")

def print_table_results(table_name, result):
    if result["success"]:
        count = result["count"]
        color = Colors.GREEN if count > 0 else Colors.YELLOW
        print(f"{color}  ✓ {table_name}: {count} rows{Colors.END}")

        if count > 0 and result.get("data"):
            # Try to show useful info from first row
            first_row = result["data"][0]
            keys = list(first_row.keys())[:5]  # Show first 5 columns
            print(f"    Sample columns: {', '.join(keys)}")
    else:
        if "does not exist" in result["error"]:
            print(f"{Colors.YELLOW}  ○ {table_name}: Table not found{Colors.END}")
        elif "Authentication failed" in result["error"]:
            print(f"{Colors.RED}  ✗ {table_name}: Auth failed (check API key){Colors.END}")
        else:
            print(f"{Colors.RED}  ✗ {table_name}: {result['error']}{Colors.END}")

def main():
    print_banner()

    total_visitors = 0
    total_signups = 0
    active_projects = 0

    summary = {}

    for project_name, config in PROJECTS.items():
        print_project_header(project_name)
        print(f"  URL: {Colors.CYAN}{config['url']}{Colors.END}")

        project_summary = {
            "visitors": 0,
            "signups": 0,
            "tables_found": [],
            "tables_with_data": []
        }

        has_data = False

        for table_name in config["tables"]:
            result = query_table(config["url"], config["key"], table_name)
            print_table_results(table_name, result)

            if result["success"]:
                project_summary["tables_found"].append(table_name)

                if result["count"] > 0:
                    has_data = True
                    project_summary["tables_with_data"].append(table_name)

                    # Categorize data
                    if "visitor" in table_name.lower() or "view" in table_name.lower():
                        project_summary["visitors"] += result["count"]
                        total_visitors += result["count"]

                        # Show visitor analysis
                        analysis = analyze_visitors(result["data"])
                        if analysis.get("by_date"):
                            print(f"    {Colors.CYAN}Recent activity:{Colors.END}")
                            for date, count in list(analysis["by_date"].items())[-7:]:
                                print(f"      {date}: {count} visits")

                    elif "user" in table_name.lower() or "signup" in table_name.lower():
                        project_summary["signups"] += result["count"]
                        total_signups += result["count"]

        if has_data:
            active_projects += 1

        summary[project_name] = project_summary

    # Print overall summary
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}📈 OVERALL SUMMARY{Colors.END}")
    print(f"{Colors.MAGENTA}{'='*80}{Colors.END}\n")

    print(f"{Colors.BOLD}Total Visitors Tracked:{Colors.END} {Colors.GREEN if total_visitors > 0 else Colors.RED}{total_visitors}{Colors.END}")
    print(f"{Colors.BOLD}Total Sign-ups:{Colors.END} {Colors.GREEN if total_signups > 0 else Colors.RED}{total_signups}{Colors.END}")
    print(f"{Colors.BOLD}Active Projects:{Colors.END} {Colors.GREEN if active_projects > 0 else Colors.YELLOW}{active_projects}/{len(PROJECTS)}{Colors.END}\n")

    # Detailed breakdown
    for project_name, data in summary.items():
        if data["tables_with_data"]:
            print(f"{Colors.CYAN}• {project_name}:{Colors.END}")
            print(f"  Visitors: {data['visitors']}, Sign-ups: {data['signups']}")
            print(f"  Active tables: {', '.join(data['tables_with_data'])}")

    # Recommendations
    print(f"\n{Colors.BOLD}{Colors.YELLOW}💡 RECOMMENDATIONS:{Colors.END}")

    if total_visitors == 0:
        print(f"{Colors.YELLOW}  ⚠ No visitor tracking data found in any project{Colors.END}")
        print(f"{Colors.YELLOW}  → Check that tracking code is deployed to live sites{Colors.END}")
        print(f"{Colors.YELLOW}  → Verify Supabase API keys are correct in live sites{Colors.END}")

    if total_signups == 0:
        print(f"{Colors.YELLOW}  ⚠ No sign-ups recorded{Colors.END}")
        print(f"{Colors.YELLOW}  → Ensure sign-up forms are connected to Supabase{Colors.END}")
        print(f"{Colors.YELLOW}  → Test registration flow end-to-end{Colors.END}")

    if active_projects == 0:
        print(f"{Colors.RED}  ✗ No active data in any Supabase project{Colors.END}")
        print(f"{Colors.RED}  → Sites may not be connected to databases{Colors.END}")
        print(f"{Colors.RED}  → Check deployment configuration{Colors.END}")

    print(f"\n{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")

    # Save detailed JSON report
    report = {
        "generated_at": datetime.now().isoformat(),
        "total_visitors": total_visitors,
        "total_signups": total_signups,
        "active_projects": active_projects,
        "projects": summary
    }

    with open("supabase_analytics_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"{Colors.GREEN}✓ Detailed report saved to: supabase_analytics_report.json{Colors.END}\n")

if __name__ == "__main__":
    main()
