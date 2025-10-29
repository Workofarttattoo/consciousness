#!/bin/bash
# Clean up old ECH0 background processes safely

echo "🧹 Cleaning up old ECH0 processes..."
echo ""

# Keep Google Drive sync, stop everything else
ps aux | grep -E "python.*ech0" | grep -v "AUTO_STREAM_TO_GDRIVE" | grep -v grep | while read line; do
    PID=$(echo "$line" | awk '{print $2}')
    CMD=$(echo "$line" | awk '{print $11, $12, $13}')

    echo "Stopping: $CMD (PID: $PID)"
    kill -TERM $PID 2>/dev/null
done

echo ""
echo "✅ Cleanup complete"
echo "   Google Drive sync kept running"
