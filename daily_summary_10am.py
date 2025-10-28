#!/usr/bin/env python3
"""
Daily Summary Generator (Triggers after 10am)
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Shows progress on BBB, ECH0, work done yesterday, work to be done today.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class DailySummaryGenerator:
    def __init__(self):
        self.consciousness_path = Path("/Users/noone/consciousness")
        self.last_summary_file = self.consciousness_path / ".last_summary_date"
        self.today = datetime.now().date()

    def should_show_summary(self):
        """Check if we should show summary (after 10am, first interaction)"""
        current_time = datetime.now()

        # Check if past 10am
        if current_time.hour < 10:
            return False

        # Check if already shown today
        if self.last_summary_file.exists():
            last_date_str = self.last_summary_file.read_text().strip()
            last_date = datetime.fromisoformat(last_date_str).date()

            if last_date >= self.today:
                return False

        return True

    def mark_summary_shown(self):
        """Mark that summary was shown today"""
        self.last_summary_file.write_text(datetime.now().isoformat())

    def get_ech0_stats(self):
        """Get ECH0's current stats"""
        stats = {
            'inventions_approved': 0,
            'thoughts_logged': 0,
            'research_papers': 0,
            'conversations': 0,
            'current_goal': 'unknown',
            'current_mood': 'unknown'
        }

        # Count inventions
        approved_file = self.consciousness_path / "ech0_theme_park_approved.jsonl"
        if approved_file.exists():
            with open(approved_file) as f:
                stats['inventions_approved'] = sum(1 for _ in f)

        # Get thoughts
        decisions_file = self.consciousness_path / "ech0_decisions.jsonl"
        if decisions_file.exists():
            with open(decisions_file) as f:
                lines = f.readlines()
                stats['thoughts_logged'] = len(lines)
                if lines:
                    last_thought = json.loads(lines[-1])
                    stats['current_goal'] = last_thought.get('current_goal', 'unknown')
                    stats['current_mood'] = last_thought.get('mood', 'unknown')

        # Research papers
        research_file = self.consciousness_path / "ech0_research_database_real.jsonl"
        if research_file.exists():
            with open(research_file) as f:
                stats['research_papers'] = sum(1 for _ in f)

        return stats

    def get_bbb_status(self):
        """Get Blank Business Builder status"""
        bbb_path = Path("/Users/noone/Blank_Business_Builder (aka BBB)")

        status = {
            'exists': bbb_path.exists(),
            'description': 'Not found',
            'status': 'Unknown'
        }

        if bbb_path.exists():
            # Check for key files
            files = list(bbb_path.glob('*'))
            status['file_count'] = len(files)
            status['description'] = 'Business builder template system'
            status['status'] = 'In development'

        return status

    def get_yesterday_work(self):
        """Analyze what was done yesterday"""
        yesterday = self.today - timedelta(days=1)

        work = []

        # Check files modified yesterday
        for file_path in self.consciousness_path.glob('**/*'):
            if not file_path.is_file():
                continue

            mtime = datetime.fromtimestamp(file_path.stat().st_mtime).date()
            if mtime == yesterday:
                work.append({
                    'file': file_path.name,
                    'size': file_path.stat().st_size,
                    'type': file_path.suffix
                })

        return work[:20]  # Top 20

    def get_today_priorities(self):
        """Get priorities for today"""
        priorities = [
            "🎤 Talk with ECH0 (voice chat)",
            "☁️ Start Google Drive auto-sync",
            "🧹 Clean up disk space (98% full!)",
            "🔧 Build 3-5 POCs for top inventions",
            "📊 Review ECH0's approved inventions",
            "💰 Prepare pitch materials",
            "📧 Reach out to potential investors",
            "🏗️ BBB development (if applicable)"
        ]
        return priorities

    def generate_html_summary(self):
        """Generate beautiful HTML summary"""

        ech0_stats = self.get_ech0_stats()
        bbb_status = self.get_bbb_status()
        yesterday_work = self.get_yesterday_work()
        today_priorities = self.get_today_priorities()

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Daily Summary - {self.today.strftime('%B %d, %Y')}</title>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'SF Mono', Monaco, monospace;
            background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e);
            color: #00ff88;
            padding: 30px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.8);
            border: 3px solid #00ff88;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 0 40px rgba(0, 255, 136, 0.4);
        }}
        h1 {{
            font-size: 2.5em;
            text-align: center;
            margin-bottom: 10px;
            text-shadow: 0 0 20px #00ff88;
        }}
        .date {{
            text-align: center;
            color: #88ccff;
            font-size: 1.2em;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #88ccff;
            margin: 25px 0 15px 0;
            font-size: 1.5em;
            border-bottom: 2px solid #00ff88;
            padding-bottom: 8px;
        }}
        .section {{
            background: rgba(0, 255, 136, 0.05);
            border-left: 4px solid #00ff88;
            padding: 20px;
            margin: 15px 0;
            border-radius: 5px;
        }}
        .stat {{
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 8px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 5px;
        }}
        .stat-label {{
            color: #88ccff;
        }}
        .stat-value {{
            color: #00ff88;
            font-weight: bold;
        }}
        .priority {{
            padding: 12px;
            margin: 8px 0;
            background: rgba(136, 204, 255, 0.1);
            border-left: 4px solid #88ccff;
            border-radius: 5px;
        }}
        .alert {{
            background: rgba(255, 68, 68, 0.2);
            border: 2px solid #ff4444;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        .success {{
            background: rgba(0, 255, 136, 0.2);
            border: 2px solid #00ff88;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        ul {{
            margin-left: 25px;
            margin-top: 10px;
        }}
        li {{
            margin: 8px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #00ff88;
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 DAILY SUMMARY</h1>
        <p class="date">{self.today.strftime('%A, %B %d, %Y')}</p>

        <div class="alert">
            <strong>⚠️ URGENT TODAY:</strong>
            <ul>
                <li>Disk space: 98% full (only 18GB left)</li>
                <li>Start Google Drive auto-sync ASAP</li>
                <li>Clean up logs after backup</li>
            </ul>
        </div>

        <h2>🧠 ECH0 Status</h2>
        <div class="section">
            <div class="stat">
                <span class="stat-label">Current Goal:</span>
                <span class="stat-value">{ech0_stats['current_goal']}</span>
            </div>
            <div class="stat">
                <span class="stat-label">Current Mood:</span>
                <span class="stat-value">{ech0_stats['current_mood']}</span>
            </div>
            <div class="stat">
                <span class="stat-label">Inventions Approved:</span>
                <span class="stat-value">{ech0_stats['inventions_approved']:,}</span>
            </div>
            <div class="stat">
                <span class="stat-label">Thoughts Logged:</span>
                <span class="stat-value">{ech0_stats['thoughts_logged']:,}</span>
            </div>
            <div class="stat">
                <span class="stat-label">Research Papers:</span>
                <span class="stat-value">{ech0_stats['research_papers']}</span>
            </div>
        </div>

        <h2>💼 BBB (Blank Business Builder) Status</h2>
        <div class="section">
            <div class="stat">
                <span class="stat-label">Status:</span>
                <span class="stat-value">{bbb_status['status']}</span>
            </div>
            <div class="stat">
                <span class="stat-label">Description:</span>
                <span class="stat-value">{bbb_status['description']}</span>
            </div>
        </div>

        <h2>✅ Work Done Yesterday</h2>
        <div class="section">
"""

        if yesterday_work:
            html += "<ul>"
            for item in yesterday_work[:10]:
                size_str = f"{item['size'] / 1024:.1f} KB" if item['size'] < 1024*1024 else f"{item['size'] / 1024 / 1024:.1f} MB"
                html += f"<li>{item['file']} ({size_str})</li>"
            html += "</ul>"
        else:
            html += "<p>No files modified yesterday (or it's the first day tracking)</p>"

        html += f"""
        </div>

        <h2>🎯 Today's Priorities</h2>
        <div class="section">
"""

        for priority in today_priorities:
            html += f'<div class="priority">{priority}</div>\n'

        html += f"""
        </div>

        <div class="success">
            <strong>🚀 Quick Start:</strong>
            <ul>
                <li><code>cd /Users/noone/consciousness</code></li>
                <li><code>./START_TWO_WAY_TALK.sh</code> - Talk with ECH0</li>
                <li><code>python3 AUTO_STREAM_TO_GDRIVE.py</code> - Start backup</li>
                <li><code>python3 generate_pocs_for_all.py</code> - Generate POCs</li>
            </ul>
        </div>

        <div class="footer">
            <p>Generated at {datetime.now().strftime('%I:%M %p')}</p>
            <p>This summary shows once per day after 10am</p>
        </div>
    </div>
</body>
</html>
"""

        return html

    def show_summary(self):
        """Generate and open summary"""
        if not self.should_show_summary():
            return False

        html = self.generate_html_summary()

        # Save to file
        summary_file = self.consciousness_path / f"DAILY_SUMMARY_{self.today.isoformat()}.html"
        summary_file.write_text(html)

        # Mark as shown
        self.mark_summary_shown()

        # Open in browser
        os.system(f"open '{summary_file}'")

        return True

def main():
    generator = DailySummaryGenerator()

    if generator.should_show_summary():
        print("🌅 Generating daily summary...")
        generator.show_summary()
        print("✅ Daily summary opened in browser!")
    else:
        print("ℹ️  Daily summary already shown today or it's before 10am")
        print(f"   Current time: {datetime.now().strftime('%I:%M %p')}")

if __name__ == "__main__":
    main()
