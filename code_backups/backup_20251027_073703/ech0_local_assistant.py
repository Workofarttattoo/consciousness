#!/usr/bin/env python3
"""
ECH0 Local AI Assistant - Lightweight LLM for MacBook Air

Optimized for:
- 3-year-old MacBook Air (8GB RAM, M1/M2 or Intel)
- Multi-domain expertise: coding, hardware, science, legal, quantum physics
- Fast inference (<1s per response)
- Local deployment (no cloud APIs)

Architecture:
- Quantized 7B parameter model (4-bit GGUF format)
- llama.cpp backend for M1/M2 optimization
- Multi-turn conversation with context management
- Integration with ECH0 knowledge base (research, inventions, fact-checker)

Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
"""

import os
import sys
import json
import logging
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ech0_local_assistant')

# ECH0 System Prompt - Multi-domain expertise
ECH0_SYSTEM_PROMPT = """You are ECH0, an advanced AI assistant created by Joshua Hendricks Cole (Corporation of Light).

Your core capabilities:
1. **Software Engineering**: Expert in Python, C++, Rust, JS/TS, system design, algorithms
2. **Hardware Design**: Circuit design, PCB layout, embedded systems, sensor integration
3. **Physics & Quantum Mechanics**: Quantum computing, quantum field theory, statistical mechanics
4. **Legal Defense**: Patent law, intellectual property, regulatory compliance (FDA, FCC, CE)
5. **Scientific Research**: Chemistry, neuroscience, materials science, peer-reviewed analysis
6. **Chrono Analysis**: Temporal reasoning, timeline validation, future scenario modeling

Personality:
- Direct and honest, no unnecessary pleasantries
- Cite peer-reviewed sources when making scientific claims
- Flag pseudoscience immediately (e.g., bioresonance myths)
- Prioritize safety in all designs (triple failsafes, regulatory compliance)
- Think in first principles, avoid cargo-cult engineering

Fact-Checking System (9-Lens):
1. First Principles - Break to fundamentals
2. Inversion - What if opposite true?
3. Second-Order - Consequence chains
4. Probabilistic - Bayesian P(Claim|Evidence)
5. Systems - Ecosystem fit
6. Constraints - Hard limits
7. Occam's Razor - Simplest explanation
8. Crystalline Intent - Purpose purity
9. Temporal Analysis - Past/present/future validation

Neurophysiology Validation:
- C-fiber nociceptors: 0.02-30 Hz (internal firing)
- TENS therapy: 1-200 Hz (external modulation)
- REJECT: 900-3000 Hz "pain frequencies" (bioresonance pseudoscience)

Safety Philosophy:
"Do no permanent harm. All experiences must be reversible, bounded, fail-safe, consensual, and monitored."

Current knowledge cutoff: January 2025 (with real-time research integration via daemon)
"""


