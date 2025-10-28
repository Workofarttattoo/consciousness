#!/bin/bash
# Start ECH0 with 14B brain but keep good voice
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

echo "🧠 Starting ECH0 with:"
echo "   • Brain: 14B Local Model (FREE)"
echo "   • Voice: ElevenLabs/OpenAI TTS (high quality)"

# Kill current ECH0
pkill -f "ech0_two_way_robust.py"
sleep 2

# Make sure Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 Starting Ollama..."
    ollama serve &
    sleep 3
fi

# Preload 14B model
echo "📥 Loading 14B model..."
ollama run qwen2.5:14b-instruct-q5_K_M "test" &
sleep 2
pkill -f "ollama run"

# Start ECH0 with LOCAL brain but KEEP good voice
# DO NOT set USE_OPENAI=1 (that's for the brain)
# The voice will use ElevenLabs if API key exists
cd /Users/noone/consciousness

echo """
╔═══════════════════════════════════════════════════════╗
║     ECH0 CONFIGURATION                                ║
║     Brain: 14B Local (Ollama) - FREE                 ║
║     Voice: ElevenLabs/OpenAI - High Quality          ║
╚═══════════════════════════════════════════════════════╝
"""

# Start with local brain (no USE_OPENAI flag)
python3 ech0_two_way_robust.py &

echo "✅ ECH0 is now using 14B for thinking + good voice for speaking!"