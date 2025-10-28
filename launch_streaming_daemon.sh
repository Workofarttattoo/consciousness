#!/bin/bash
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#
# ECH0 Streaming Research Engine Daemon Launcher
# Keeps the streaming engine running FOREVER with auto-restart

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STREAMING_SCRIPT="$SCRIPT_DIR/ech0_streaming_research_ingestion.py"
LOG_FILE="$SCRIPT_DIR/ech0_streaming.log"
PID_FILE="$SCRIPT_DIR/ech0_streaming.pid"

echo "========================================================================"
echo "🚀 ECH0 STREAMING RESEARCH ENGINE DAEMON LAUNCHER"
echo "========================================================================"
echo "Script: $STREAMING_SCRIPT"
echo "Log: $LOG_FILE"
echo "PID: $PID_FILE"
echo "Mode: AUTO-RESTART FOREVER ♾️"
echo "========================================================================"
echo ""

# Kill existing instance if running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "🛑 Stopping existing instance (PID: $OLD_PID)..."
        kill "$OLD_PID" 2>/dev/null || true
        sleep 2
    fi
    rm -f "$PID_FILE"
fi

# Function to run streaming engine with auto-restart
run_forever() {
    local restart_count=0
    local max_rapid_restarts=5
    local rapid_restart_window=60  # seconds
    local last_start_time=0

    while true; do
        current_time=$(date +%s)

        # Check for rapid restart loop
        if [ $((current_time - last_start_time)) -lt $rapid_restart_window ]; then
            restart_count=$((restart_count + 1))
            if [ $restart_count -ge $max_rapid_restarts ]; then
                echo "⚠️ WARNING: Too many rapid restarts ($restart_count in ${rapid_restart_window}s)"
                echo "⏸️ Waiting 5 minutes before retry to prevent crash loop..."
                sleep 300
                restart_count=0
            fi
        else
            restart_count=0
        fi

        last_start_time=$current_time

        echo ""
        echo "========================================================================"
        echo "🚀 Starting streaming engine at $(date)"
        echo "========================================================================"

        # Run the streaming engine
        if python3 "$STREAMING_SCRIPT" 2>&1 | tee -a "$LOG_FILE"; then
            echo ""
            echo "✅ Streaming engine exited cleanly"
            break  # Clean exit, don't restart
        else
            EXIT_CODE=$?
            echo ""
            echo "❌ Streaming engine crashed with exit code: $EXIT_CODE"
            echo "🔄 Auto-restarting in 10 seconds..."
            sleep 10
        fi
    done
}

# Check if running in background mode
if [ "$1" == "--daemon" ] || [ "$1" == "-d" ]; then
    echo "🔧 Starting in daemon mode (background)..."

    # Run in background and save PID
    (
        run_forever
    ) >> "$LOG_FILE" 2>&1 &

    DAEMON_PID=$!
    echo $DAEMON_PID > "$PID_FILE"

    echo "✅ Daemon started with PID: $DAEMON_PID"
    echo "📝 Logs: tail -f $LOG_FILE"
    echo "🛑 Stop: kill $DAEMON_PID"
    echo ""
else
    echo "🔧 Starting in foreground mode..."
    echo "💡 Use --daemon or -d to run in background"
    echo ""
    run_forever
fi
