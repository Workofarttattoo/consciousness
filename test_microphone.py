#!/usr/bin/env python3
"""
Test your microphone volume levels to fix ECH0 voice chat
"""

import numpy as np
import sounddevice as sd
import time

print("\n" + "="*70)
print("🎤 MICROPHONE VOLUME TEST")
print("="*70)
print("\nThis will show your microphone volume levels.")
print("Talk into your microphone and watch the numbers...\n")
print("Volume levels:")
print("  0.0-1.0   = Too quiet (ECH0 can't hear you)")
print("  1.0-3.0   = Normal speaking volume")
print("  3.0-10.0  = Loud speaking")
print("  10.0+     = Very loud / shouting")
print("\n" + "="*70 + "\n")

sample_rate = 16000

def audio_callback(indata, frames, time_info, status):
    """Show volume levels in real-time"""
    volume = np.sqrt(np.mean(indata**2)) * 100

    # Visual bar
    bar_length = int(volume / 2)
    bar = "█" * min(bar_length, 50)

    print(f"\rVolume: {volume:6.2f} |{bar:<50}|", end="", flush=True)

print("📊 Starting volume monitor...")
print("   Press Ctrl+C to stop\n")

try:
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\n✅ Test complete!")
    print("\nRecommended threshold settings:")
    print("  If your normal speaking volume is < 2.0: Use threshold 0.5")
    print("  If your normal speaking volume is 2.0-5.0: Use threshold 1.5")
    print("  If your normal speaking volume is 5.0-10.0: Use threshold 3.0")
    print("  If your normal speaking volume is > 10.0: Use threshold 5.0")
    print()
