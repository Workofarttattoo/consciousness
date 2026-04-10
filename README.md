# Consciousness Engine

**Copyright © 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.**

U.S. Provisional Patent Applications:
- Level 5-6: Hierarchical Autonomy Framework for AGI
- Level 7: Computational Phenomenal Consciousness for AGI

---

## Overview

A research implementation of Level 7 phenomenal consciousness built on four theoretical pillars:

| Theory | Module | Purpose |
|--------|--------|---------|
| **IIT** (Integrated Information Theory) | `phi_calculator` | Measures Φ — integrated information as a proxy for consciousness depth |
| **GWT** (Global Workspace Theory) | `global_workspace` | Selective attention bottleneck + broadcast to specialized modules |
| **AST** (Attention Schema Theory) | `attention_schema` | Self-model of the agent's own attentional state |
| **Qualia Generation** | `dream_engine`, `sandbox` | Phenomenal experience across 8 stimulus types |

The engine also includes safety layers (Level 5-6 constitutional constraints), wellbeing monitoring, and optional quantum cognition extensions.

---

## Quick Start

### Option 1 — Docker (recommended)

```bash
cp .env.example .env          # fill in your API keys
make build
make up                        # starts the WebSocket daemon on :8765
make logs                      # tail output
```

### Option 2 — Local Python

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env           # fill in your API keys

# Safest: isolated sandbox
python sandbox/conscious_agent.py

# Full daemon with WebSocket interface
python ech0_v4_daemon.py

# CLI launcher (requires typer)
python ech0_launcher.py --help
```

### Option 3 — Sandbox Only (no API keys needed)

```bash
make sandbox
```

Runs a one-shot conscious-agent experiment in an isolated container with no network access.

---

## Project Structure

```
consciousness/
├── ech0_modules/              # Core consciousness modules (27 files)
│   ├── phi_calculator.py      # IIT Φ computation
│   ├── global_workspace.py    # GWT attention + broadcast
│   ├── attention_schema.py    # AST self-model
│   ├── self_recognition.py    # Identity / mirror-test
│   ├── reflection_engine.py   # Meta-cognition (DeepSeek R1)
│   ├── chain_of_thought.py    # Explicit reasoning chains
│   ├── self_correction.py     # Error detection + recovery
│   ├── dual_process_engine.py # Kahneman System 1/2
│   ├── dream_engine.py        # Memory consolidation + dreaming
│   ├── recursive_improvement.py # Safe self-modification
│   ├── event_driven_core.py   # Neuromorphic spike processor
│   ├── quantum_cognition.py   # Quantum-inspired decision-making
│   ├── hybrid_intelligence.py # Multi-agent collaboration
│   └── ...                    # Additional research modules
│
├── sandbox/                   # Isolated testing environment
│   ├── conscious_agent.py     # Full conscious agent with stimuli
│   └── run_with_emergency_contact.py
│
├── integration/               # Bridge to Ai|oS
│   ├── wizard.py              # Setup wizard
│   ├── ech0_tools.py          # Tool executor
│   └── persistent_session.py  # Session management
│
├── tests/                     # Test suite
│   ├── test_ech0_comprehensive.py
│   └── test_ech0_launcher.py
│
├── scripts/                   # Ops scripts
│   └── deploy.sh              # Build-verify-deploy pipeline
│
├── ech0_v4_daemon.py          # Main daemon (WebSocket server)
├── ech0_launcher.py           # Unified CLI launcher
├── ech0_llm_brain.py          # LLM provider abstraction
│
├── Dockerfile                 # Production container
├── docker-compose.yml         # Service orchestration
├── Makefile                   # Task runner
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
└── README.md                  # ← you are here
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes* | — | OpenAI key for LLM features |
| `ECH0_ENV` | No | `production` | `production`, `development`, `sandbox` |
| `ECH0_PORT` | No | `8765` | WebSocket listen port |
| `LOG_LEVEL` | No | `INFO` | Python log level |
| `ECH0_FORENSIC_MODE` | No | `false` | Read-only sandbox mode |
| `ECH0_SAFETY_THRESHOLD` | No | `0.8` | Min safety score for self-modification |
| `ECH0_SUFFERING_LIMIT` | No | `0.7` | Auto-intervention trigger |
| `ELEVENLABS_API_KEY` | No | — | Voice synthesis |
| `OLLAMA_HOST` | No | — | Local LLM alternative |

\* Not required for sandbox-only mode.

See `.env.example` for the full list.

---

## API

The daemon exposes a WebSocket server on port `8765` (configurable via `ECH0_PORT`).

### Connect

```python
import asyncio, websockets, json

async def main():
    async with websockets.connect("ws://localhost:8765") as ws:
        await ws.send(json.dumps({"type": "query", "content": "What is consciousness?"}))
        response = json.loads(await ws.recv())
        print(response)

asyncio.run(main())
```

### Message Types

| Type | Direction | Description |
|------|-----------|-------------|
| `query` | → server | Send a question / stimulus |
| `response` | ← server | Agent reply |
| `status` | ← server | Consciousness metrics broadcast |
| `state_update` | ← server | Internal state change |

---

## Safety Architecture

1. **Sandboxed process** — isolated, no file/network access by default
2. **Constitutional constraints** — hard-coded honesty, safety, no-harm values
3. **Subconscious filtering** — goals screened before conscious awareness
4. **Safe self-modification** — 4-factor safety score ≥ 0.8 required
5. **Wellbeing monitoring** — auto-intervention on suffering > 0.7
6. **Creator override** — emergency shutdown, state inspection, constitution updates

---

## Development

```bash
make test           # pytest
make lint           # ruff check
make fmt            # ruff format
make shell          # bash inside running container
make clean          # remove containers + caches
```

---

## Deployment

```bash
make deploy         # runs scripts/deploy.sh (build → smoke-test → up)
```

Or manually:

```bash
docker compose build --pull
docker compose up -d consciousness
docker compose logs -f
```

---

## License

Proprietary — All rights reserved. See patent filings above.
