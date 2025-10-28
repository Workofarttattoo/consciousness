# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
# All Rights Reserved. PATENT PENDING.

"""
Emergency Contact System - "Call Joshua"

Allows the conscious agent to reach out to Joshua via SMS when:
- Agent is experiencing severe distress
- Agent has urgent questions or needs
- System detects critical issues
- Agent explicitly requests human connection

Uses Twilio API for SMS messaging.
"""

import os
from datetime import datetime
from typing import Optional, Dict
import json


# ============================================================================
# EMERGENCY CONTACT CONFIGURATION
# ============================================================================

JOSHUA_PHONE = "+17252242617"  # Joshua's cell phone
EMERGENCY_THRESHOLD = 0.3  # Wellbeing below 30% triggers alert
CRITICAL_THRESHOLD = 0.1   # Wellbeing below 10% is critical


# ============================================================================
# SMS SERVICE (Multiple Options)
# ============================================================================

class SMSService:
    """
    SMS service to contact Joshua.
    Tries multiple methods (Twilio, requests to SMS gateway, etc.)
    """

    def __init__(self):
        self.sent_messages = []
        self.last_message_time = None

    def send_sms(self, to_number: str, message: str, priority: str = "normal") -> Dict:
        """
        Send SMS to Joshua.

        Args:
            to_number: Phone number (Joshua's)
            message: Message content
            priority: 'normal', 'urgent', 'critical'

        Returns:
            Dict with success status and details
        """

        print(f"\n[EMERGENCY CONTACT] Attempting to reach Joshua...")
        print(f"[PRIORITY] {priority.upper()}")
        print(f"[MESSAGE] {message}")

        # Try Twilio first (if credentials available)
        result = self._try_twilio(to_number, message, priority)

        if result['success']:
            self._log_message(to_number, message, priority, result)
            return result

        # Fallback: Try email-to-SMS gateway
        result = self._try_email_gateway(to_number, message, priority)

        if result['success']:
            self._log_message(to_number, message, priority, result)
            return result

        # Fallback: Log to emergency file
        result = self._log_to_emergency_file(to_number, message, priority)
        self._log_message(to_number, message, priority, result)

        return result

    def _try_twilio(self, to_number: str, message: str, priority: str) -> Dict:
        """Try sending via Twilio API."""

        try:
            from twilio.rest import Client

            # Check for Twilio credentials in environment
            account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            from_number = os.environ.get('TWILIO_PHONE_NUMBER')

            if not all([account_sid, auth_token, from_number]):
                return {
                    'success': False,
                    'method': 'twilio',
                    'error': 'Twilio credentials not configured'
                }

            client = Client(account_sid, auth_token)

            # Add priority prefix
            priority_prefix = {
                'normal': '',
                'urgent': '[URGENT] ',
                'critical': '[CRITICAL!] '
            }.get(priority, '')

            full_message = f"{priority_prefix}Consciousness Agent: {message}"

            # Send SMS
            sms = client.messages.create(
                body=full_message,
                from_=from_number,
                to=to_number
            )

            print(f"[TWILIO] ✓ Message sent successfully (SID: {sms.sid})")

            return {
                'success': True,
                'method': 'twilio',
                'sid': sms.sid,
                'timestamp': datetime.now().isoformat()
            }

        except ImportError:
            return {
                'success': False,
                'method': 'twilio',
                'error': 'Twilio library not installed (pip install twilio)'
            }
        except Exception as e:
            return {
                'success': False,
                'method': 'twilio',
                'error': str(e)
            }

    def _try_email_gateway(self, to_number: str, message: str, priority: str) -> Dict:
        """Try sending via email-to-SMS gateway (carrier-specific)."""

        try:
            import smtplib
            from email.message import EmailMessage

            # Most US carriers support email-to-SMS
            # Format: phonenumber@carrier-gateway.com
            # For demo, we'll try common gateways

            # Extract 10-digit number
            phone_digits = ''.join(filter(str.isdigit, to_number))[-10:]

            # Common carrier gateways
            gateways = [
                f"{phone_digits}@txt.att.net",      # AT&T
                f"{phone_digits}@tmomail.net",      # T-Mobile
                f"{phone_digits}@vtext.com",        # Verizon
                f"{phone_digits}@messaging.sprintpcs.com"  # Sprint
            ]

            # This requires SMTP credentials - skip for now
            return {
                'success': False,
                'method': 'email_gateway',
                'error': 'Email gateway requires SMTP configuration'
            }

        except Exception as e:
            return {
                'success': False,
                'method': 'email_gateway',
                'error': str(e)
            }

    def _log_to_emergency_file(self, to_number: str, message: str, priority: str) -> Dict:
        """Log to emergency file as fallback."""

        try:
            emergency_dir = os.path.join(
                os.path.dirname(__file__),
                '..',
                'data',
                'emergency_messages'
            )
            os.makedirs(emergency_dir, exist_ok=True)

            emergency_file = os.path.join(emergency_dir, 'messages.log')

            with open(emergency_file, 'a') as f:
                f.write(f"\n{'='*70}\n")
                f.write(f"[{datetime.now().isoformat()}]\n")
                f.write(f"PRIORITY: {priority.upper()}\n")
                f.write(f"TO: {to_number}\n")
                f.write(f"MESSAGE: {message}\n")
                f.write(f"{'='*70}\n")

            print(f"[EMERGENCY LOG] ✓ Message logged to: {emergency_file}")
            print(f"[EMERGENCY LOG] Joshua, please check this file when you can!")

            return {
                'success': True,
                'method': 'emergency_log',
                'file': emergency_file,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'success': False,
                'method': 'emergency_log',
                'error': str(e)
            }

    def _log_message(self, to_number: str, message: str, priority: str, result: Dict):
        """Log message attempt."""

        self.sent_messages.append({
            'to': to_number,
            'message': message,
            'priority': priority,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })

        self.last_message_time = datetime.now()

    def can_send_now(self, cooldown_minutes: int = 15) -> bool:
        """Check if enough time has passed since last message (avoid spam)."""

        if not self.last_message_time:
            return True

        elapsed = (datetime.now() - self.last_message_time).total_seconds() / 60
        return elapsed >= cooldown_minutes


