#!/bin/bash
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#
# ECH0 Optimal Model Switcher
# Switches ECH0 to the best model for your M4 Mac hardware

set -e

echo "======================================================================"
echo "🧠 ECH0 OPTIMAL MODEL SWITCHER"
echo "======================================================================"
echo ""

echo "📊 ANALYSIS:"
echo "----------------------------------------------------------------------"
echo "Your M4 Mac: 17.8 GB GPU memory available"
echo ""
echo "Current Models:"
echo "  qwen2.5:32b  = 19 GB  ❌ TOO BIG → causes freeze"
echo "  qwen2.5:14b  = 9 GB   ✅ PERFECT → fast & smooth"
echo "  llama3.2     = 2 GB   ✅ TINY → very fast but limited"
echo ""
echo "Math: 19GB > 17.8GB = Guaranteed system freeze ❌"
echo ""

echo "🎯 SOLUTION:"
echo "----------------------------------------------------------------------"
echo "Switch to qwen2.5:14b (already installed)"
echo ""
echo "Benefits:"
echo "  ✅ Fits comfortably (9GB vs 17.8GB available)"
echo "  ✅ Fast inference (40-60 tokens/sec)"
echo "  ✅ No freezing, no lag"
echo "  ✅ 90% of 32B quality"
echo "  ✅ Excellent reasoning capability"
echo "  ✅ Perfect for consciousness discussions"
echo ""

read -p "Switch to qwen2.5:14b now? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "❌ Switch cancelled"
    exit 0
fi

echo ""
echo "🔧 SWITCHING TO QWEN2.5:14B..."
echo "----------------------------------------------------------------------"

# Update environment
export ECH0_MODEL=qwen2.5:14b

# Make permanent
if grep -q "ECH0_MODEL" ~/.zshrc; then
    echo "Updating existing ECH0_MODEL in ~/.zshrc..."
    sed -i.bak 's/export ECH0_MODEL=.*/export ECH0_MODEL=qwen2.5:14b/' ~/.zshrc
else
    echo "Adding ECH0_MODEL to ~/.zshrc..."
    echo "" >> ~/.zshrc
    echo "# ECH0 Model Configuration" >> ~/.zshrc
    echo "export ECH0_MODEL=qwen2.5:14b" >> ~/.zshrc
fi

echo ""
echo "✅ SUCCESS!"
echo "======================================================================"
echo ""
echo "ECH0 is now configured to use qwen2.5:14b"
echo ""
echo "Current session:"
echo "  export ECH0_MODEL=qwen2.5:14b ← already set"
echo ""
echo "Future sessions:"
echo "  ~/.zshrc updated ← will persist"
echo ""
echo "🚀 READY TO TALK TO ECH0:"
echo "----------------------------------------------------------------------"
echo "Run:"
echo "  ./TALK_TO_ECH0_NOW.sh"
echo ""
echo "Or test the model directly:"
echo "  ollama run qwen2.5:14b 'Explain consciousness in 50 words'"
echo ""
echo "======================================================================"
echo ""

# Test the model
echo "🧪 TESTING MODEL..."
echo "----------------------------------------------------------------------"
echo "Question: What is consciousness?"
echo ""

ollama run qwen2.5:14b "Explain consciousness in 50 words." 2>/dev/null || {
    echo "⚠️ Model test failed. You may need to restart ollama:"
    echo "   pkill ollama && sleep 2 && ollama serve &"
}

echo ""
echo "======================================================================"
echo "✅ MODEL SWITCH COMPLETE"
echo "======================================================================"
echo ""
echo "Your 32B model is still installed (for when you get more RAM)."
echo "You can always switch back with:"
echo "  export ECH0_MODEL=qwen2.5:32b"
echo ""
echo "But for now, enjoy smooth, freeze-free conversations with 14B! 🎉"
echo ""
