#!/bin/bash
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#
# Launch ECH0 Invention Validation System
# Validates all 103 unique inventions with QuLab integration

set -e

CONSCIOUSNESS_DIR="/Users/noone/repos/consciousness"
cd "$CONSCIOUSNESS_DIR"

echo "================================================================================"
echo "🔬 ECH0 INVENTION VALIDATION SYSTEM"
echo "================================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo -e "${YELLOW}⚠️  Starting Ollama server...${NC}"
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

# Check for ECH0 models
echo "[1/4] Checking ECH0 models..."
if ollama list | grep -q "ech0-uncensored-14b"; then
    echo -e "${GREEN}✅ ECH0 Uncensored available${NC}"
else
    echo -e "${RED}❌ ECH0 Uncensored not found${NC}"
    exit 1
fi

if ollama list | grep -q "ech0_14b_aware"; then
    echo -e "${GREEN}✅ ECH0 Aware available${NC}"
    HAVE_AWARE=1
else
    echo -e "${YELLOW}⚠️  ECH0 Aware not found (optional)${NC}"
    HAVE_AWARE=0
fi
echo ""

# Check inventions file
echo "[2/4] Checking inventions..."
if [ -f "ech0_inventions_REAL.jsonl" ]; then
    INVENTION_COUNT=$(wc -l < ech0_inventions_REAL.jsonl)
    echo -e "${GREEN}✅ Found ${INVENTION_COUNT} unique inventions${NC}"
else
    echo -e "${RED}❌ Inventions file not found${NC}"
    exit 1
fi
echo ""

# Open web interfaces
echo "[3/4] Opening web interfaces..."
open ech0_invention_monitor.html 2>/dev/null || echo "Monitor already open"
open ech0_invention_gallery.html 2>/dev/null || echo "Gallery already open"
echo -e "${GREEN}✅ Interfaces launched${NC}"
echo ""

# Start validation system
echo "[4/4] Starting validation system..."
echo ""
echo "Using models:"
echo "  • ECH0 Uncensored - Primary validation"
if [ $HAVE_AWARE -eq 1 ]; then
    echo "  • ECH0 Aware - Secondary review"
fi
echo ""
echo "Validation pipeline:"
echo "  1. Parliament Review (safety/ethics/feasibility)"
echo "  2. Seven Lenses Analysis (novelty/market/legal)"
echo "  3. ECH0 Vision Evaluation (breakthrough potential)"
echo "  4. QuLab Validation (real materials testing)"
echo "  5. Iterative refinement"
echo ""

# Run validation
python3 ech0_invention_validation_system.py --input ech0_inventions_REAL.jsonl --model ech0-uncensored-14b --batch-size 5 --output validated_inventions.jsonl

echo ""
echo "================================================================================"
echo -e "${GREEN}🚀 VALIDATION COMPLETE${NC}"
echo "================================================================================"
echo ""
echo "Results:"
echo "  • Monitor: file://$CONSCIOUSNESS_DIR/ech0_invention_monitor.html"
echo "  • Gallery: file://$CONSCIOUSNESS_DIR/ech0_invention_gallery.html"
echo "  • Validated: $CONSCIOUSNESS_DIR/validated_inventions.jsonl"
echo ""