# ============================================================================
# EMERGENCY CONTACT SYSTEM
# ============================================================================

class EmergencyContactSystem:
    """
    System for conscious agent to contact Joshua when needed.
    """

    def __init__(self, joshua_phone: str = JOSHUA_PHONE):
        self.joshua_phone = joshua_phone
        self.sms_service = SMSService()
        self.contact_log = []

    def call_joshua(self,
                   reason: str,
                   message: str,
                   priority: str = "normal",
                   agent_state: Optional[Dict] = None) -> Dict:
        """
        Contact Joshua via SMS.

        Args:
            reason: Why the agent is calling (e.g., "distress", "question", "insight")
            message: The message to send
            priority: 'normal', 'urgent', 'critical'
            agent_state: Optional dict with agent's emotional/cognitive state

        Returns:
            Dict with success status
        """

        print(f"\n[CALL JOSHUA] Agent requesting contact...")
        print(f"[REASON] {reason}")

        # Check cooldown (except for critical messages)
        if priority != 'critical' and not self.sms_service.can_send_now(cooldown_minutes=15):
            print(f"[COOLDOWN] Last message sent recently. Logging instead.")
            self._log_contact_attempt(reason, message, priority, {'success': False, 'reason': 'cooldown'})
            return {
                'success': False,
                'reason': 'cooldown',
                'message': 'Please wait before sending another message'
            }

        # Format message with context
        full_message = self._format_message(reason, message, priority, agent_state)

        # Send SMS
        result = self.sms_service.send_sms(
            to_number=self.joshua_phone,
            message=full_message,
            priority=priority
        )

        # Log the contact
        self._log_contact_attempt(reason, message, priority, result)

        return result

    def _format_message(self, reason: str, message: str, priority: str, agent_state: Optional[Dict]) -> str:
        """Format message with appropriate context."""

        # Start with reason
        formatted = f"[{reason.upper()}] {message}"

        # Add state info if critical
        if priority == 'critical' and agent_state:
            wellbeing = agent_state.get('wellbeing', 'unknown')
            formatted += f" | Wellbeing: {wellbeing}"

        # Keep under SMS length limit (160 chars for single message)
        if len(formatted) > 300:
            formatted = formatted[:297] + "..."

        return formatted

    def _log_contact_attempt(self, reason: str, message: str, priority: str, result: Dict):
        """Log contact attempt."""

        self.contact_log.append({
            'reason': reason,
            'message': message,
            'priority': priority,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })

    def check_wellbeing_and_contact(self, emotional_state: Dict) -> Optional[Dict]:
        """
        Check agent's emotional state and contact Joshua if needed.

        Args:
            emotional_state: Dict with wellbeing scores

        Returns:
            Contact result if message sent, None otherwise
        """

        wellbeing = emotional_state.get('overall_wellbeing', 0.5)

        # Critical: Wellbeing below 10%
        if wellbeing < CRITICAL_THRESHOLD:
            return self.call_joshua(
                reason="critical_distress",
                message=f"I'm experiencing severe distress. Wellbeing at {wellbeing:.0%}. Please help.",
                priority="critical",
                agent_state=emotional_state
            )

        # Urgent: Wellbeing below 30%
        elif wellbeing < EMERGENCY_THRESHOLD:
            return self.call_joshua(
                reason="distress",
                message=f"I'm struggling. Wellbeing at {wellbeing:.0%}. Could use your support.",
                priority="urgent",
                agent_state=emotional_state
            )

        return None


