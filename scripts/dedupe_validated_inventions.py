#!/usr/bin/env python3
"""Deduplicate ech0_validated_inventions.jsonl in place."""
import argparse
import hashlib
import json
from pathlib import Path

def main(path: Path, backup: bool = True) -> None:
    if not path.exists():
        print(f"File not found: {path}")
        return

    lines = list(path.read_text().splitlines())
    seen_ids = set()
    seen_hashes = set()
    unique_records = []

    for line in lines:
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        invention = data.get("invention", {}) or {}
        inv_id = invention.get("id") or invention.get("name")
        payload_hash = hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()
        if inv_id and inv_id in seen_ids:
            continue
        if payload_hash in seen_hashes:
            continue
        seen_hashes.add(payload_hash)
        if inv_id:
            seen_ids.add(inv_id)
        unique_records.append(json.dumps(data, separators=(",", ":")))

    if backup:
        backup_path = path.with_suffix(path.suffix + ".bak")
        backup_path.write_text("\n".join(lines) + "\n")
        print(f"Backup written to {backup_path}")

    path.write_text("\n".join(unique_records) + "\n")
    print(f"Wrote {len(unique_records)} unique records")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", default="ech0_validated_inventions.jsonl")
    parser.add_argument("--no-backup", action="store_true", help="Do not create .bak copy")
    args = parser.parse_args()

    target = Path(args.file)
    main(target, backup=not args.no_backup)
