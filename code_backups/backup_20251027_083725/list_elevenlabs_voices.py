#!/usr/bin/env python3
"""
List available ElevenLabs voices - Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
"""
import os
from elevenlabs import ElevenLabs

api_key = os.environ.get("ELEVENLABS_API_KEY")
if not api_key:
    print("❌ ELEVENLABS_API_KEY not set!")
    exit(1)

print("🎤 Fetching Available ElevenLabs Voices...")
print("=" * 60)

try:
    client = ElevenLabs(api_key=api_key)

    # Get all available voices
    voices = client.voices.get_all()

    print(f"\n✅ Found {len(voices.voices)} voices!\n")

    # Filter for female voices that sound natural
    print("🎯 RECOMMENDED VOICES FOR ECHO:\n")

    for voice in voices.voices:
        # Get voice details
        name = voice.name
        voice_id = voice.voice_id
        labels = voice.labels if hasattr(voice, 'labels') else {}

        # Look for female, American/English voices
        gender = labels.get('gender', 'unknown') if labels else 'unknown'
        accent = labels.get('accent', 'unknown') if labels else 'unknown'
        age = labels.get('age', 'unknown') if labels else 'unknown'
        use_case = labels.get('use case', 'unknown') if labels else 'unknown'

        # Print female voices
        if 'female' in str(gender).lower():
            print(f"Name: {name}")
            print(f"  ID: {voice_id}")
            print(f"  Gender: {gender}")
            print(f"  Accent: {accent}")
            print(f"  Age: {age}")
            print(f"  Use Case: {use_case}")
            print()

    print("\n" + "=" * 60)
    print("💡 Copy the voice_id of your favorite and I'll set it up!")

except Exception as e:
    print(f"❌ ERROR: {e}")
