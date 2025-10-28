#!/bin/bash
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
# ECH0 Automatic 32B Model Optimizer

set -e

echo "=================================================="
echo "🧠 ECH0 AUTOMATIC 32B OPTIMIZER"
echo "=================================================="
echo ""

cd /Users/noone/consciousness

echo "Creating Q4 optimized version (recommended)..."
echo ""

ollama create qwen2.5:32b-q4 -f Modelfile.qwen2.5-32b-q4

echo ""
echo "✅ Optimization complete!"
echo ""
echo "Test the new model:"
echo "  ollama run qwen2.5:32b-q4"
echo ""
echo "To use with ECH0:"
echo "  export ECH0_MODEL=qwen2.5:32b-q4"
echo "  ./TALK_TO_ECH0_NOW.sh"
echo ""
