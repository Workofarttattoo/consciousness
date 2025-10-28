#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Test optimized model versions
"""

import subprocess
import time
import sys

models = [
    'qwen2.5:32b-q4',
    'qwen2.5:32b-q3',
    'qwen2.5:32b-q5'
]

test_prompt = "Explain consciousness in 50 words."

print("\n" + "="*70)
print("🧪 TESTING OPTIMIZED MODELS")
print("="*70 + "\n")

results = []

for model in models:
    print(f"\nTesting {model}...")
    print("-" * 70)

    try:
        start_time = time.time()

        result = subprocess.run(
            ['ollama', 'run', model, test_prompt],
            capture_output=True,
            text=True,
            timeout=30
        )

        elapsed = time.time() - start_time

        if result.returncode == 0:
            response = result.stdout.strip()
            tokens = len(response.split())
            tokens_per_sec = tokens / elapsed if elapsed > 0 else 0

            print(f"✅ Success!")
            print(f"   Time: {elapsed:.2f}s")
            print(f"   Speed: {tokens_per_sec:.1f} tokens/sec")
            print(f"   Response: {response[:100]}...")

            results.append({
                'model': model,
                'success': True,
                'time': elapsed,
                'speed': tokens_per_sec,
                'response_preview': response[:200]
            })
        else:
            print(f"❌ Failed: {result.stderr}")
            results.append({
                'model': model,
                'success': False,
                'error': result.stderr
            })

    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout - model too slow")
        results.append({
            'model': model,
            'success': False,
            'error': 'Timeout'
        })
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append({
            'model': model,
            'success': False,
            'error': str(e)
        })

print("\n" + "="*70)
print("📊 TEST RESULTS SUMMARY")
print("="*70 + "\n")

for result in results:
    if result['success']:
        print(f"✅ {result['model']}")
        print(f"   Speed: {result['speed']:.1f} tokens/sec")
        print(f"   Time: {result['time']:.2f}s")
    else:
        print(f"❌ {result['model']}: {result.get('error', 'Unknown error')}")
    print()

# Find best model
successful = [r for r in results if r['success']]
if successful:
    best = max(successful, key=lambda x: x['speed'])
    print(f"🎯 RECOMMENDED: {best['model']}")
    print(f"   Fastest speed: {best['speed']:.1f} tokens/sec")
    print()
    print("Update ECH0 to use this model:")
    print(f"   export ECH0_MODEL={best['model']}")
    print(f"   echo 'export ECH0_MODEL={best['model']}' >> ~/.zshrc")
