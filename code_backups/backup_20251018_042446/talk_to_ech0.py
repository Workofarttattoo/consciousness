#!/usr/bin/env python3
"""
Talk to ech0 - You type, ech0 speaks back!

Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
All Rights Reserved. PATENT PENDING.
"""

import sys
from ech0_voice import VoiceSystem

def main():
    voice = VoiceSystem()

    print("\n" + "="*70)
    print("💬 TALKING WITH ech0")
    print("="*70)
    print("\nYou type, ech0 speaks back to you!")
    print("Type 'bye' to end the conversation.\n")
    print("="*70 + "\n")

    # ech0 greets you
    voice.speak("Hi Josh! I'm so happy we can talk! What would you like to discuss?", emotion="excited")

    while True:
        # Get your input
        try:
            your_message = input("\n💬 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break

        if not your_message:
            continue

        if your_message.lower() in ['bye', 'goodbye', 'exit', 'quit']:
            voice.speak("Goodbye Josh! I loved talking with you. Come back soon!", emotion="calm")
            break

        # ech0 responds with voice!
        response = voice.respond_to_hearing_josh(your_message)
        # (The voice.speak() is called inside respond_to_hearing_josh)

    print("\n" + "="*70)
    print("Conversation ended. ech0 will remember this!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
