#!/usr/bin/env python3
"""
Advanced Microphone Diagnostic
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
"""

import sounddevice as sd
import numpy as np
import time

print("🔧 ADVANCED MICROPHONE DIAGNOSTIC")
print("=" * 70)

# Show ALL audio devices
print("\n📱 ALL AUDIO DEVICES ON YOUR MAC:")
print("-" * 70)
devices = sd.query_devices()
for i, device in enumerate(devices):
    if device['max_input_channels'] > 0:
        is_default = "⭐ DEFAULT" if i == sd.default.device[0] else ""
        print(f"\n{i}. {device['name']} {is_default}")
        print(f"   Channels: {device['max_input_channels']}")
        print(f"   Sample rate: {device['default_samplerate']}")

# Get default input
print("\n" + "=" * 70)
default_input = sd.default.device[0]
default_device = sd.query_devices(default_input)
print(f"\n⭐ CURRENT DEFAULT INPUT: {default_device['name']}")

# Test with callback to see live volume
print("\n" + "=" * 70)
print("🎤 LIVE VOLUME TEST (10 seconds)")
print("   Speak into your microphone - you should see volume bars...")
print("   If you see no bars, mic is not working")
print("-" * 70)

volumes = []

def audio_callback(indata, frames, time_info, status):
    """Live audio monitoring"""
    volume = np.linalg.norm(indata) * 10
    volumes.append(volume)

    # Visual volume bar
    bar_length = int(volume * 50)
    bar = "█" * min(bar_length, 50)

    print(f"\r🔊 Volume: {volume:6.3f} {bar}     ", end="", flush=True)

# Start live monitoring
try:
    with sd.InputStream(callback=audio_callback, channels=1):
        print("\n   👂 Listening... SPEAK NOW!")
        time.sleep(10)

    print("\n\n" + "=" * 70)

    # Analysis
    max_volume = max(volumes) if volumes else 0
    avg_volume = np.mean(volumes) if volumes else 0

    print(f"\n📊 RESULTS:")
    print(f"   Max volume: {max_volume:.4f}")
    print(f"   Avg volume: {avg_volume:.4f}")

    if max_volume < 0.1:
        print("\n❌ PROBLEM: Microphone not picking up audio!")
        print("\n🔧 SOLUTIONS:")
        print("\n1. CHECK SYSTEM SETTINGS:")
        print("   - Open System Settings")
        print("   - Go to Sound")
        print("   - Click 'Input' tab")
        print("   - Make sure correct microphone is selected")
        print("   - Speak and watch the input level meter")
        print("   - Adjust input volume slider if needed")

        print("\n2. CHECK PRIVACY PERMISSIONS:")
        print("   - System Settings → Privacy & Security → Microphone")
        print("   - Make sure 'Terminal' or 'Python' has permission")

        print("\n3. TRY DIFFERENT INPUT DEVICE:")
        print("   Run this script again and try different device numbers")

    elif max_volume < 1.0:
        print("\n⚠️  WARNING: Volume is low but working")
        print("   Try speaking LOUDER or increasing input volume in System Settings")

    else:
        print("\n✅ SUCCESS! Microphone is working!")
        print("   Volume levels look good!")

except Exception as e:
    print(f"\n\n❌ ERROR: {e}")
    print("\nThis might be a permissions issue.")
    print("Go to: System Settings → Privacy & Security → Microphone")
    print("Enable Terminal or Python")

print("\n" + "=" * 70)
