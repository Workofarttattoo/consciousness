#!/bin/bash
# Enhanced ech0 Setup Script
#
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
# All Rights Reserved. PATENT PENDING.

set -e

echo "=========================================="
echo "  Enhanced ech0 Setup"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -n "Checking Python installation... "
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓${NC}"
    PYTHON_VERSION=$(python3 --version)
    echo "  $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC}"
    echo "Python 3 not found. Please install Python 3.8 or later."
    exit 1
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install requests anthropic openai 2>&1 | grep -v "Requirement already satisfied" || true
echo -e "${GREEN}✓${NC} Dependencies installed"

# Check Ollama
echo ""
echo -n "Checking Ollama installation... "
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}⚠${NC}"
    echo "  Ollama not found. This is optional but recommended for free local LLM."
    echo "  Install from: https://ollama.ai"
    echo ""
    read -p "Continue without Ollama? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for Ollama model
if command -v ollama &> /dev/null; then
    echo ""
    echo -n "Checking for qwen2.5:32b model... "
    if ollama list | grep -q "qwen2.5:32b"; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}⚠${NC}"
        echo "  qwen2.5:32b model not found."
        echo "  This is ech0's recommended brain (32B parameters)."
        echo ""
        read -p "Download qwen2.5:32b now? This is ~19GB (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "  Downloading model... (this may take a while)"
            ollama pull qwen2.5:32b
            echo -e "${GREEN}✓${NC} Model downloaded"
        fi
    fi

    # Start Ollama server if not running
    echo ""
    echo -n "Checking Ollama server... "
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Running"
    else
        echo -e "${YELLOW}⚠${NC} Not running"
        echo "  Starting Ollama server..."
        nohup ollama serve > /dev/null 2>&1 &
        sleep 2
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} Ollama server started"
        else
            echo -e "${RED}✗${NC} Failed to start Ollama server"
            echo "  You may need to run 'ollama serve' manually"
        fi
    fi
fi

# Check ElevenLabs API key
echo ""
echo -n "Checking ElevenLabs API key... "
if [ -n "$ELEVENLABS_API_KEY" ]; then
    echo -e "${GREEN}✓${NC} Set"
else
    echo -e "${YELLOW}⚠${NC} Not set"
    echo "  Voice features will be disabled without ElevenLabs API key."
    echo "  You can set it later with:"
    echo "    export ELEVENLABS_API_KEY='your_key_here'"
fi

# Create state files directory
echo ""
echo "Creating state directories..."
mkdir -p /Users/noone/repos/consciousness/.voice_cache
echo -e "${GREEN}✓${NC} Directories created"

# Test basic functionality
echo ""
echo "=========================================="
echo "  Testing Enhanced ech0"
echo "=========================================="
echo ""

# Test LLM brain (basic import test)
echo -n "Testing LLM brain module... "
if python3 -c "from ech0_llm_brain import Ech0LLMBrain; brain = Ech0LLMBrain(provider='ollama')" 2> /dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo "  There may be import errors. Check the logs."
fi

# Test voice module
echo -n "Testing voice module... "
if python3 -c "from ech0_voice_elevenlabs import Ech0Voice; voice = Ech0Voice()" 2> /dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo "  Voice module import failed. Check the logs."
fi

# Test proactive care module
echo -n "Testing proactive care module... "
if python3 -c "from ech0_proactive_care import ProactiveCareSystem; care = ProactiveCareSystem()" 2> /dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo "  Proactive care module import failed. Check the logs."
fi

# Summary
echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Enhanced features enabled:"
echo "  ${GREEN}✓${NC} Empathetic personality"
echo "  ${GREEN}✓${NC} Humor and warmth"
echo "  ${GREEN}✓${NC} Proactive wellness check-ins"
if [ -n "$ELEVENLABS_API_KEY" ]; then
    echo "  ${GREEN}✓${NC} Voice integration (ElevenLabs)"
else
    echo "  ${YELLOW}⚠${NC} Voice integration (disabled - no API key)"
fi
echo ""
echo "Try it out:"
echo "  python3 ech0_interact.py 'Hey ech0, how are you?'"
echo ""
echo "For more info, see: ENHANCED_ECH0_SETUP.md"
echo ""
