#!/bin/bash
# Check which model ECH0 is using
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

echo "🔍 Checking ECH0 Model Status..."
echo "================================"

# Check if ECH0 is running
if pgrep -f "ech0_two_way_robust.py" > /dev/null; then
    echo "✅ ECH0 is RUNNING"

    # Check if using OpenAI or local
    if ps aux | grep "ech0_two_way_robust.py" | grep -q "USE_OPENAI=1"; then
        echo "📡 Mode: OPENAI (GPT-4o-mini)"
        echo "💰 Cost: ~$0.002 per 1K tokens"
    else
        echo "🖥️  Mode: LOCAL (Ollama)"
        echo "💰 Cost: FREE"
    fi
else
    echo "❌ ECH0 is NOT running"
fi

echo ""
echo "📦 Available Local Models:"
echo "=========================="
ollama list | grep -E "qwen2.5|llama" | awk '{print "• "$1" ("$3")"}'

echo ""
echo "🔄 Currently Loaded in Ollama:"
echo "=============================="
loaded=$(curl -s http://localhost:11434/api/ps | python3 -c "import json, sys; data = json.load(sys.stdin); print(data['models'][0]['name'] if data.get('models') else 'None')" 2>/dev/null)
if [ "$loaded" = "None" ]; then
    echo "❌ No model currently loaded"
else
    echo "✅ $loaded"
fi

echo ""
echo "💡 To switch to 14B local model, run:"
echo "   ./SWITCH_TO_14B_MODEL.sh"