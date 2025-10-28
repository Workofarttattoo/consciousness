#!/usr/bin/env python3
"""
Quick test of ElevenLabs voice - Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
"""
import os
import subprocess
import tempfile
from elevenlabs import ElevenLabs, VoiceSettings

# Test connection
api_key = os.environ.get("ELEVENLABS_API_KEY")
if not api_key:
    print("❌ ELEVENLABS_API_KEY not set!")
    exit(1)

print("🔥 Testing ElevenLabs Voice - Rachel")
print("=" * 50)

try:
    client = ElevenLabs(api_key=api_key)

    test_text = "Well hey there, Joshua! I'm Echo, and I sound like a real person now - not some robot. This is what actual Texas sass sounds like, baby!"

    print("📡 Generating audio from ElevenLabs...")

    # Try the default pre-made voice ID (should work without voices_read permission)
    # This is Rachel's actual voice ID from ElevenLabs pre-made voices
    audio_generator = client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel - pre-made voice
        text=test_text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.5,
            use_speaker_boost=True
        )
    )

    print("💾 Saving audio...")
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        audio_path = f.name
        for chunk in audio_generator:
            if chunk:
                f.write(chunk)

    print(f"🎤 Playing audio: {audio_path}")
    subprocess.run(["afplay", audio_path])

    print("\n✅ SUCCESS! ElevenLabs is working!")
    print("🎉 Echo will now sound like a REAL PERSON!")

    # Cleanup
    os.remove(audio_path)

except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\nTroubleshooting:")
    print("1. Check your API key is valid")
    print("2. Make sure you have internet connection")
    print("3. Verify you have credits remaining at elevenlabs.io")
