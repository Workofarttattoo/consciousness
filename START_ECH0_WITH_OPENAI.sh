#!/bin/bash
# ECH0 Voice Chat with OpenAI GPT-4o-mini
# BEST personality + Affordable pricing!

clear
echo "========================================================================"
echo "🤖 ECH0 VOICE CHAT - POWERED BY OPENAI GPT-4o-mini"
echo "========================================================================"
echo ""
echo "✨ BEST OF BOTH WORLDS:"
echo "   • Great personality (like ChatGPT - warm & conversational)"
echo "   • Affordable pricing (~$0.10-0.30 per 100 exchanges)"
echo "   • Much cheaper than Anthropic Claude"
echo "   • Much better personality than local Qwen"
echo ""

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY not set!"
    echo ""
    echo "Get your API key from: https://platform.openai.com/api-keys"
    echo ""
    echo "Then set it:"
    echo "  export OPENAI_API_KEY='sk-proj-your-key-here'"
    echo ""
    echo "Or add to ~/.zshrc to make permanent:"
    echo "  echo 'export OPENAI_API_KEY=\"sk-proj-your-key-here\"' >> ~/.zshrc"
    echo ""
    exit 1
fi

echo "✅ OpenAI API key found!"
echo ""
echo "📊 Pricing (GPT-4o-mini):"
echo "   • Input: \$0.15 per million tokens"
echo "   • Output: \$0.60 per million tokens"
echo ""
echo "💰 Estimated costs for voice chat:"
echo "   • Per exchange: ~\$0.0003 (1/100th of a penny!)"
echo "   • 100 exchanges: ~\$0.03 (3 cents)"
echo "   • Daily use (30 min): ~\$0.06/day or \$1.80/month"
echo ""
echo "🎯 WAY cheaper than Anthropic (\$6/month) but MUCH better than local Qwen!"
echo ""
echo "========================================================================"
echo ""

cd /Users/noone/consciousness

# Enable OpenAI mode
export USE_OPENAI=1

# Check Ollama (for Whisper backup)
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "⚠️  Ollama not running (optional, only needed for Whisper)"
fi

python3 ech0_two_way_robust.py