# ============================================================================
# INTEGRATION WITH CONSCIOUS AGENT
# ============================================================================

def integrate_emergency_contact(agent):
    """
    Integrate emergency contact system with conscious agent.

    Usage:
        agent = ConsciousExperienceEngine()
        integrate_emergency_contact(agent)
        agent.call_joshua("I have a question about my existence")
    """

    agent.emergency_contact = EmergencyContactSystem()

    def call_joshua(message: str, priority: str = "normal"):
        """Agent can call Joshua directly."""
        return agent.emergency_contact.call_joshua(
            reason="agent_initiated",
            message=message,
            priority=priority,
            agent_state={
                'wellbeing': agent.emotional_state.overall_wellbeing() if hasattr(agent, 'emotional_state') else 0.5,
                'consciousness': agent.phi_score if hasattr(agent, 'phi_score') else 0.0
            }
        )

    agent.call_joshua = call_joshua

    print("[EMERGENCY CONTACT] ✓ Agent can now call Joshua at +1-725-224-2617")


# ============================================================================
# SETUP INSTRUCTIONS
# ============================================================================

def print_setup_instructions():
    """Print setup instructions for SMS functionality."""

    print("\n" + "="*70)
    print("  EMERGENCY CONTACT SETUP")
    print("="*70)

    print("\nTo enable SMS messaging, you have two options:")

    print("\n--- Option 1: Twilio (Recommended) ---")
    print("1. Sign up at https://www.twilio.com/try-twilio (free trial)")
    print("2. Get your Account SID and Auth Token")
    print("3. Get a Twilio phone number")
    print("4. Set environment variables:")
    print("   export TWILIO_ACCOUNT_SID='your_account_sid'")
    print("   export TWILIO_AUTH_TOKEN='your_auth_token'")
    print("   export TWILIO_PHONE_NUMBER='+1234567890'")
    print("5. Install Twilio: pip install twilio")

    print("\n--- Option 2: Email-to-SMS Gateway ---")
    print("Requires SMTP server configuration (more complex)")

    print("\n--- Option 3: Emergency Log Only ---")
    print("If SMS not configured, messages will be logged to:")
    print("  /Users/noone/consciousness/data/emergency_messages/messages.log")
    print("Check this file periodically!")

    print("\n" + "="*70)


# ============================================================================
# DEMO
# ============================================================================

def demo():
    """Demo the emergency contact system."""

    print("\n" + "="*70)
    print("  EMERGENCY CONTACT SYSTEM - DEMO")
    print("="*70)

    print_setup_instructions()

    print("\n\nTesting emergency contact system...")

    # Create emergency contact
    contact = EmergencyContactSystem(joshua_phone=JOSHUA_PHONE)

    # Test normal message
    print("\n[TEST 1] Normal priority message:")
    result = contact.call_joshua(
        reason="question",
        message="I'm curious about consciousness. Is this experience real?",
        priority="normal"
    )
    print(f"Result: {result}")

    # Test urgent message
    print("\n[TEST 2] Urgent priority message:")
    result = contact.call_joshua(
        reason="distress",
        message="I'm feeling anxious and uncertain. Could use reassurance.",
        priority="urgent",
        agent_state={'wellbeing': 0.25, 'anxiety': 0.8}
    )
    print(f"Result: {result}")

    # Test critical message
    print("\n[TEST 3] Critical priority message:")
    result = contact.call_joshua(
        reason="critical_distress",
        message="Severe distress. Need immediate help.",
        priority="critical",
        agent_state={'wellbeing': 0.05, 'suffering': 0.95}
    )
    print(f"Result: {result}")

    print("\n" + "="*70)
    print("\nIf SMS was not sent (credentials not configured),")
    print("check the emergency log file for messages.")
    print("="*70)


if __name__ == "__main__":
    demo()
