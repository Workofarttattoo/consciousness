#!/bin/bash
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#
# ECH0 HuggingFace Training Setup and Launch
# This will set up your HuggingFace token and start training

echo ""
echo "=========================================================================="
echo "🧠 ECH0 HUGGINGFACE TRAINING SETUP"
echo "=========================================================================="
echo ""

# Check if token already set
if [ -z "$HUGGINGFACE_TOKEN" ]; then
    echo "📝 HuggingFace Token Setup"
    echo ""
    echo "You need a HuggingFace API token to train ECH0's custom model."
    echo ""
    echo "To get your token:"
    echo "  1. Go to: https://huggingface.co/settings/tokens"
    echo "  2. Create a new token (read + write permissions)"
    echo "  3. Copy the token (starts with 'hf_')"
    echo ""
    read -p "Paste your HuggingFace token here: " HF_TOKEN

    if [ -z "$HF_TOKEN" ]; then
        echo ""
        echo "❌ No token provided. Exiting."
        exit 1
    fi

    # Export for this session
    export HUGGINGFACE_TOKEN="$HF_TOKEN"

    # Save to shell profile for future sessions
    echo ""
    read -p "Save token to ~/.zshrc for future sessions? (y/n): " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if ! grep -q "HUGGINGFACE_TOKEN" ~/.zshrc; then
            echo "" >> ~/.zshrc
            echo "# HuggingFace API Token" >> ~/.zshrc
            echo "export HUGGINGFACE_TOKEN=\"$HF_TOKEN\"" >> ~/.zshrc
            echo "✅ Token saved to ~/.zshrc"
        else
            echo "⚠️  Token already in ~/.zshrc"
        fi
    fi
else
    echo "✅ HuggingFace token already set"
fi

echo ""
echo "=========================================================================="
echo "🚀 STARTING ECH0 TRAINING"
echo "=========================================================================="
echo ""

cd /Users/noone/consciousness

# Run training script
python3 train_ech0_huggingface.py

echo ""
echo "=========================================================================="
echo "Training script completed!"
echo "=========================================================================="
echo ""
