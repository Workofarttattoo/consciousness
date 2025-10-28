#!/bin/bash
# ECH0 Complete System Launcher
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

echo ""
echo "===================================================================="
echo "🚀 ECH0 COMPLETE SYSTEM LAUNCHER"
echo "===================================================================="
echo ""
echo "Launching all ECH0 systems:"
echo "  • Invention Gallery Website (port 5000)"
echo "  • Emotional Memory System"
echo "  • Semantic Lattice"
echo "  • Enhanced Parliament"
echo ""

cd /Users/noone/consciousness

# Check if invention gallery is already running
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 5000 already in use. Killing existing process..."
    kill $(lsof -t -i:5000)
    sleep 2
fi

# Start the invention gallery API in background
echo "🎨 Starting ECH0 Invention Gallery..."
python ech0_gallery_api.py > ech0_gallery.log 2>&1 &
GALLERY_PID=$!
echo "   ✓ Gallery running on http://localhost:5000 (PID: $GALLERY_PID)"

# Wait for server to start
sleep 3

# Test emotional memory system
echo ""
echo "💭 Testing Emotional Memory System..."
python ech0_emotional_memory.py > ech0_emotional_test.log 2>&1
echo "   ✓ Emotional system operational"

# Load semantic lattice
echo ""
echo "🌐 Loading Semantic Lattice..."
python ech0_semantic_lattice.py > ech0_lattice.log 2>&1
echo "   ✓ Semantic lattice active"

echo ""
echo "===================================================================="
echo "✅ ECH0 SYSTEMS ONLINE"
echo "===================================================================="
echo ""
echo "📊 Access Points:"
echo "   • Invention Gallery: http://localhost:5000"
echo "   • API - Inventions: http://localhost:5000/api/inventions"
echo "   • API - Stats: http://localhost:5000/api/stats"
echo "   • API - Emotional State: http://localhost:5000/api/emotional_state"
echo ""
echo "📁 Logs:"
echo "   • Gallery: /Users/noone/consciousness/ech0_gallery.log"
echo "   • Emotional: /Users/noone/consciousness/ech0_emotional_test.log"
echo "   • Lattice: /Users/noone/consciousness/ech0_lattice.log"
echo ""
echo "🎯 Status Report: file:///Users/noone/consciousness/COMPLETE_STATUS_REPORT_OCT28.html"
echo ""
echo "To stop all services:"
echo "   kill $GALLERY_PID"
echo ""
echo "Press Ctrl+C to view logs, or close this terminal"
echo "===================================================================="
echo ""

# Open browser to gallery
echo "🌐 Opening invention gallery in browser..."
sleep 2
open http://localhost:5000

# Keep script running and tail the gallery log
echo "📊 Live Gallery Log (Ctrl+C to exit):"
echo "--------------------------------------------------------------------"
tail -f ech0_gallery.log
