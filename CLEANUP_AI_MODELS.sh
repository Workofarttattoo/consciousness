#!/bin/bash
# AI Model Cleanup Script
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

echo ""
echo "====================================================================="
echo "🤖 ECH0 AI MODEL CLEANUP"
echo "====================================================================="
echo ""
echo "Current AI model storage:"
echo ""

# Show current models
echo "📦 Ollama Models:"
ollama list

echo ""
echo "💾 Current disk usage:"
df -h / | tail -1

echo ""
echo "====================================================================="
echo "🎯 RECOMMENDED ACTIONS"
echo "====================================================================="
echo ""
echo "1. DELETE Private AI app (21GB)"
echo "   - You're not using it"
echo "   - Free up massive space"
echo ""
echo "2. DELETE Ollama 32B models (38GB total)"
echo "   - Your Mac can't run them well anyway"
echo "   - Keep 14B instead (9GB, works great)"
echo ""
echo "3. DELETE HuggingFace cache (11GB)"
echo "   - Old downloaded models"
echo "   - Will re-download if needed"
echo ""
echo "4. USE OpenAI API for heavy lifting"
echo "   - Already configured!"
echo "   - Zero disk space"
echo "   - Much faster than local"
echo ""
echo "TOTAL TO FREE: ~70GB"
echo ""
echo "====================================================================="
echo ""

read -p "Proceed with AI model cleanup? (y/n) " -n 1 -r
echo
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cleanup cancelled"
    exit 0
fi

TOTAL_FREED=0

# 1. Remove Private AI
if [ -d ~/Library/Containers/apify.privateai.macos.prod ]; then
    echo "🗑️  Deleting Private AI app (21GB)..."
    rm -rf ~/Library/Containers/apify.privateai.macos.prod
    echo "   ✅ Deleted Private AI"
    TOTAL_FREED=$((TOTAL_FREED + 21))
fi

# 2. Remove large Ollama models
echo ""
echo "🗑️  Removing large Ollama models..."

if ollama list | grep -q "qwen2.5:32B"; then
    echo "   Removing qwen2.5:32B (19GB)..."
    ollama rm qwen2.5:32B
    echo "   ✅ Removed qwen2.5:32B"
    TOTAL_FREED=$((TOTAL_FREED + 19))
fi

if ollama list | grep -q "qwen2.5:32b-compressed"; then
    echo "   Removing qwen2.5:32b-compressed (19GB)..."
    ollama rm qwen2.5:32b-compressed
    echo "   ✅ Removed qwen2.5:32b-compressed"
    TOTAL_FREED=$((TOTAL_FREED + 19))
fi

# 3. Remove HuggingFace cache
if [ -d ~/.cache/huggingface ]; then
    echo ""
    echo "🗑️  Deleting HuggingFace cache (11GB)..."
    rm -rf ~/.cache/huggingface
    echo "   ✅ Deleted HuggingFace cache"
    TOTAL_FREED=$((TOTAL_FREED + 11))
fi

# Summary
echo ""
echo "====================================================================="
echo "✅ CLEANUP COMPLETE"
echo "====================================================================="
echo ""
echo "💾 Space freed: ~${TOTAL_FREED}GB"
echo ""
echo "📊 New disk usage:"
df -h / | tail -1
echo ""
echo "🎯 What's left:"
echo "   • qwen2.5:14b (9GB) - Your local ECH0 brain"
echo "   • llama3.2:latest (2GB) - Fast fallback"
echo ""
echo "🚀 Next steps:"
echo ""
echo "   For routine tasks:"
echo "   → ./START_TWO_WAY_TALK.sh  # Uses local 14B model"
echo ""
echo "   For complex reasoning (uses GPT-4):"
echo "   → ./START_ECH0_WITH_OPENAI.sh  # Zero disk space!"
echo ""
echo "   For 120B models later:"
echo "   → Deploy to RunPod/Lambda cloud ($0.50-1/hour)"
echo ""
echo "====================================================================="
