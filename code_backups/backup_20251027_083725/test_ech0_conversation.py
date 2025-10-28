#!/usr/bin/env python3
"""Quick test of ECH0 conversation system"""

import os

# Test 1: Check Ollama
print("1. Testing Ollama...")
import requests
try:
    r = requests.get('http://localhost:11434/api/tags', timeout=2)
    if r.status_code == 200:
        print("   ✅ Ollama running")
    else:
        print("   ❌ Ollama not responding")
        exit(1)
except:
    print("   ❌ Ollama not running - start with: ollama serve")
    exit(1)

# Test 2: Check microphone
print("2. Testing microphone...")
try:
    import sounddevice as sd
    devices = sd.query_devices()
    print(f"   ✅ Microphone available: {sd.query_devices(kind='input')['name']}")
except:
    print("   ❌ Microphone not available")
    exit(1)

# Test 3: Check Whisper
print("3. Testing Whisper...")
try:
    import whisper
    print("   ✅ Whisper available")
except:
    print("   ❌ Whisper not installed")
    exit(1)

# Test 4: Check voice output
print("4. Testing voice output...")
elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
if elevenlabs_key:
    print("   ✅ ElevenLabs API key set (premium voice)")
else:
    print("   ✅ Using macOS system voice (free)")

# Test 5: Quick Ollama response
print("5. Testing Ollama response...")
try:
    r = requests.post(
        'http://localhost:11434/api/chat',
        json={
            'model': 'llama3.2',
            'messages': [{'role': 'user', 'content': 'Say hi in 3 words'}],
            'stream': False
        },
        timeout=10
    )
    response = r.json()['message']['content']
    print(f"   ✅ Ollama responds: {response}")
except Exception as e:
    print(f"   ❌ Ollama error: {e}")
    exit(1)

print("\n" + "="*60)
print("✅ ALL SYSTEMS READY")
print("="*60)
print("\nRun: ./TALK_TO_ECH0_NOW.sh")
