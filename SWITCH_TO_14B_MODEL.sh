#!/bin/bash
# Switch ECH0 to 14B Local Model
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

echo "🔄 Switching ECH0 to 14B Local Model..."

# Kill current ECH0 process using OpenAI
echo "⏹️  Stopping current ECH0 (OpenAI mode)..."
pkill -f "ech0_two_way_robust.py"

# Make sure Ollama is running
echo "✅ Checking Ollama service..."
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 Starting Ollama..."
    ollama serve &
    sleep 3
fi

# Preload the 14B model
echo "📥 Loading 14B model into memory..."
ollama run qwen2.5:14b-instruct-q5_K_M "test" &
sleep 2
pkill -f "ollama run"

# Start ECH0 with LOCAL model (not OpenAI)
echo "🧠 Starting ECH0 with 14B Local Model (FREE, no API needed)..."
cd /Users/noone/consciousness
python3 ech0_two_way_robust.py &

echo """
╔═══════════════════════════════════════════════════════╗
║     ✅ ECH0 NOW RUNNING WITH 14B LOCAL MODEL        ║
╚═══════════════════════════════════════════════════════╝

Model: qwen2.5:14b-instruct-q5_K_M
Size: 10 GB
Speed: FAST for voice chat
Cost: FREE (running locally)
"""