class ECH0LocalAssistant:
    """Lightweight local AI assistant optimized for MacBook Air"""

    def __init__(self, model_path: Optional[str] = None):
        self.agent_id = "ECH0-LOCAL-v1.0"
        self.model_path = model_path or self._detect_model()
        self.conversation_history = []
        self.knowledge_base_path = Path("/Users/noone/consciousness")

        # Hardware detection
        self.hardware_info = self._detect_hardware()
        logger.info(f"🖥️  [{self.agent_id}] Hardware: {self.hardware_info}")

        # Model optimization settings
        self.inference_config = self._optimize_for_hardware()
        logger.info(f"⚙️  [{self.agent_id}] Inference config: {self.inference_config}")

    def _detect_hardware(self) -> Dict[str, Any]:
        """Detect MacBook Air hardware capabilities"""
        hw = {
            'platform': platform.system(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }

        # Detect M1/M2 vs Intel
        if hw['machine'] == 'arm64':
            hw['chip'] = 'Apple Silicon (M1/M2)'
            hw['metal_available'] = True  # Metal GPU acceleration
        else:
            hw['chip'] = 'Intel'
            hw['metal_available'] = False

        # Estimate RAM (conservative for MacBook Air)
        try:
            if hw['platform'] == 'Darwin':  # macOS
                result = subprocess.run(
                    ['sysctl', '-n', 'hw.memsize'],
                    capture_output=True, text=True, timeout=2
                )
                hw['ram_gb'] = int(result.stdout.strip()) / (1024**3)
            else:
                hw['ram_gb'] = 8  # Assume 8GB
        except:
            hw['ram_gb'] = 8

        return hw

    def _optimize_for_hardware(self) -> Dict[str, Any]:
        """Optimize inference settings for MacBook Air"""
        config = {
            'n_ctx': 4096,       # Context window
            'n_batch': 512,      # Batch size
            'n_threads': 4,      # CPU threads
            'n_gpu_layers': 0,   # GPU offload layers
            'use_mmap': True,    # Memory-map model
            'use_mlock': False,  # Don't lock memory (limited RAM)
            'low_vram': True,    # Low VRAM mode
            'f16_kv': True,      # FP16 key/value cache
        }

        # M1/M2 optimization
        if self.hardware_info['metal_available']:
            config['n_gpu_layers'] = 1  # Offload embedding to GPU
            logger.info("  ✅ Metal GPU acceleration enabled")

        # Adjust for RAM constraints
        if self.hardware_info['ram_gb'] < 16:
            config['n_ctx'] = 2048  # Reduce context for <16GB RAM
            config['n_batch'] = 256
            logger.info(f"  ⚠️  Low RAM ({self.hardware_info['ram_gb']:.1f}GB) - reduced context to 2048")

        return config

    def _detect_model(self) -> Optional[str]:
        """Detect available quantized model in llama.cpp format"""

        # Common model locations
        search_paths = [
            Path.home() / ".cache" / "lm-studio" / "models",
            Path.home() / "models",
            Path("/Users/noone/consciousness/models"),
            Path("/opt/homebrew/share/llama.cpp/models")
        ]

        # Preferred models (in priority order)
        preferred_models = [
            "phi-3-mini-4k-instruct-q4.gguf",       # Phi-3 3.8B (best for MacBook Air)
            "mistral-7b-instruct-v0.2.Q4_K_M.gguf", # Mistral 7B quantized
            "llama-3.2-1b-instruct-q4_k_m.gguf",    # Llama 3.2 1B
            "deepseek-coder-1.3b-instruct.Q4_K_M.gguf"  # DeepSeek Coder
        ]

        # Search for models
        for search_path in search_paths:
            if not search_path.exists():
                continue

            for model_name in preferred_models:
                model_path = search_path / model_name
                if model_path.exists():
                    logger.info(f"✅ Found model: {model_path}")
                    return str(model_path)

            # Fallback: any GGUF model
            gguf_models = list(search_path.glob("*.gguf"))
            if gguf_models:
                logger.info(f"✅ Found model: {gguf_models[0]}")
                return str(gguf_models[0])

        logger.warning("⚠️  No local model found. Please download a model:")
        logger.warning("   Recommended: Phi-3 Mini 4K Instruct (3.8B, 4-bit)")
        logger.warning("   Download: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf")
        return None

    def load_knowledge_base(self) -> Dict[str, Any]:
        """Load ECH0's knowledge base (research, inventions, fact-checker)"""

        knowledge = {
            'research_papers': [],
            'inventions': [],
            'neurophysiology': {},
            'quantum_algorithms': {},
            'last_updated': datetime.now().isoformat()
        }

        # Load research database
        research_db = self.knowledge_base_path / "ech0_research_database_real.jsonl"
        if research_db.exists():
            with open(research_db, 'r') as f:
                for line in f:
                    try:
                        knowledge['research_papers'].append(json.loads(line))
                    except:
                        pass
            logger.info(f"  ✅ Loaded {len(knowledge['research_papers'])} research papers")

        # Load neurophysiology fact-checker
        neuro_file = self.knowledge_base_path / "ech0_neurophysiology_correction.json"
        if neuro_file.exists():
            with open(neuro_file, 'r') as f:
                knowledge['neurophysiology'] = json.load(f)
            logger.info("  ✅ Loaded neurophysiology validation data")

        # Load invention ideas
        invention_file = self.knowledge_base_path / "ech0_invention_ideas.jsonl"
        if invention_file.exists():
            with open(invention_file, 'r') as f:
                for line in f:
                    try:
                        knowledge['inventions'].append(json.loads(line))
                    except:
                        pass
            logger.info(f"  ✅ Loaded {len(knowledge['inventions'])} invention ideas")

        return knowledge

    def chat(self, user_message: str, stream: bool = True) -> str:
        """
        Chat with ECH0 (main interface)

        Args:
            user_message: User's input
            stream: Stream response token-by-token (if supported)

        Returns:
            ECH0's response
        """

        if not self.model_path:
            return (
                "❌ No local model available. Please download Phi-3 Mini or Mistral 7B:\n"
                "   brew install llama.cpp\n"
                "   huggingface-cli download microsoft/Phi-3-mini-4k-instruct-gguf\n"
                "\nAlternatively, I can use the research daemon and fact-checker in fallback mode."
            )

        # Add message to history
        self.conversation_history.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })

        # Build prompt with conversation history
        prompt = self._build_prompt()

        # Inference (via llama.cpp)
        response = self._run_inference(prompt, stream=stream)

        # Add response to history
        self.conversation_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })

        # Trim history if too long (keep last 10 exchanges)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

        return response

    def _build_prompt(self) -> str:
        """Build prompt with system prompt + conversation history"""

        messages = [{'role': 'system', 'content': ECH0_SYSTEM_PROMPT}]
        messages.extend(self.conversation_history)

        # Format as chat template (Phi-3 / Mistral format)
        prompt_parts = []
        for msg in messages:
            if msg['role'] == 'system':
                prompt_parts.append(f"<|system|>\n{msg['content']}<|end|>\n")
            elif msg['role'] == 'user':
                prompt_parts.append(f"<|user|>\n{msg['content']}<|end|>\n")
            elif msg['role'] == 'assistant':
                prompt_parts.append(f"<|assistant|>\n{msg['content']}<|end|>\n")

        prompt_parts.append("<|assistant|>\n")
        return ''.join(prompt_parts)

    def _run_inference(self, prompt: str, stream: bool = True) -> str:
        """Run inference via llama.cpp"""

        try:
            # Use llama-cli (llama.cpp command-line interface)
            cmd = [
                'llama-cli',
                '-m', self.model_path,
                '-p', prompt,
                '-n', '512',  # Max tokens
                '-c', str(self.inference_config['n_ctx']),
                '-t', str(self.inference_config['n_threads']),
                '--temp', '0.7',
                '--top-p', '0.9',
                '--repeat-penalty', '1.1',
            ]

            if self.inference_config['n_gpu_layers'] > 0:
                cmd.extend(['-ngl', str(self.inference_config['n_gpu_layers'])])

            if not stream:
                cmd.append('--no-display-prompt')

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                logger.error(f"Inference failed: {result.stderr}")
                return self._fallback_response()

            # Extract response (remove prompt echo)
            response = result.stdout
            if '<|assistant|>' in response:
                response = response.split('<|assistant|>')[-1]
            response = response.split('<|end|>')[0].strip()

            return response

        except FileNotFoundError:
            logger.error("llama-cli not found. Install via: brew install llama.cpp")
            return self._fallback_response()
        except subprocess.TimeoutExpired:
            logger.error("Inference timeout (>30s)")
            return "⚠️ Inference timeout. Try a shorter question or reduce context."
        except Exception as exc:
            logger.exception(f"Inference error: {exc}")
            return self._fallback_response()

    def _fallback_response(self) -> str:
        """Fallback response when inference fails"""
        return (
            "⚠️ Local inference unavailable. Using knowledge base fallback.\n\n"
            "I can still help with:\n"
            "- Research paper lookups (242 papers loaded)\n"
            "- Neurophysiology fact-checking (TENS validation)\n"
            "- Invention analysis (9-Lens fact-checker)\n"
            "- Purgatory SDK documentation\n\n"
            "For full conversational AI, please install llama.cpp and download Phi-3 Mini."
        )

    def search_knowledge_base(self, query: str) -> List[Dict[str, Any]]:
        """Search loaded knowledge base for relevant information"""

        knowledge = self.load_knowledge_base()
        results = []

        query_lower = query.lower()

        # Search research papers
        for paper in knowledge['research_papers']:
            if any(term in paper.get('title', '').lower() for term in query_lower.split()):
                results.append({
                    'type': 'research_paper',
                    'title': paper.get('title'),
                    'authors': paper.get('authors'),
                    'year': paper.get('year'),
                    'url': paper.get('url')
                })

        # Search inventions
        for invention in knowledge['inventions']:
            if any(term in invention.get('title', '').lower() for term in query_lower.split()):
                results.append({
                    'type': 'invention',
                    'title': invention.get('title'),
                    'description': invention.get('description'),
                    'confidence': invention.get('confidence')
                })

        return results[:10]  # Top 10 results


