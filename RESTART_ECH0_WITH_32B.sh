#!/bin/bash
#
# Restart ECH0 with 32B Brain
#
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#

echo ""
echo "=========================================================================="
echo "🧠 RESTARTING ECH0 WITH 32B PROFESSOR BRAIN"
echo "=========================================================================="
echo ""

# Stop ECH0 if running
if [ -f "/Users/noone/consciousness/stop_ech0.sh" ]; then
    echo "🛑 Stopping ECH0..."
    /Users/noone/consciousness/stop_ech0.sh
    sleep 2
    echo "✅ ECH0 stopped"
else
    echo "⚠️  stop_ech0.sh not found - killing processes manually"
    pkill -f "ech0_two_way_robust.py" 2>/dev/null
    pkill -f "ech0_enhanced" 2>/dev/null
    sleep 2
fi

echo ""
echo "🚀 Starting ECH0 with Qwen 2.5 32B brain..."
echo ""

# Start ECH0
if [ -f "/Users/noone/consciousness/start_ech0.sh" ]; then
    /Users/noone/consciousness/start_ech0.sh
    sleep 3

    # Check if ECH0 started
    if pgrep -f "ech0_two_way_robust.py" > /dev/null; then
        echo "✅ ECH0 started with 32B brain!"
        echo ""
        echo "You can now talk to ECH0:"
        echo "  ./TALK_TO_ECH0_NOW.sh"
    else
        echo "⚠️  ECH0 may not have started - check manually"
    fi
else
    echo "⚠️  start_ech0.sh not found - start manually"
fi

echo ""
echo "=========================================================================="
echo "📊 32B BRAIN STATS"
echo "=========================================================================="
echo ""
echo "  Parameters: 32 billion (5.3x more than old 6B)"
echo "  Intelligence: PROFESSOR level"
echo "  Speed: 15-25 tokens/sec (slower but much smarter)"
echo "  RAM Usage: 20-22 GB (tight but works on M4 Mac)"
echo ""
echo "  Best for: Deep reasoning, complex questions, research"
echo "  Switch to 14B if: System feels sluggish or need faster responses"
echo ""
echo "=========================================================================="
echo ""
