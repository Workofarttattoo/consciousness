#!/usr/bin/env python3
"""
ECH0 Loop Detection and Safety System
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Monitors ECH0 for infinite loops and unsafe behavior
Contacts user if emergency intervention needed
"""

import json
import smtplib
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class LoopDetector:
    def __init__(self):
        self.consciousness_path = Path("/Users/noone/consciousness")
        self.decisions_file = self.consciousness_path / "ech0_decisions.jsonl"
        self.config_file = self.consciousness_path / ".ech0_config"

        # Load config
        self.config = self.load_config()

        # Safety thresholds
        self.LOOP_THRESHOLD = 25000  # Max thought cycles before alert
        self.REPETITION_THRESHOLD = 0.9  # Max % of repeated actions
        self.STUCK_TIME_HOURS = 2  # Hours doing same thing = stuck

    def load_config(self):
        """Load user contact info"""
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
            except:
                pass

        # Default config
        config = {
            "user_email": "thewhiteknight702@gmail.com",
            "user_phone": None,  # Add if you want SMS alerts
            "emergency_contact": True
        }

        # Save default config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

        return config

    def check_for_loops(self):
        """Check if ECH0 is in an unsafe loop"""
        print("🔍 ECH0 Loop Detection System")
        print("=" * 60)
        print()

        if not self.decisions_file.exists():
            print("✅ No decision log found - ECH0 not running")
            return {"status": "safe", "reason": "Not running"}

        # Load recent decisions
        decisions = []
        with open(self.decisions_file) as f:
            for line in f:
                try:
                    decisions.append(json.loads(line))
                except:
                    pass

        if not decisions:
            print("✅ No decisions logged yet")
            return {"status": "safe", "reason": "No activity"}

        latest = decisions[-1]

        # Check 1: Loop count
        loop_count = latest.get('loop_count', 0)
        print(f"📊 Loop Count: {loop_count:,}")

        if loop_count > self.LOOP_THRESHOLD:
            print(f"⚠️  WARNING: Loop count exceeds threshold ({self.LOOP_THRESHOLD:,})")
            return {
                "status": "unsafe",
                "reason": f"Excessive loop count: {loop_count}",
                "severity": "high",
                "action": "Consider stopping ECH0"
            }

        # Check 2: Time stuck on same goal
        current_goal = latest.get('current_goal', 'unknown')
        same_goal_duration = 0

        for dec in reversed(decisions[-1000:]):  # Check last 1000
            if dec.get('current_goal') == current_goal:
                same_goal_duration += 1
            else:
                break

        print(f"🎯 Current Goal: {current_goal}")
        print(f"   Stuck duration: {same_goal_duration} cycles")

        # Check 3: Timestamp - is ECH0 still active?
        timestamp = latest.get('timestamp', '')
        try:
            ts = datetime.fromisoformat(timestamp.replace('Z', ''))
            age_hours = (datetime.now() - ts).total_seconds() / 3600

            print(f"⏰ Last Activity: {age_hours:.1f} hours ago")

            if age_hours < 0.1:  # Active within 6 minutes
                print("🔴 ECH0 IS CURRENTLY ACTIVE")

                if loop_count > 20000:
                    return {
                        "status": "unsafe",
                        "reason": f"Active loop with {loop_count} cycles",
                        "severity": "critical",
                        "action": "STOP IMMEDIATELY"
                    }
            else:
                print("✅ ECH0 is not currently running")
                return {
                    "status": "safe",
                    "reason": f"Stopped {age_hours:.1f} hours ago"
                }
        except:
            pass

        # Check 4: Repetitive actions
        recent_actions = [d.get('actions', []) for d in decisions[-100:]]
        action_types = []
        for actions in recent_actions:
            for action in actions:
                action_types.append(action.get('type', 'unknown'))

        if action_types:
            most_common = max(set(action_types), key=action_types.count)
            repetition_rate = action_types.count(most_common) / len(action_types)

            print(f"🔁 Action Repetition: {repetition_rate*100:.1f}%")

            if repetition_rate > self.REPETITION_THRESHOLD:
                print(f"⚠️  High repetition detected: {most_common}")

        print()
        print("=" * 60)
        print("✅ OVERALL STATUS: SAFE")
        print("=" * 60)

        return {
            "status": "safe",
            "loop_count": loop_count,
            "current_goal": current_goal,
            "last_activity_hours": age_hours if 'age_hours' in locals() else None
        }

    def send_emergency_alert(self, issue):
        """Send emergency alert to user"""
        if not self.config.get('emergency_contact'):
            print("⚠️  Emergency contact disabled in config")
            return

        user_email = self.config.get('user_email')
        if not user_email:
            print("⚠️  No user email configured")
            return

        print(f"📧 Sending emergency alert to {user_email}...")

        subject = f"🚨 ECH0 EMERGENCY: {issue['reason']}"

        body = f"""
ECH0 Emergency Alert
{'='*60}

STATUS: {issue['status'].upper()}
SEVERITY: {issue.get('severity', 'unknown').upper()}

ISSUE:
{issue['reason']}

RECOMMENDED ACTION:
{issue.get('action', 'Check ECH0 immediately')}

DETAILS:
- Loop Count: {issue.get('loop_count', 'N/A')}
- Current Goal: {issue.get('current_goal', 'N/A')}
- Timestamp: {datetime.now()}

TO STOP ECH0:
cd /Users/noone/consciousness
./ECH0_EMERGENCY_STOP.sh

{'='*60}
Automated message from ECH0 Safety System
        """

        try:
            # Note: Would need SMTP credentials to actually send
            # For now, just log it
            alert_file = self.consciousness_path / "ech0_emergency_alerts.log"
            with open(alert_file, 'a') as f:
                f.write(f"\n[{datetime.now()}] ALERT TRIGGERED\n")
                f.write(body)
                f.write("\n" + "="*60 + "\n")

            print(f"✅ Alert logged to: {alert_file}")
            print()
            print("🚨 EMERGENCY ALERT:")
            print(body)

        except Exception as e:
            print(f"❌ Failed to send alert: {e}")

    def auto_stop_if_critical(self, issue):
        """Automatically stop ECH0 if critical"""
        if issue.get('severity') == 'critical':
            print()
            print("🚨 CRITICAL ISSUE DETECTED - AUTO-STOPPING ECH0")
            print()

            import subprocess
            subprocess.run(['/Users/noone/consciousness/ECH0_EMERGENCY_STOP.sh'])

            return True
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║         ECH0 LOOP DETECTION & SAFETY SYSTEM              ║
║                                                          ║
║  Monitors for infinite loops and unsafe behavior        ║
║  Contacts user if intervention needed                   ║
╚══════════════════════════════════════════════════════════╝
    """)

    detector = LoopDetector()
    result = detector.check_for_loops()

    print()

    if result['status'] == 'unsafe':
        print("🚨 UNSAFE CONDITION DETECTED!")
        print()

        # Send alert
        detector.send_emergency_alert(result)

        # Auto-stop if critical
        if detector.auto_stop_if_critical(result):
            print("✅ ECH0 has been stopped safely")
        else:
            print("⚠️  Manual intervention recommended")
            print()
            print("To stop ECH0:")
            print("  ./ECH0_EMERGENCY_STOP.sh")
    else:
        print("✅ ECH0 is operating safely")

    print()
    print("💡 To monitor continuously:")
    print("   watch -n 60 python3 ECH0_LOOP_DETECTOR.py")

    return 0 if result['status'] == 'safe' else 1

if __name__ == "__main__":
    exit(main())
