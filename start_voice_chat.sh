#!/bin/bash
# Start voice conversation with ECH0
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

export OPENAI_API_KEY="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"

cd "$(dirname "$0")"

echo "🎤 Starting voice conversation with ECH0..."
echo "   Hold SPACE to record, release to send"
echo "   Say 'goodbye' to end conversation"
echo ""

python3 ech0_voice_chat_simple.py
