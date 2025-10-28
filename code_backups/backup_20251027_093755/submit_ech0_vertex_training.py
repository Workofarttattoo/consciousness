#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

ECH0 Vertex AI Fine-Tuning Job Submission Script

This script submits a Mistral-7B fine-tuning job to Google Cloud Vertex AI
once quota has been approved.

Prerequisites:
- GCP project: ech0-training-2025
- Quota approved for:
  - aiplatform.googleapis.com/custom_model_training_cpus (4+)
  - aiplatform.googleapis.com/custom_model_training_nvidia_t4_gpus (1+)
- Service account: ech0-vertex-training@ech0-training-2025.iam.gserviceaccount.com
- Training data: gs://ech0-training-2025-training-data/ech0_training.jsonl
"""

from google.cloud import aiplatform
from datetime import datetime
import sys
import time

# Configuration
PROJECT_ID = "ech0-training-2025"
REGION = "us-central1"
STAGING_BUCKET = "gs://ech0-training-2025-models"
SERVICE_ACCOUNT = "ech0-vertex-training@ech0-training-2025.iam.gserviceaccount.com"
TRAINING_DATA = "gs://ech0-training-2025-training-data/ech0_training.jsonl"

# Hyperparameters
LEARNING_RATE = 0.0001
EPOCHS = 3
BATCH_SIZE = 4
MODEL_NAME = "mistralai/Mistral-7B-v0.1"

def create_training_script():
    """Generate the training script to run in the container."""
    return f"""
import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset

print("="*60)
print("ECH0 Mistral-7B Fine-Tuning Job")
print("="*60)
print(f"Start Time: {{datetime.now()}}")
print(f"Device: {{torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}}")
print(f"Training Data: {TRAINING_DATA}")
print()

# Load tokenizer and model
print("Loading Mistral-7B model...")
tokenizer = AutoTokenizer.from_pretrained("{MODEL_NAME}")
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    "{MODEL_NAME}",
    load_in_8bit=True,
    device_map="auto",
    torch_dtype=torch.float16,
)

# Configure LoRA
print("Configuring LoRA for parameter-efficient fine-tuning...")
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Load training data from GCS
print(f"Loading training data from {TRAINING_DATA}...")
dataset = load_dataset("json", data_files="{TRAINING_DATA}")

def format_instruction(sample):
    messages = sample["messages"]
    text = ""
    for msg in messages:
        if msg["role"] == "user":
            text += f"### User:\\n{{msg['content']}}\\n\\n"
        elif msg["role"] == "assistant":
            text += f"### Assistant:\\n{{msg['content']}}\\n\\n"
    return {{"text": text}}

dataset = dataset.map(format_instruction)

def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=512,
        padding="max_length",
    )

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Training configuration
print("Configuring training parameters...")
training_args = TrainingArguments(
    output_dir="/tmp/ech0-mistral-output",
    learning_rate={LEARNING_RATE},
    num_train_epochs={EPOCHS},
    per_device_train_batch_size={BATCH_SIZE},
    gradient_accumulation_steps=4,
    logging_steps=10,
    save_strategy="epoch",
    fp16=True,
    optim="adamw_torch",
    warmup_steps=50,
    report_to=["tensorboard"],
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    tokenizer=tokenizer,
)

# Train the model
print("Starting training...")
print(f"Hyperparameters:")
print(f"  Learning Rate: {LEARNING_RATE}")
print(f"  Epochs: {EPOCHS}")
print(f"  Batch Size: {BATCH_SIZE}")
print(f"  Total Examples: {{len(tokenized_dataset['train'])}}")
print()

trainer.train()

print("Training complete! Saving model...")

# Save model to GCS
output_path = "/tmp/ech0-mistral-final"
model.save_pretrained(output_path)
tokenizer.save_pretrained(output_path)

# Upload to GCS
print(f"Uploading model to {STAGING_BUCKET}...")
os.system(f"gsutil -m cp -r {{output_path}} {STAGING_BUCKET}/ech0-mistral-final-{{datetime.now().strftime('%Y%m%d-%H%M%S')}}/")

