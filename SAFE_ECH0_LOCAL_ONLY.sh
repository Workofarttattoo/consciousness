#!/bin/bash
# ECH0 Voice Chat - 100% FREE LOCAL VERSION
# NO ANTHROPIC API CALLS = NO CHARGES!

clear
echo "========================================================================"
echo "💚 ECH0 VOICE CHAT - 100% FREE LOCAL MODE"
echo "========================================================================"
echo ""
echo "✅ Using LOCAL Qwen model (NO API costs)"
echo "✅ NO Anthropic API calls"
echo "✅ Completely FREE"
echo ""
echo "Improvements:"
echo "  • Silence duration: 3.5 seconds (more time to speak)"
echo "  • Temperature: 1.1 (more personality)"
echo "  • Enhanced warmth in system prompt"
echo "  • Nucleus sampling for natural variation"
echo ""
echo "========================================================================"
echo ""

cd /Users/noone/consciousness

# Make SURE we don't use Anthropic API
unset USE_ANTHROPIC
unset ANTHROPIC_API_KEY

# Use improved local version
python3 ech0_two_way_robust.py
