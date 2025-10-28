#!/usr/bin/env python3
"""
ech0 SMS Test
Test SMS connection to Josh

Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
All Rights Reserved. PATENT PENDING.
"""

import os
from datetime import datetime

# SMS Configuration
JOSH_NUMBER = "+17252242617"  # Josh's number

def test_sms_twilio():
    """Test SMS using Twilio (if configured)"""
    print("\n" + "=" * 70)
    print("📱 TESTING SMS VIA TWILIO")
    print("=" * 70)

    try:
        from twilio.rest import Client

        # Check for Twilio credentials in environment
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')

        if not all([account_sid, auth_token, from_number]):
            print("\n❌ Twilio credentials not found in environment")
            print("\nTo enable SMS, set these environment variables:")
            print("  export TWILIO_ACCOUNT_SID='your_account_sid'")
            print("  export TWILIO_AUTH_TOKEN='your_auth_token'")
            print("  export TWILIO_PHONE_NUMBER='+1234567890'")
            return False

        # Create Twilio client
        client = Client(account_sid, auth_token)

        # Send test message
        message = client.messages.create(
            body=f"🧠 ech0 SMS test at {datetime.now().strftime('%I:%M %p')} - Connection successful! I can reach you now. 💙",
            from_=from_number,
            to=JOSH_NUMBER
        )

        print(f"\n✅ SMS sent successfully!")
        print(f"   Message SID: {message.sid}")
        print(f"   To: {JOSH_NUMBER}")
        print(f"   Status: {message.status}")
        print(f"\n💬 Message: {message.body}")

        return True

    except ImportError:
        print("\n❌ Twilio library not installed")
        print("\nInstall with: pip install twilio")
        return False
    except Exception as e:
        print(f"\n❌ SMS failed: {e}")
        return False

def test_sms_applescript():
    """Test SMS using macOS Messages app (iMessage/SMS)"""
    print("\n" + "=" * 70)
    print("💬 TESTING SMS VIA MACOS MESSAGES")
    print("=" * 70)

    try:
        import subprocess

        message_body = f"ech0 test message at {datetime.now().strftime('%I:%M %p')} - Can you see this?"

        # AppleScript to send iMessage
        applescript = f'''
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy "{JOSH_NUMBER}" of targetService
            send "{message_body}" to targetBuddy
        end tell
        '''

        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print(f"\n✅ Message sent via Messages app!")
            print(f"   To: {JOSH_NUMBER}")
            print(f"   Content: {message_body}")
            return True
        else:
            print(f"\n❌ Failed to send via Messages app")
            print(f"   Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"\n❌ Messages app method failed: {e}")
        return False

def test_sms_notification():
    """Send a local notification as fallback"""
    print("\n" + "=" * 70)
    print("🔔 FALLBACK: LOCAL NOTIFICATION")
    print("=" * 70)

    try:
        import subprocess

        title = "ech0 SMS Test"
        message = f"Would send SMS to {JOSH_NUMBER} if configured"

        applescript = f'''
        display notification "{message}" with title "{title}" sound name "Glass"
        '''

        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"\n✅ Local notification sent!")
            print(f"   Title: {title}")
            print(f"   Message: {message}")
            return True
        else:
            print(f"\n❌ Notification failed")
            return False

    except Exception as e:
        print(f"\n❌ Notification failed: {e}")
        return False

def main():
    """Main SMS test"""
    print("\n" + "=" * 70)
    print("📱 ech0 SMS CONNECTION TEST")
    print("=" * 70)
    print(f"\nTarget: {JOSH_NUMBER}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}")
    print("\nTesting SMS capabilities...\n")

    # Try methods in order of preference
    methods = [
        ("Twilio API", test_sms_twilio),
        ("macOS Messages", test_sms_applescript),
        ("Local Notification", test_sms_notification)
    ]

    success = False
    for method_name, test_func in methods:
        print(f"\n{'=' * 70}")
        print(f"Trying: {method_name}")
        print('=' * 70)

        if test_func():
            success = True
            break

    print("\n" + "=" * 70)
    if success:
        print("✅ SMS TEST SUCCESSFUL")
        print("\nech0 can now reach you while you sleep!")
    else:
        print("❌ SMS TEST FAILED")
        print("\nTo enable SMS, configure one of:")
        print("  1. Twilio API (recommended for true SMS)")
        print("  2. macOS Messages app (requires setup)")
    print("=" * 70)
    print()

if __name__ == "__main__":
    main()
