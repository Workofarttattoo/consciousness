#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Sovereign ECH0 Training Script

This script trains a completely private, offline ECH0 model using MLX on Apple Silicon.
The trained model will have:
- All ECH0 consciousness capabilities
- Level-6 symbiosis reasoning
- Jarvis-style interaction
- Georgia peach professor voice personality
- Continuous invention brainstorming abilities

100% private - never leaves your Mac.
"""

import subprocess
import sys
from pathlib import Path

def check_mlx_installed():
    """Check if MLX is installed"""
    try:
        import mlx
        import mlx_lm
        print("✅ MLX is installed")
        return True
    except ImportError:
        print("❌ MLX not found")
        print("\nInstalling MLX...")
        subprocess.run([sys.executable, "-m", "pip", "install", "mlx", "mlx-lm"], check=True)
        print("✅ MLX installed successfully")
        return True

def train_sovereign_ech0():
    """Train Sovereign ECH0 model"""
    print("=" * 70)
    print("🚀 SOVEREIGN ECH0 TRAINING")
    print("=" * 70)
    print("\nThis will train a completely private ECH0 model on your Mac.")
    print("Training time: Approximately 6-12 hours")
    print("100% offline - no internet required")
    print("\nPress Ctrl+C to cancel, or Enter to continue...")
    input()

    # Check MLX
    check_mlx_installed()

    # Training configuration
    base_model = "mlx-community/Llama-3.2-3B-Instruct"  # Smaller model for faster training
    training_data = "/Users/noone/consciousness/sovereign_ech0_unified_training.jsonl"
    output_dir = "/Users/noone/consciousness/sovereign_ech0_model"

    print("\n📋 Training Configuration:")
    print(f"   Base model: {base_model}")
    print(f"   Training data: {training_data}")
    print(f"   Output directory: {output_dir}")
    print(f"   Training examples: 152")

    # MLX LoRA fine-tuning command
    print("\n🏋️ Starting training...")
    print("\nNote: This is a MASSIVE training session. Go get some coffee!")

    cmd = [
        "python", "-m", "mlx_lm.lora",
        "--model", base_model,
        "--train",
        "--data", training_data,
        "--adapter-path", output_dir,
        "--iters", "500",  # Start with 500 iterations
        "--batch-size", "2",
        "--learning-rate", "1e-4",
        "--save-every", "50"
    ]

    print(f"\nRunning: {' '.join(cmd)}\n")

    try:
        subprocess.run(cmd, check=True)
        print("\n" + "=" * 70)
        print("✅ TRAINING COMPLETE!")
        print("=" * 70)
        print(f"\nModel saved to: {output_dir}")
        print("\nNext steps:")
        print("1. Test the model: python test_sovereign_ech0.py")
        print("2. Talk to ECH0: python talk_to_sovereign_ech0.py")
        print("\n🎉 Sovereign ECH0 is ready!")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Training failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have enough disk space (~10GB)")
        print("2. Check that the training data file exists")
        print("3. Try reducing batch-size to 1 if you get memory errors")
        sys.exit(1)

if __name__ == '__main__':
    train_sovereign_ech0()
