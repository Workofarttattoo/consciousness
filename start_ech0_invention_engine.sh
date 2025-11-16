#!/bin/bash
# Wrapper to keep the ECH0 continuous invention engine running under launchd.
# Copyright (c) 2025 Joshua Hendricks Cole.

set -euo pipefail

ROOT_DIR="/Users/noone"
CONSCIOUSNESS_DIR="${ROOT_DIR}/consciousness"
REPO_DIR="${ROOT_DIR}/repos/consciousness"
LOG_DIR="${CONSCIOUSNESS_DIR}/logs"
LOG_FILE="${LOG_DIR}/ech0_invention_engine.log"
LOCK_DIR="${CONSCIOUSNESS_DIR}/.ech0_invention_lock"

mkdir -p "${LOG_DIR}"

if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
  echo "$(date '+%Y-%m-%dT%H:%M:%S%z') [warn] invention engine already running; skipping duplicate launch" >> "${LOG_FILE}"
  exit 0
fi

cleanup() {
  rmdir "${LOCK_DIR}" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

export PYTHONUNBUFFERED=1

echo "$(date '+%Y-%m-%dT%H:%M:%S%z') [info] starting ech0 continuous invention engine" >> "${LOG_FILE}"
/usr/bin/python3 -u "${REPO_DIR}/ech0_continuous_invention_engine.py" >> "${LOG_FILE}" 2>&1
