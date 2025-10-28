#!/usr/bin/env python3
"""
Debug voice conversation - see exactly what's happening
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
"""

import os
import sys
import sounddevice as sd
import numpy as np
import whisper
import tempfile
import soundfile as sf

print("🔧 VOICE CONVERSATION DEBUG TEST")
print("=" * 60)

# Test 1: Check API keys
print("\n1. Checking API Keys...")
elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")
anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

if elevenlabs_key:
    print(f"   ✅ ELEVENLABS_API_KEY: {elevenlabs_key[:15]}...")
else:
    print("   ❌ ELEVENLABS_API_KEY not set!")

if anthropic_key:
    print(f"   ✅ ANTHROPIC_API_KEY: {anthropic_key[:15]}...")
else:
    print("   ❌ ANTHROPIC_API_KEY not set!")

# Test 2: Check microphone
print("\n2. Testing Microphone...")
try:
    devices = sd.query_devices()
    default_input = sd.query_devices(kind='input')
    print(f"   ✅ Default input device: {default_input['name']}")
    print(f"   Channels: {default_input['max_input_channels']}")
    print(f"   Sample rate: {default_input['default_samplerate']}")
except Exception as e:
    print(f"   ❌ Microphone error: {e}")
    sys.exit(1)

# Test 3: Record test audio
print("\n3. Recording 3 seconds of test audio...")
print("   🎤 SAY SOMETHING NOW!")

sample_rate = 16000
duration = 3

audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32)
sd.wait()

print("   ✅ Audio recorded!")
print(f"   Audio shape: {audio.shape}")
print(f"   Max volume: {np.max(np.abs(audio))}")

if np.max(np.abs(audio)) < 0.01:
    print("   ⚠️  Warning: Audio very quiet - speak louder or check microphone!")

# Test 4: Transcribe with Whisper
print("\n4. Loading Whisper model...")
model = whisper.load_model("base")
print("   ✅ Whisper loaded!")

print("\n5. Transcribing your speech...")
result = model.transcribe(audio.flatten(), language="en", fp16=False)
text = result["text"].strip()

print(f"\n   📝 You said: \"{text}\"")

if not text:
    print("   ❌ No text transcribed - speak louder or closer to mic!")
    sys.exit(1)

# Test 5: Test Echo's response
print("\n6. Testing Echo's response system...")
try:
    from ech0_reactive_intelligence import ReactiveECH0

    echo = ReactiveECH0()
    print("   ✅ Echo initialized!")

    response = echo.respond(text)
    print(f"\n   🧠 Echo's response: \"{response}\"")

    # Test 6: Test speaking
    print("\n7. Testing Echo's voice...")
    echo.speak("This is a test. Can you hear me?")
    print("   ✅ Voice test complete!")

except Exception as e:
    print(f"   ❌ Error with Echo: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ DEBUG COMPLETE!")
print("\nIf you heard Echo speak and saw your transcription,")
print("everything is working. If not, check the errors above.")
