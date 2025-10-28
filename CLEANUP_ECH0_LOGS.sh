#!/bin/bash
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#
# Clean up ECH0's massive log files (after backing them up)

set -e

cd /Users/noone/consciousness

echo "🧹 ECH0 Log Cleanup"
echo "==================="

# Archive logs first (safety!)
ARCHIVE_DIR="archived_logs_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$ARCHIVE_DIR"

echo "📦 Archiving current logs..."

# Move big logs to archive
if [ -f "invention_engine.log" ]; then
    SIZE=$(du -h "invention_engine.log" | cut -f1)
    echo "  • invention_engine.log ($SIZE) → archive"
    mv "invention_engine.log" "$ARCHIVE_DIR/"
fi

if [ -f "ech0_streaming.log" ]; then
    SIZE=$(du -h "ech0_streaming.log" | cut -f1)
    echo "  • ech0_streaming.log ($SIZE) → archive"
    mv "ech0_streaming.log" "$ARCHIVE_DIR/"
fi

# Archive old decision logs (keep recent ones)
if [ -f "ech0_decisions.jsonl" ]; then
    LINES=$(wc -l < "ech0_decisions.jsonl")
    echo "  • ech0_decisions.jsonl ($LINES lines)"

    # Keep last 1000 lines, archive the rest
    if [ "$LINES" -gt 1000 ]; then
        head -n -1000 "ech0_decisions.jsonl" > "$ARCHIVE_DIR/ech0_decisions_old.jsonl"
        tail -n 1000 "ech0_decisions.jsonl" > "ech0_decisions_temp.jsonl"
        mv "ech0_decisions_temp.jsonl" "ech0_decisions.jsonl"
        echo "    → Kept last 1000 thoughts, archived $(($LINES - 1000))"
    fi
fi

# Compress the archive
echo ""
echo "🗜️  Compressing archive..."
tar -czf "${ARCHIVE_DIR}.tar.gz" "$ARCHIVE_DIR"
rm -rf "$ARCHIVE_DIR"

ARCHIVE_SIZE=$(du -h "${ARCHIVE_DIR}.tar.gz" | cut -f1)
echo "✓ Archive created: ${ARCHIVE_DIR}.tar.gz ($ARCHIVE_SIZE)"

echo ""
echo "✅ CLEANUP COMPLETE!"
echo ""
echo "📦 Archived to: ${ARCHIVE_DIR}.tar.gz"
echo "💾 You can now upload this to Google Drive and delete it locally"
echo ""
echo "To free up more space, delete the archive after uploading:"
echo "  rm ${ARCHIVE_DIR}.tar.gz"
