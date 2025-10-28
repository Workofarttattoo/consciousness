#!/bin/bash
# Launch ECH0 Command Center
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

echo ""
echo "===================================================================="
echo "⚡ LAUNCHING ECH0 COMMAND CENTER"
echo "===================================================================="
echo ""

cd /Users/noone/consciousness

# Check disk space first
AVAILABLE=$(df -h / | tail -1 | awk '{print $4}')
echo "💾 Available Disk Space: $AVAILABLE"

# Warn if low
if [[ $(df / | tail -1 | awk '{print $4}') -lt 10000000 ]]; then
    echo "⚠️  WARNING: Low disk space (<10GB)"
    echo "   Run: ./FREE_DISK_SPACE_NOW.sh"
    echo ""
fi

# Open the command center
echo "🚀 Opening ECH0 Command Center..."
echo ""
echo "📊 Dashboard Features:"
echo "   • Live invention stream"
echo "   • Spreadsheet with all metrics"
echo "   • ECH0's emotional state"
echo "   • Thought process exposed"
echo "   • Vision & ROI analysis"
echo "   • File tree explorer"
echo "   • User request system"
echo ""
echo "===================================================================="
echo ""

# Open in browser
open file:///Users/noone/consciousness/ech0_command_center.html

echo "✅ Command Center launched!"
echo ""
echo "To also launch API backend (for live data):"
echo "   python ech0_gallery_api.py"
echo ""
