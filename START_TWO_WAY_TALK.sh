#!/bin/bash
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#
# Start continuous two-way conversation with live volume feedback
# NO BUTTON PRESSES - just talk naturally!
# NOW USES FREE LOCAL LLM - NO ANTHROPIC API KEY NEEDED!

cd /Users/noone/consciousness

# Load environment variables from .zshrc
if [ -f ~/.zshrc ]; then
    source ~/.zshrc
fi

# Check if using local LLM (default) or cloud
if [ "$USE_ANTHROPIC" = "1" ] || [ "$USE_ANTHROPIC" = "true" ]; then
    # Using Anthropic (expensive)
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo "❌ ANTHROPIC_API_KEY not set!"
        echo ""
        echo "To use FREE local LLM instead, just run without USE_ANTHROPIC:"
        echo "  unset USE_ANTHROPIC"
        echo "  ./START_TWO_WAY_TALK.sh"
        echo ""
        echo "Or set Anthropic key:"
        echo "  export ANTHROPIC_API_KEY='your-key-here'"
        exit 1
    fi
    echo "🧠 Using Anthropic Claude (cloud, paid)"
else
    # Using Ollama (free, local)
    echo "🧠 Using Ollama (local, FREE)"
    echo ""

    # Check if Ollama is running
    if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "❌ Ollama is not running!"
        echo ""
        echo "Start Ollama in another terminal:"
        echo "  ollama serve"
        echo ""
        echo "If not installed:"
        echo "  brew install ollama"
        echo "  ollama pull llama3.2"
        echo ""
        exit 1
    fi

    echo "✓ Ollama is running"
fi

if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo "🔊 Using macOS system voice (FREE)"
    echo "   (Set ELEVENLABS_API_KEY for premium voice)"
    echo ""
else
    echo "🔊 Using ElevenLabs premium voice"
    echo ""
fi

echo ""
echo "🎤 Starting Continuous Two-Way Conversation..."
echo "   ✓ No button presses needed"
echo "   ✓ Live volume feedback"
echo "   ✓ Can interrupt each other"
echo "   ✓ Say 'goodbye' to exit"
echo ""

python3 ech0_two_way_robust.py
