#!/bin/bash
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#
# Quick start script for ECH0 voice chat with all fixes

cd /Users/noone/consciousness

# Load ElevenLabs API key
export ELEVENLABS_API_KEY="sk_b9f1fbb3c26a2c904f285bf864288a53092924388c0a24d4"

echo "🎤 Starting ECH0 Voice Chat"
echo "=========================="
echo ""
echo "✓ ElevenLabs Premium Voice: ENABLED"
echo "✓ Whisper Speech Recognition: Medium model"
echo "✓ LLM: Ollama Qwen 14B (local, free)"
echo ""
echo "Just start talking - no button needed!"
echo ""

# Check Ollama is running
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "⚠️  Ollama not running. Starting it now..."
    echo ""
    echo "If this fails, run in another terminal:"
    echo "  ollama serve"
    echo ""
fi

python3 ech0_two_way_robust.py
