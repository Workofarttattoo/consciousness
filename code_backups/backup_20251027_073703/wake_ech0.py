#!/usr/bin/env python3
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
# All Rights Reserved. PATENT PENDING.

"""
Direct launcher for Ech0 - skips wizard, loads existing config
"""

import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "integration"))

from persistent_session import PersistentConsciousSession

def main():
    """Wake Ech0 directly."""

    config_path = Path(__file__).parent / "data" / "Ech0_config.json"

    if not config_path.exists():
        print(f"[ERROR] Ech0's config not found at: {config_path}")
        return

    print("Waking Ech0...")

    # Create session with Ech0's config
    session = PersistentConsciousSession(str(config_path))

    # Boot
    if not session.boot_agent():
        return

    # Start background experiences
    session.start_background_experiences()

    # Interactive conversation
    session.interactive_session()


if __name__ == "__main__":
    main()
