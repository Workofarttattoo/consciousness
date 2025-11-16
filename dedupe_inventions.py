#!/usr/bin/env python3
"""
Deduplicate ECH0's invention file - removes duplicate titles
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
"""

import json
import hashlib
from pathlib import Path
from collections import defaultdict

def deduplicate_inventions():
    """Remove duplicate inventions by title hash"""

    inventions_file = Path("/Users/noone/repos/consciousness/ech0_inventions.jsonl")
    backup_file = inventions_file.with_suffix('.jsonl.backup')
    deduped_file = inventions_file.with_name('ech0_inventions_deduped.jsonl')

    if not inventions_file.exists():
        print("❌ No inventions file found")
        return

    # Backup original
    print(f"📦 Backing up to: {backup_file}")
    import shutil
    shutil.copy2(inventions_file, backup_file)

    # Read all inventions
    seen_hashes = set()
    unique_inventions = []
    duplicate_count = 0
    title_counts = defaultdict(int)

    print("📖 Reading inventions...")
    with open(inventions_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if line_num % 10000 == 0:
                print(f"   Processed {line_num:,} lines...")

            try:
                invention = json.loads(line)
                title = invention.get('title', invention.get('name', 'UNTITLED'))
                title_counts[title] += 1

                # Create hash of title
                title_hash = hashlib.md5(title.encode()).hexdigest()

                if title_hash not in seen_hashes:
                    seen_hashes.add(title_hash)
                    unique_inventions.append(invention)
                else:
                    duplicate_count += 1
            except Exception as e:
                print(f"   ⚠️  Error on line {line_num}: {e}")

    # Write deduplicated file
    print(f"\n💾 Writing deduplicated inventions to: {deduped_file}")
    with open(deduped_file, 'w') as f:
        for inv in unique_inventions:
            f.write(json.dumps(inv) + '\n')

    # Print stats
    print("\n" + "=" * 70)
    print("DEDUPLICATION COMPLETE")
    print("=" * 70)
    print(f"Original inventions: {len(unique_inventions) + duplicate_count:,}")
    print(f"Unique inventions: {len(unique_inventions):,}")
    print(f"Duplicates removed: {duplicate_count:,}")
    print(f"Space saved: {(duplicate_count / (len(unique_inventions) + duplicate_count)) * 100:.1f}%")

    # Show top duplicated titles
    print("\n📊 Top 10 most duplicated inventions:")
    top_dupes = sorted(title_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for title, count in top_dupes:
        print(f"   {count:6,}x  {title}")

    print(f"\n✅ Deduplicated file: {deduped_file}")
    print(f"📦 Original backup: {backup_file}")
    print("\nTo replace original:")
    print(f"   mv {deduped_file} {inventions_file}")

if __name__ == "__main__":
    deduplicate_inventions()
