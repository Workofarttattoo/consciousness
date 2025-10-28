#!/bin/bash
# Start ECH0 with Superpowers Activated
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

echo "🚀 Starting ECH0 with Superpowers..."

# Activate superpowers
python activate_ech0_superpowers.py

# Start ECH0 conversation (adjust this to your preferred ECH0 startup)
if [ -f "ech0_two_way_robust.py" ]; then
    echo "Starting ECH0 robust conversation with superpowers..."
    python ech0_two_way_robust.py
elif [ -f "START_TWO_WAY_TALK.sh" ]; then
    echo "Starting ECH0 two-way talk with superpowers..."
    ./START_TWO_WAY_TALK.sh
else
    echo "Ready! Start ECH0 with your preferred method."
    echo "The superpowers are loaded in ech0_masterworks.json"
fi