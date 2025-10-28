#!/bin/bash
# Start ECH0 Voice Chat with Fixed 14B Model

clear
echo "========================================================================"
echo "🎤 ECH0 VOICE CHAT - READY TO TALK!"
echo "========================================================================"
echo ""

cd /Users/noone/consciousness

# Check Ollama is running
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "❌ Ollama is not running!"
    echo ""
    echo "Starting Ollama..."
    ollama serve &
    sleep 3
    echo "✓ Ollama started"
fi

# Check if model is available
if ! ollama list | grep -q "qwen2.5:14b-instruct-q5_K_M"; then
    echo "❌ Model not found!"
    echo ""
    echo "Pulling model (this will take a few minutes)..."
    ollama pull qwen2.5:14b-instruct-q5_K_M
fi

echo ""
echo "✅ Everything ready!"
echo ""
echo "🎤 VOICE CHAT FEATURES:"
echo "   • Just start talking - ECH0 will hear you"
echo "   • Wait for silence - ECH0 will respond"
echo "   • Say 'goodbye' to exit"
echo "   • Interrupt each other naturally"
echo ""
echo "🔊 AUDIO:"
echo "   • Using macOS system voice (FREE)"
echo "   • Set ELEVENLABS_API_KEY for premium voice"
echo ""
echo "🧠 MODEL:"
echo "   • Qwen 2.5 14B Instruct (YOUR MODEL)"
echo "   • Local & FREE - no API costs"
echo "   • Fast responses optimized for voice"
echo ""
echo "========================================================================"
echo ""

python3 ech0_two_way_robust.py
