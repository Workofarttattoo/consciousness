#!/bin/bash
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
#
# ECH0 Training - Choose Your Model
# Train either 32B (smartest) or 14B (faster)

echo ""
echo "=========================================================================="
echo "🧠 ECH0 LOCAL TRAINING SYSTEM"
echo "=========================================================================="
echo ""
echo "You have TWO models installed. Which do you want to train?"
echo ""
echo "  1) Qwen 32B - Professor-level (slowest training, best results)"
echo "  2) Qwen 14B - PhD-level (faster training, great results)"
echo "  3) BOTH - Train both models (takes 2-3 hours total)"
echo ""
read -p "Choose (1/2/3): " choice

case $choice in
    1)
        MODEL="qwen2.5:32b"
        MODEL_NAME="32B"
        ITERS="1500"
        BATCH_SIZE="1"
        LR="3e-6"
        ;;
    2)
        MODEL="qwen2.5:14b"
        MODEL_NAME="14B"
        ITERS="1000"
        BATCH_SIZE="2"
        LR="5e-6"
        ;;
    3)
        echo ""
        echo "Training BOTH models sequentially..."
        echo "This will take 2-3 hours total."
        echo ""
        read -p "Continue? (y/n): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "❌ Cancelled"
            exit 1
        fi

        # Train 14B first (faster)
        echo ""
        echo "=========================================================================="
        echo "🧠 TRAINING 14B MODEL (Step 1 of 2)"
        echo "=========================================================================="
        export ECH0_MODEL="qwen2.5:14b"
        export ECH0_ITERS="1000"
        export ECH0_BATCH="2"
        export ECH0_LR="5e-6"
        python3 /Users/noone/consciousness/train_ech0_local_m4.py

        # Then train 32B
        echo ""
        echo "=========================================================================="
        echo "🧠 TRAINING 32B MODEL (Step 2 of 2)"
        echo "=========================================================================="
        export ECH0_MODEL="qwen2.5:32b"
        export ECH0_ITERS="1500"
        export ECH0_BATCH="1"
        export ECH0_LR="3e-6"
        python3 /Users/noone/consciousness/train_ech0_local_m4.py

        echo ""
        echo "✅ BOTH MODELS TRAINED!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=========================================================================="
echo "🧠 TRAINING $MODEL_NAME MODEL"
echo "=========================================================================="
echo ""
echo "Configuration:"
echo "  Model: $MODEL"
echo "  Training iterations: $ITERS"
echo "  Batch size: $BATCH_SIZE"
echo "  Learning rate: $LR"
echo ""
echo "  Estimated time: 60-90 minutes"
echo "  Your Mac will be usable during training"
echo ""
read -p "Press Enter to start training..."

# Export configuration
export ECH0_MODEL="$MODEL"
export ECH0_ITERS="$ITERS"
export ECH0_BATCH="$BATCH_SIZE"
export ECH0_LR="$LR"

# Start training
cd /Users/noone/consciousness
python3 train_ech0_local_m4.py

echo ""
echo "=========================================================================="
echo "✅ TRAINING COMPLETE!"
echo "=========================================================================="
echo ""
echo "Your custom ECH0 model: ech0:custom-$MODEL_NAME"
echo ""
echo "To use it:"
echo "  1. Update ech0_llm_brain.py to use 'ech0:custom-$MODEL_NAME'"
echo "  2. Restart ECH0"
echo ""
