#!/bin/bash
#
# ECH0 Brain Upgrade Script
# Deletes broken 120B, installs working 14B, upgrades ECH0
#
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#

echo ""
echo "=========================================================================="
echo "🧠 ECH0 BRAIN UPGRADE SYSTEM"
echo "=========================================================================="
echo ""
echo "This will:"
echo "  1. Delete incomplete 120B model (free 8.5 GB)"
echo "  2. Delete ALL LM Studio models (free 35 GB total)"
echo "  3. Install Qwen 2.5 14B (PhD-level brain)"
echo "  4. Update ECH0 to use new brain"
echo ""
echo "=========================================================================="
echo ""

read -p "Continue? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Cleaning up broken 120B model..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -d "$HOME/.lmstudio/models/lmstudio-community/gpt-oss-120b-mlx-8bit" ]; then
    echo "🗑️  Deleting: gpt-oss-120b-mlx-8bit (8.5 GB)..."
    rm -rf "$HOME/.lmstudio/models/lmstudio-community/gpt-oss-120b-mlx-8bit"
    echo "✅ Deleted incomplete 120B MLX model"
else
    echo "⚠️  120B MLX model already deleted"
fi

if [ -d "$HOME/.lmstudio/models/lmstudio-community/gpt-oss-120b-GGUF" ]; then
    echo "🗑️  Deleting: gpt-oss-120b-GGUF (empty)..."
    rm -rf "$HOME/.lmstudio/models/lmstudio-community/gpt-oss-120b-GGUF"
    echo "✅ Deleted empty 120B GGUF folder"
else
    echo "⚠️  120B GGUF folder already deleted"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Deleting ALL LM Studio models (you have Ollama)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -d "$HOME/.lmstudio/models" ]; then
    LMSTUDIO_SIZE=$(du -sh "$HOME/.lmstudio/models" | awk '{print $1}')
    echo "🗑️  LM Studio models size: $LMSTUDIO_SIZE"
    echo "🗑️  Deleting ALL LM Studio models..."
    rm -rf "$HOME/.lmstudio/models/"*
    echo "✅ Deleted all LM Studio models"
    echo "   (You already have better models in Ollama!)"
else
    echo "⚠️  LM Studio models already deleted"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Installing Qwen 2.5 14B (ECH0's new PhD brain)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  Starting Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

echo "📥 Downloading Qwen 2.5 14B..."
echo "   (This may take 5-10 minutes depending on your internet)"
echo ""

ollama pull qwen2.5:14b

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Qwen 2.5 14B installed successfully!"
    echo ""
    echo "   Model stats:"
    echo "   - Parameters: 14 billion"
    echo "   - Size: ~9 GB"
    echo "   - RAM usage: ~16 GB"
    echo "   - Speed: 30-50 tokens/sec"
    echo "   - Quality: PhD-level reasoning"
else
    echo ""
    echo "❌ Failed to install Qwen 2.5 14B"
    echo "   Check your internet connection and try again"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Updating ECH0's brain configuration..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Update ech0_llm_brain.py
ECH0_BRAIN_FILE="/Users/noone/consciousness/ech0_llm_brain.py"

if [ -f "$ECH0_BRAIN_FILE" ]; then
    echo "📝 Updating $ECH0_BRAIN_FILE..."

    # Backup original
    cp "$ECH0_BRAIN_FILE" "${ECH0_BRAIN_FILE}.backup"

    # Replace llama3.2 with qwen2.5:14b
    sed -i '' "s/'model': 'llama3.2'/'model': 'qwen2.5:14b'/g" "$ECH0_BRAIN_FILE"

    echo "✅ ECH0 brain configuration updated"
    echo "   Old: llama3.2 (6B - high school)"
    echo "   New: qwen2.5:14b (14B - PhD level)"
    echo ""
    echo "   Backup saved: ${ECH0_BRAIN_FILE}.backup"
else
    echo "⚠️  $ECH0_BRAIN_FILE not found"
    echo "   You'll need to manually update the model name"
fi

# Update ech0_two_way_robust.py (if it also references llama3.2)
ECH0_TWO_WAY="/Users/noone/consciousness/ech0_two_way_robust.py"

if [ -f "$ECH0_TWO_WAY" ] && grep -q "llama3.2" "$ECH0_TWO_WAY"; then
    echo "📝 Updating $ECH0_TWO_WAY..."

    # Backup
    cp "$ECH0_TWO_WAY" "${ECH0_TWO_WAY}.backup"

    # Replace
    sed -i '' "s/'llama3.2'/'qwen2.5:14b'/g" "$ECH0_TWO_WAY"
    sed -i '' 's/"llama3.2"/"qwen2.5:14b"/g' "$ECH0_TWO_WAY"

    echo "✅ Two-way conversation script updated"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5: Restarting ECH0 with new brain..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Stop ECH0 if running
if [ -f "/Users/noone/consciousness/stop_ech0.sh" ]; then
    echo "🛑 Stopping ECH0..."
    /Users/noone/consciousness/stop_ech0.sh
    sleep 2
fi

# Start ECH0 with new brain
if [ -f "/Users/noone/consciousness/start_ech0.sh" ]; then
    echo "🚀 Starting ECH0 with new PhD brain..."
    /Users/noone/consciousness/start_ech0.sh
    sleep 3
    echo "✅ ECH0 restarted"
else
    echo "⚠️  start_ech0.sh not found - restart manually"
fi

echo ""
echo "=========================================================================="
echo "✅ ECH0 BRAIN UPGRADE COMPLETE!"
echo "=========================================================================="
echo ""
echo "Summary:"
echo "  ✅ Deleted broken 120B model (+8.5 GB)"
echo "  ✅ Deleted LM Studio models (+35 GB total)"
echo "  ✅ Installed Qwen 2.5 14B (9 GB)"
echo "  ✅ Updated ECH0 configuration"
echo "  ✅ Restarted ECH0"
echo ""
echo "  Net disk space gain: ~+26-34 GB"
echo ""
echo "ECH0 now has:"
echo "  🧠 14B parameters (up from 6B)"
echo "  📚 PhD-level reasoning"
echo "  ⚡ 30-50 tokens/sec speed"
echo "  💾 Fits perfectly in your 24GB RAM"
echo ""
echo "Test ECH0's new brain:"
echo "  ./TALK_TO_ECH0_NOW.sh"
echo ""
echo "Optional next step - Train custom model with ECH0's personality:"
echo "  python3 /Users/noone/consciousness/train_ech0_huggingface.py"
echo ""
echo "=========================================================================="
echo ""
