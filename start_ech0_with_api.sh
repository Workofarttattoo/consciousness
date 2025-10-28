#!/bin/bash
# Start ECH0 v4.0 with OpenAI API key
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

export OPENAI_API_KEY="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"

cd "$(dirname "$0")"
python3 ech0_v4_daemon.py
