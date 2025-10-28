#!/usr/bin/env python3
"""
ECH0 Auto-Stream to Google Drive
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Continuously monitors ECH0's outputs and streams them to Google Drive
"""

import os
import time
import shutil
import json
from pathlib import Path
from datetime import datetime
import subprocess

# Configuration
ECH0_PATH = Path("/Users/noone/consciousness")

# Detect Google Drive path (new Google Drive for Desktop location)
GDRIVE_CANDIDATES = [
    Path.home() / "Library" / "CloudStorage" / "GoogleDrive-thewhiteknight702@gmail.com" / "My Drive",
    Path.home() / "Google Drive" / "My Drive",
    Path.home() / "GoogleDrive" / "My Drive",
]

GDRIVE_BASE = None
for candidate in GDRIVE_CANDIDATES:
    if candidate.exists():
        GDRIVE_BASE = candidate
        break

if GDRIVE_BASE is None:
    # Fallback: use the symlink
    GDRIVE_BASE = Path.home() / "Google Drive" / "My Drive"

GDRIVE_PATH = GDRIVE_BASE / "ECH0_Backups"

# Files to monitor and sync
WATCH_FILES = {
    "ech0_decisions.jsonl": "logs/",
    "ech0_activity_log.jsonl": "logs/",
    "ech0_inventions.jsonl": "inventions/",
    "ech0_theme_park_inventions.jsonl": "inventions/",
    "ech0_research_database_real.jsonl": "research/",
    "ech0_conversation_memory.json": "conversations/",
    "invention_engine.log": "logs/",
    "ech0_streaming.log": "logs/",
}

# Size threshold for log rotation (50 MB)
MAX_LOG_SIZE = 50 * 1024 * 1024

class ECH0Streamer:
    def __init__(self):
        self.last_sync = {}
        self.setup_gdrive()

    def setup_gdrive(self):
        """Create Google Drive directory structure"""
        print(f"🔍 Looking for Google Drive...")
        print(f"   Found: {GDRIVE_BASE}")

        if not GDRIVE_BASE.exists():
            print("❌ Google Drive not found. Please install Google Drive Desktop.")
            print("   https://www.google.com/drive/download/")
            print(f"   Checked: {GDRIVE_CANDIDATES}")
            exit(1)

        # Create subdirectories
        for subdir in ["logs", "inventions", "research", "conversations", "archives"]:
            (GDRIVE_PATH / subdir).mkdir(parents=True, exist_ok=True)

        print(f"✓ Google Drive backup location: {GDRIVE_PATH}")

    def get_file_age(self, filepath):
        """Get seconds since file was modified"""
        if not filepath.exists():
            return float('inf')
        return time.time() - filepath.stat().st_mtime

    def rotate_large_logs(self, filepath):
        """Rotate log files that are too large"""
        if not filepath.exists():
            return

        size = filepath.stat().st_size
        if size > MAX_LOG_SIZE:
            print(f"📦 Rotating large log: {filepath.name} ({size / 1024 / 1024:.1f} MB)")

            # Archive with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"{filepath.stem}_{timestamp}{filepath.suffix}"
            archive_path = GDRIVE_PATH / "archives" / archive_name

            # Copy to archive
            shutil.copy2(filepath, archive_path)
            print(f"  → Archived to {archive_path.name}")

            # Truncate original (keep empty for new logs)
            filepath.write_text("")
            print(f"  → Truncated {filepath.name}")

    def sync_file(self, filename, gdrive_subdir):
        """Sync a single file to Google Drive"""
        src = ECH0_PATH / filename

        if not src.exists():
            return

        # Check if file has been modified since last sync
        age = self.get_file_age(src)
        last_sync_time = self.last_sync.get(filename, float('inf'))

        if age > last_sync_time:
            return  # File hasn't changed since last sync

        # Rotate if too large
        if filename.endswith('.log'):
            self.rotate_large_logs(src)

        # Sync to Google Drive
        dest_dir = GDRIVE_PATH / gdrive_subdir
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / filename

        try:
            shutil.copy2(src, dest)
            self.last_sync[filename] = age

            # Get file size for display
            size = src.stat().st_size
            size_str = f"{size / 1024:.1f} KB" if size < 1024*1024 else f"{size / 1024 / 1024:.1f} MB"

            print(f"✓ {filename} → {gdrive_subdir} ({size_str})")

        except Exception as e:
            print(f"⚠️  Failed to sync {filename}: {e}")

    def run_continuous(self, interval=60):
        """Run continuous sync every N seconds"""
        print("🔄 ECH0 Auto-Stream to Google Drive")
        print("=" * 50)
        print(f"Syncing every {interval} seconds")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        print()

        sync_count = 0

        try:
            while True:
                sync_count += 1
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n[{timestamp}] Sync #{sync_count}")
                print("-" * 50)

                # Sync all monitored files
                for filename, gdrive_subdir in WATCH_FILES.items():
                    self.sync_file(filename, gdrive_subdir)

                print(f"\n💤 Sleeping for {interval} seconds...")
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\n👋 Stopped auto-sync")
            print(f"Total syncs performed: {sync_count}")

def main():
    streamer = ECH0Streamer()

    # Run every 60 seconds by default
    # Change to 300 (5 min) for less frequent syncing
    streamer.run_continuous(interval=60)

if __name__ == "__main__":
    main()
