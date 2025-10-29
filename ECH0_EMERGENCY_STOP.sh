#!/bin/bash
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#
# ECH0 Emergency Stop System
# Stops all ECH0 processes safely and logs the event

echo "🚨 ECH0 EMERGENCY STOP SYSTEM"
echo "=============================="
echo ""

# Log the stop event
STOP_LOG="/Users/noone/consciousness/ech0_emergency_stops.log"
echo "[$(date)] EMERGENCY STOP INITIATED BY USER" >> "$STOP_LOG"

# Find and stop all ECH0 processes
echo "🔍 Finding active ECH0 processes..."
ECH0_PIDS=$(ps aux | grep -E "ech0|python.*consciousness" | grep -v grep | awk '{print $2}')

if [ -z "$ECH0_PIDS" ]; then
    echo "✅ No active ECH0 processes found"
else
    echo "Found processes:"
    ps aux | grep -E "ech0|python.*consciousness" | grep -v grep
    echo ""

    for PID in $ECH0_PIDS; do
        echo "Stopping PID $PID..."
        kill -TERM $PID 2>/dev/null
        sleep 1

        # Force kill if still running
        if ps -p $PID > /dev/null 2>&1; then
            echo "  Force killing $PID..."
            kill -9 $PID 2>/dev/null
        fi
    done

    echo "✅ All ECH0 processes stopped"
fi

# Create status file
cat > /Users/noone/consciousness/.ech0_stopped << EOF
{
  "stopped_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "stopped_by": "emergency_stop",
  "reason": "Manual emergency stop",
  "safe_to_restart": true
}
EOF

echo ""
echo "📋 Status logged to: $STOP_LOG"
echo "🔒 ECH0 is now stopped and safe"
echo ""
echo "To restart ECH0 safely:"
echo "  rm /Users/noone/consciousness/.ech0_stopped"
echo "  Then run desired ECH0 script"