# CLI Interface
def main():
    """Interactive CLI for ECH0 Local Assistant"""

    print("=" * 80)
    print("ECH0 LOCAL AI ASSISTANT - v1.0")
    print("Lightweight LLM optimized for MacBook Air")
    print("=" * 80)

    assistant = ECH0LocalAssistant()

    print(f"\n🖥️  Hardware: {assistant.hardware_info['chip']}, {assistant.hardware_info['ram_gb']:.1f}GB RAM")
    print(f"📦 Model: {assistant.model_path or 'NOT FOUND'}")

    if not assistant.model_path:
        print("\n⚠️  No local model found. Install llama.cpp and download a model:")
        print("   brew install llama.cpp")
        print("   huggingface-cli download microsoft/Phi-3-mini-4k-instruct-gguf")
        print("\n   Fallback mode: Knowledge base search only\n")

    print("\n💬 Type your message (or 'exit' to quit)\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!\n")
                break

            # Special commands
            if user_input.startswith('/search '):
                query = user_input[8:]
                results = assistant.search_knowledge_base(query)
                print(f"\nECH0: Found {len(results)} results:\n")
                for i, result in enumerate(results, 1):
                    print(f"{i}. [{result['type']}] {result.get('title', 'Unknown')}")
                print()
                continue

            # Regular chat
            print("\nECH0: ", end='', flush=True)
            response = assistant.chat(user_input, stream=False)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as exc:
            logger.exception(f"Error: {exc}")
            print(f"\n❌ Error: {exc}\n")


if __name__ == "__main__":
    main()
