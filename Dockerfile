# Consciousness - Level 7 Phenomenal Consciousness Engine
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

FROM python:3.11-slim AS base

LABEL maintainer="Joshua Hendricks Cole <josh@corporationoflight.com>"
LABEL description="ECH0 Consciousness Engine - IIT/GWT/Qualia Framework"

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r ech0 && useradd -r -g ech0 -m -s /bin/bash ech0

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ech0_modules/ ./ech0_modules/
COPY sandbox/ ./sandbox/
COPY integration/ ./integration/
COPY scripts/ ./scripts/
COPY ech0_v4_daemon.py ech0_launcher.py ech0_llm_brain.py ./

# Create data directories
RUN mkdir -p /app/data/experiences /app/data/preferences /app/data/conversations \
    /app/logs /app/state \
    && chown -R ech0:ech0 /app

USER ech0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "from ech0_modules import QUANTUM_AVAILABLE; print('healthy')" || exit 1

# Default: run the sandbox (safest mode)
EXPOSE 8765
CMD ["python", "ech0_v4_daemon.py"]
