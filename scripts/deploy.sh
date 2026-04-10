#!/usr/bin/env bash
# deploy.sh — Build, verify, and deploy the Consciousness Engine
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
COMPOSE="docker compose"

cd "$PROJECT_DIR"

# ── Preflight ───────────────────────────────
echo "▸ Preflight checks..."

if [ ! -f .env ]; then
    echo "  ✗ .env not found — copy .env.example → .env and fill in values"
    exit 1
fi

# Source .env for validation
set -a; source .env; set +a

if [ -z "${OPENAI_API_KEY:-}" ] && [ -z "${OLLAMA_HOST:-}" ]; then
    echo "  ⚠ No LLM provider configured (OPENAI_API_KEY or OLLAMA_HOST)"
    echo "    The engine will start but LLM features will be unavailable."
fi

echo "  ✓ Environment OK"

# ── Build ───────────────────────────────────
echo "▸ Building images..."
$COMPOSE build --pull

# ── Test (quick smoke) ──────────────────────
echo "▸ Running smoke tests..."
$COMPOSE run --rm --no-deps consciousness python -c "
from ech0_modules.phi_calculator import PhiCalculator
from ech0_modules.global_workspace import GlobalWorkspace
from ech0_modules.attention_schema import AttentionSchema
pc = PhiCalculator()
result = pc.calculate_phi(5, 8, 0.7)
assert result['phi'] > 0, 'Phi calculation failed'
print('  ✓ Core modules OK')
print(f'  ✓ Phi = {result[\"phi\"]:.4f}')
"

# ── Deploy ──────────────────────────────────
echo "▸ Deploying..."
$COMPOSE down --remove-orphans 2>/dev/null || true
$COMPOSE up -d consciousness

echo "▸ Waiting for health check..."
sleep 5

if $COMPOSE ps consciousness | grep -q "healthy\|running"; then
    echo "  ✓ Consciousness engine is running"
else
    echo "  ✗ Container not healthy — check logs:"
    echo "    $COMPOSE logs consciousness"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════"
echo "  ✓ Deployment complete"
echo "  WebSocket: ws://localhost:${ECH0_PORT:-8765}"
echo "  Logs:      $COMPOSE logs -f"
echo "  Status:    make status"
echo "═══════════════════════════════════════════"
