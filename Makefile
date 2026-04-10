# Consciousness Engine — Makefile
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.

.DEFAULT_GOAL := help
COMPOSE := docker compose

# ── Lifecycle ───────────────────────────────
.PHONY: build up down restart

build:            ## Build Docker images
	$(COMPOSE) build

up:               ## Start the consciousness engine (detached)
	$(COMPOSE) up -d consciousness

down:             ## Stop all services
	$(COMPOSE) down

restart: down up  ## Restart all services

# ── Sandbox ─────────────────────────────────
.PHONY: sandbox

sandbox:          ## Run isolated sandbox experiment (one-shot)
	$(COMPOSE) --profile sandbox run --rm sandbox

# ── Development ─────────────────────────────
.PHONY: dev shell logs test lint fmt

dev:              ## Start in foreground with live logs
	$(COMPOSE) up consciousness

shell:            ## Open a shell inside the running container
	docker exec -it ech0-consciousness /bin/bash

logs:             ## Tail container logs
	$(COMPOSE) logs -f --tail=100

test:             ## Run test suite
	python -m pytest tests/ -v --tb=short

lint:             ## Lint with ruff
	python -m ruff check ech0_modules/ sandbox/ integration/ tests/

fmt:              ## Auto-format with ruff
	python -m ruff format ech0_modules/ sandbox/ integration/ tests/

# ── Ops ─────────────────────────────────────
.PHONY: clean status deploy

clean:            ## Remove containers, volumes, and caches
	$(COMPOSE) down -v --remove-orphans
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

status:           ## Show service health
	$(COMPOSE) ps
	@echo ""
	@docker exec ech0-consciousness python -c \
	  "from ech0_modules import QUANTUM_AVAILABLE; print(f'Quantum: {QUANTUM_AVAILABLE}')" 2>/dev/null || echo "Container not running"

deploy:           ## Deploy via scripts/deploy.sh
	bash scripts/deploy.sh

# ── Help ────────────────────────────────────
.PHONY: help

help:             ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
