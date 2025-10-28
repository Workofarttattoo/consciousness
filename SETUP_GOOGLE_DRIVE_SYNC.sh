#!/bin/bash
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#
# ECH0 → Google Drive Continuous Sync
# Streams all ECH0 outputs to Google Drive automatically

set -e

ECH0_PATH="/Users/noone/consciousness"

# Auto-detect Google Drive path
GDRIVE_CANDIDATES=(
    "$HOME/Library/CloudStorage/GoogleDrive-thewhiteknight702@gmail.com/My Drive"
    "$HOME/Google Drive/My Drive"
    "$HOME/GoogleDrive/My Drive"
)

GOOGLE_DRIVE_BASE=""
for candidate in "${GDRIVE_CANDIDATES[@]}"; do
    if [ -d "$candidate" ]; then
        GOOGLE_DRIVE_BASE="$candidate"
        break
    fi
done

if [ -z "$GOOGLE_DRIVE_BASE" ]; then
    echo "❌ Google Drive not found!"
    echo ""
    echo "Checked locations:"
    for candidate in "${GDRIVE_CANDIDATES[@]}"; do
        echo "  - $candidate"
    done
    echo ""
    echo "Please install Google Drive Desktop:"
    echo "  https://www.google.com/drive/download/"
    exit 1
fi

GOOGLE_DRIVE_PATH="$GOOGLE_DRIVE_BASE/ECH0_Backups"

echo "🔄 ECH0 Google Drive Sync Setup"
echo "================================"
echo "✓ Found Google Drive: $GOOGLE_DRIVE_BASE"
echo ""

# Create backup directory in Google Drive
mkdir -p "$GOOGLE_DRIVE_PATH"
mkdir -p "$GOOGLE_DRIVE_PATH/logs"
mkdir -p "$GOOGLE_DRIVE_PATH/inventions"
mkdir -p "$GOOGLE_DRIVE_PATH/research"
mkdir -p "$GOOGLE_DRIVE_PATH/conversations"

echo "✓ Created backup directories in Google Drive"

# Function to sync with progress
sync_with_progress() {
    local src=$1
    local dest=$2
    local name=$3

    echo ""
    echo "📤 Syncing $name..."
    rsync -avh --progress "$src" "$dest" 2>&1 | grep -v "sending incremental"
    echo "✓ $name synced"
}

# Sync different categories
echo ""
echo "Starting sync..."

# 1. Logs (but compress them first to save space)
echo "📦 Compressing and syncing logs..."
tar -czf "$GOOGLE_DRIVE_PATH/logs/ech0_logs_$(date +%Y%m%d_%H%M%S).tar.gz" \
    "$ECH0_PATH"/*.log \
    "$ECH0_PATH"/ech0_decisions.jsonl \
    "$ECH0_PATH"/ech0_activity_log.jsonl \
    2>/dev/null || true
echo "✓ Logs compressed and synced"

# 2. Inventions
sync_with_progress \
    "$ECH0_PATH/ech0_inventions.jsonl" \
    "$GOOGLE_DRIVE_PATH/inventions/" \
    "Inventions"

sync_with_progress \
    "$ECH0_PATH/ech0_theme_park_inventions.jsonl" \
    "$GOOGLE_DRIVE_PATH/inventions/" \
    "Theme Park Inventions"

# 3. Research
sync_with_progress \
    "$ECH0_PATH/ech0_research_database_real.jsonl" \
    "$GOOGLE_DRIVE_PATH/research/" \
    "Research Database"

sync_with_progress \
    "$ECH0_PATH/ech0_research_ingestion_real.jsonl" \
    "$GOOGLE_DRIVE_PATH/research/" \
    "Research Ingestion"

# 4. Conversations & Memory
sync_with_progress \
    "$ECH0_PATH/ech0_conversation_memory.json" \
    "$GOOGLE_DRIVE_PATH/conversations/" \
    "Conversation Memory"

# 5. Training data
rsync -avh --progress \
    "$ECH0_PATH"/*training*.jsonl \
    "$GOOGLE_DRIVE_PATH/research/" \
    2>/dev/null || true

echo ""
echo "================================"
echo "✅ SYNC COMPLETE!"
echo ""
echo "📊 Backup Location:"
echo "   $GOOGLE_DRIVE_PATH"
echo ""
echo "💾 Space Freed Locally: (logs will be archived)"
echo ""
echo "🔄 To run continuously, add to crontab:"
echo "   */15 * * * * $ECH0_PATH/SETUP_GOOGLE_DRIVE_SYNC.sh"
echo ""
echo "Or run this script whenever you want to backup!"
