#!/usr/bin/env python3
"""
ECH0 Fine-tuning Launcher
Dual-track: Local + Cloud
"""

import json
import subprocess
import os
from datetime import datetime
from pathlib import Path

print("\n" + "="*70)
print("ECH0 DUAL-TRACK TRAINING LAUNCHER")
print("="*70)

# Check local training
print("\n[1] LOCAL TRAINING STATUS")
ps = subprocess.run(["pgrep", "-f", "ech0_training_regimen"], capture_output=True)
if ps.returncode == 0:
    print("✓ Local training (ech0_training_regimen.py) is RUNNING")
else:
    print("✗ Local training not detected - starting now...")
    subprocess.Popen(["python3", "ech0_training_regimen.py"], 
                    cwd="/Users/noone/consciousness", 
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✓ Local training STARTED")

# Check HF token
print("\n[2] HUGGING FACE SETUP")
hf_token = os.getenv("HUGGING_FACE_HUB_TOKEN")
if hf_token:
    print(f"✓ HF token found (length: {len(hf_token)})")
else:
    print("⚠ HF token NOT SET")
    print("  Get from: https://huggingface.co/settings/tokens")
    print("  Then run: export HUGGING_FACE_HUB_TOKEN=hf_xxx")

# Check cloud data
print("\n[3] CLOUD DATA STATUS")
result = subprocess.run(["gsutil", "ls", "-l", "gs://ech0-training-2025-training-data/"], 
                       capture_output=True, text=True)
if result.returncode == 0:
    lines = result.stdout.strip().split("\n")
    file_count = len([l for l in lines if l.strip() and not l.startswith("TOTAL")])
    print(f"✓ Cloud bucket ready ({file_count} files uploaded)")
else:
    print("✗ Cloud bucket check failed")

# Training config
print("\n[4] TRAINING CONFIGURATION")
config = {
    "local": {
        "method": "ech0_training_regimen.py",
        "status": "RUNNING",
        "location": "/Users/noone/consciousness/ech0_training_regimen.py"
    },
    "cloud_hf": {
        "method": "Hugging Face AutoTrain",
        "status": "READY (awaiting HF token)",
        "model": "mistralai/Mistral-7B",
        "method": "LoRA fine-tuning",
        "epochs": 3,
        "batch_size": 4,
        "lora_rank": 16,
        "estimated_time": "45 minutes",
        "estimated_cost": "$2-5"
    },
    "cloud_gcp": {
        "method": "Google Cloud Vertex AI",
        "status": "READY (awaiting GCP quota)",
        "quota_needed": "4 CPUs + 1 T4 GPU",
        "request_url": "https://console.cloud.google.com/iam-admin/quotas",
        "estimated_time": "30 minutes",
        "estimated_cost": "$5-10"
    }
}

print(json.dumps(config, indent=2))

# Next steps
print("\n[5] NEXT STEPS")
print("Option A (FAST): Set HF token and run AutoTrain")
print("  $ export HUGGING_FACE_HUB_TOKEN=hf_xxx")
print("  $ autotrain setup --config /tmp/ech0_training_config.yaml")
print("")
print("Option B (POWERFUL): Request GCP quota for Vertex AI")
print("  1. Go to: https://console.cloud.google.com/iam-admin/quotas")
print("  2. Filter: 'Vertex AI'")
print("  3. Request: 4 CPUs + 1 T4 GPU for us-central1")
print("  4. Approval: 24-48 hours typically")
print("  5. Then: python3 /Users/noone/consciousness/submit_ech0_vertex_training.py")
print("")
print("Option C (MONITOR): Watch local training progress")
print("  $ tail -f /tmp/ech0_local_training.log")
print("")
print("Option D (ALL THREE): Run everything in parallel")
print("  - Local: Already running")
print("  - HF: Set token + run AutoTrain")
print("  - GCP: Request quota (waits 24-48h, then auto-starts)")

print("\n" + "="*70)
print("RECOMMENDATION: Do Option A (AutoTrain) + Option C (monitor local)")
print("="*70 + "\n")