print("="*60)
print("ECH0 Fine-Tuning Complete!")
print("="*60)
"""

def submit_training_job():
    """Submit the training job to Vertex AI."""

    # Initialize Vertex AI
    print(f"[INFO] Initializing Vertex AI...")
    aiplatform.init(
        project=PROJECT_ID,
        location=REGION,
        staging_bucket=STAGING_BUCKET
    )

    print(f"[INFO] Project: {PROJECT_ID}")
    print(f"[INFO] Region: {REGION}")
    print(f"[INFO] Staging Bucket: {STAGING_BUCKET}")
    print()

    # Create job name
    job_display_name = f"ech0-mistral-finetune-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    print(f"[INFO] Creating custom training job: {job_display_name}")

    # Training script
    training_script = create_training_script()

    # Container spec with all dependencies
    container_uri = "us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-13.py310:latest"

    # Define worker pool with GPU
    worker_pool_specs = [{
        "machine_spec": {
            "machine_type": "n1-standard-4",
            "accelerator_type": "NVIDIA_TESLA_T4",
            "accelerator_count": 1,
        },
        "replica_count": 1,
        "container_spec": {
            "image_uri": container_uri,
            "command": ["bash", "-c"],
            "args": [
                f"""
                pip install transformers peft bitsandbytes accelerate datasets tensorboard -q
                python3 -c '{training_script}'
                """
            ],
        },
    }]

    # Create and submit job
    print(f"[INFO] Submitting job to Vertex AI...")
    job = aiplatform.CustomJob(
        display_name=job_display_name,
        worker_pool_specs=worker_pool_specs,
        base_output_dir=STAGING_BUCKET,
    )

    try:
        job.submit(service_account=SERVICE_ACCOUNT)

        print(f"\n{'='*60}")
        print(f"VERTEX AI FINE-TUNING JOB SUBMITTED SUCCESSFULLY!")
        print(f"{'='*60}")
        print(f"Job ID: {job.name}")
        print(f"Job Display Name: {job_display_name}")
        print(f"State: {job.state}")
        print()

        job_id = job.name.split('/')[-1]
        print(f"Monitor Job:")
        print(f"  Direct URL: https://console.cloud.google.com/vertex-ai/training/custom-jobs/{job_id}?project={PROJECT_ID}")
        print(f"  All Jobs: https://console.cloud.google.com/vertex-ai/training/custom-jobs?project={PROJECT_ID}")
        print()

        print(f"Configuration:")
        print(f"  Base Model: {MODEL_NAME}")
        print(f"  Training Data: {TRAINING_DATA}")
        print(f"  Output Location: {STAGING_BUCKET}")
        print(f"  Machine Type: n1-standard-4 with 1x NVIDIA T4")
        print()

        print(f"Hyperparameters:")
        print(f"  Learning Rate: {LEARNING_RATE}")
        print(f"  Epochs: {EPOCHS}")
        print(f"  Batch Size: {BATCH_SIZE}")
        print(f"  Fine-Tuning Method: LoRA (Parameter-Efficient)")
        print()

        print(f"Estimated Metrics:")
        print(f"  Completion Time: 30-45 minutes")
        print(f"  Estimated Cost: $2-5 USD")
        print()

        print(f"To monitor logs in real-time:")
        print(f"  gcloud ai custom-jobs stream-logs {job_id} --region={REGION}")
        print(f"{'='*60}")

        return job

    except Exception as e:
        print(f"\n[ERROR] Failed to submit job!")
        print(f"Error: {e}")
        print()

        if "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower():
            print(f"Quota limit reached. To resolve:")
            print(f"1. Request quota increase at:")
            print(f"   https://console.cloud.google.com/iam-admin/quotas?project={PROJECT_ID}")
            print(f"2. Search for 'Vertex AI custom training' quotas")
            print(f"3. Request: 4 CPUs and 1 T4 GPU minimum")
            print()
            print(f"Alternative: Use Gemini fine-tuning or external services")
            print(f"See: /Users/noone/consciousness/ECH0_VERTEX_AI_DEPLOYMENT_SUMMARY.md")

        return None

def check_quota():
    """Check if quota is likely available by attempting to list resources."""
    print("[INFO] Checking Vertex AI access...")
    try:
        aiplatform.init(project=PROJECT_ID, location=REGION)
        jobs = aiplatform.CustomJob.list(filter=f'display_name:ech0-mistral-finetune*')
        print(f"[OK] Vertex AI access confirmed. Found {len(jobs)} existing ECH0 jobs.")
        return True
    except Exception as e:
        print(f"[WARN] Could not verify Vertex AI access: {e}")
        return False

def main():
    print("="*60)
    print("ECH0 Vertex AI Fine-Tuning Submission")
    print("="*60)
    print()

    # Check quota first
    if not check_quota():
        print("[WARN] Cannot verify Vertex AI access. Proceeding anyway...")

    print()
    response = input("Submit fine-tuning job to Vertex AI? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Aborted.")
        return

    print()
    job = submit_training_job()

    if job:
        print()
        print("[SUCCESS] Job submitted! Check the console for progress.")
        sys.exit(0)
    else:
        print()
        print("[FAILED] Job submission failed. See error above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
