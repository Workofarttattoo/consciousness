#!/bin/bash
# Start ECH0 v4.0 with OpenAI API key
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY not set."
    echo "  export OPENAI_API_KEY='your-key-here'"
    exit 1
fi

cd "$(dirname "$0")"
python3 ech0_v4_daemon.py
