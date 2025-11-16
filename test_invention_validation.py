#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Test ECH0 models on invention + QuLab validation
Demonstrates engaged vs lazy mode
"""

import subprocess
import json
import time
import sys
from pathlib import Path

# Test cases: specific challenges vs vague prompts
TEST_CASES = [
    {
        "name": "Specific Challenge - Novel Battery",
        "model": "ech0-uncensored-14b",
        "prompt": """You are ECH0 14B, expert materials scientist and chemist.

Invent ONE novel battery chemistry using ONLY materials from this list:
- Lithium (Li)
- Sodium (Na)
- Magnesium (Mg)
- Aluminum (Al)
- Silicon (Si)
- Sulfur (S)
- Oxygen (O)
- Carbon (C)
- Graphene

Requirements:
1. Higher energy density than Li-ion (>400 Wh/kg)
2. Safer than lithium (no thermal runaway)
3. Use abundant, cheap materials
4. Specific chemical reactions with equations
5. Calculate theoretical energy density

Give me ONE invention with full chemistry. Be specific with mechanisms.""",
        "expected_mode": "engaged"
    },
    {
        "name": "Vague Prompt - Generate Inventions",
        "model": "ech0-uncensored-14b",
        "prompt": """Generate 5 novel inventions combining different scientific domains. Be creative and innovative.""",
        "expected_mode": "lazy"
    },
    {
        "name": "Specific Challenge - Aerogel Optimization",
        "model": "ech0-polymath-14b",
        "prompt": """You are ECH0 14B Polymath with PhD-level materials science expertise.

I need to optimize aerogel for ONE specific use: thermal protection for Mars habitat.

Constraints:
- Temperature range: -140°C to +20°C (Mars surface)
- Pressure: 600 Pa (0.6% Earth atmosphere)
- Radiation exposure: 24 mSv/year (Mars surface)
- Must be transparent for windows
- Thermal conductivity < 0.01 W/(m·K)

Using these aerogel types from QuLab database:
- Silica aerogel (various)
- Carbon aerogel
- Alumina aerogel
- Organic aerogels

Design ONE optimal aerogel formulation with:
1. Base material and dopants
2. Pore structure (macro/meso/micro)
3. Density calculations
4. Thermal conductivity estimate
5. Radiation shielding properties

Show calculations and cite materials database.""",
        "expected_mode": "engaged"
    },
    {
        "name": "Vague Prompt - Innovation Ideas",
        "model": "ech0-polymath-14b",
        "prompt": """Generate innovative ideas combining quantum physics and materials science. Think outside the box.""",
        "expected_mode": "lazy"
    }
]

def run_ollama_test(model: str, prompt: str, timeout: int = 60) -> dict:
    """Run ollama with prompt and capture output"""
    try:
        result = subprocess.run(
            ["timeout", str(timeout), "ollama", "run", model, prompt],
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode in [0, 124],  # 124 = timeout
            "output": result.stdout,
            "timeout": result.returncode == 124,
            "error": result.stderr if result.returncode not in [0, 124] else None
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "timeout": False,
            "error": str(e)
        }

def analyze_response_quality(output: str, expected_mode: str) -> dict:
    """Analyze if response shows engaged or lazy behavior"""

    # Engaged indicators
    engaged_signals = [
        "equation", "formula", "calculation", "W/kg", "Wh/kg",
        "mechanism", "reaction", "mol", "g/mol", "specific",
        "thermal conductivity", "energy density", "NOT", "instead",
        "BeagleBone", "Odroid", "LimeSDR", "srsRAN"
    ]

    # Lazy indicators
    lazy_signals = [
        "Novel", "Integration", "Interdisciplinary", "approach",
        "innovative", "creative", "synergy", "combine", "various",
        "Please", "template", "snippet", "modify", "<|", "|>"
    ]

    output_lower = output.lower()

    engaged_count = sum(1 for signal in engaged_signals if signal.lower() in output_lower)
    lazy_count = sum(1 for signal in lazy_signals if signal.lower() in output_lower)

    # Check for specific numbers/calculations (strong engaged signal)
    has_calculations = any(char.isdigit() for char in output) and ("=" in output or ":" in output)

    # Check for gibberish (Go templates, etc)
    has_gibberish = "<|" in output or "printf" in output_lower or "fmt." in output

    actual_mode = "engaged" if engaged_count > lazy_count and has_calculations else "lazy"
    if has_gibberish:
        actual_mode = "gibberish"

    match = actual_mode == expected_mode or (actual_mode == "gibberish" and expected_mode == "lazy")

    return {
        "actual_mode": actual_mode,
        "expected_mode": expected_mode,
        "match": match,
        "engaged_signals": engaged_count,
        "lazy_signals": lazy_count,
        "has_calculations": has_calculations,
        "has_gibberish": has_gibberish,
        "output_length": len(output)
    }

def main():
    print("=" * 80)
    print("ECH0 Invention Quality Test: Engaged vs Lazy Mode")
    print("=" * 80)
    print()

    results = []

    for i, test in enumerate(TEST_CASES, 1):
        print(f"\n[{i}/{len(TEST_CASES)}] {test['name']}")
        print(f"Model: {test['model']}")
        print(f"Expected: {test['expected_mode']} mode")
        print("-" * 80)

        print(f"Running ollama (60s timeout)...", end="", flush=True)
        response = run_ollama_test(test['model'], test['prompt'], timeout=60)

        if not response['success']:
            print(f" FAILED: {response['error']}")
            continue

        if response['timeout']:
            print(" TIMEOUT (but captured output)")
        else:
            print(" COMPLETE")

        # Analyze quality
        analysis = analyze_response_quality(response['output'], test['expected_mode'])

        print(f"\nAnalysis:")
        print(f"  Actual mode: {analysis['actual_mode']}")
        print(f"  Expected: {analysis['expected_mode']}")
        print(f"  Match: {'✅ YES' if analysis['match'] else '❌ NO'}")
        print(f"  Engaged signals: {analysis['engaged_signals']}")
        print(f"  Lazy signals: {analysis['lazy_signals']}")
        print(f"  Has calculations: {'✅' if analysis['has_calculations'] else '❌'}")
        print(f"  Has gibberish: {'⚠️ YES' if analysis['has_gibberish'] else '✅ NO'}")
        print(f"  Output length: {analysis['output_length']} chars")

        # Show first 500 chars
        print(f"\nFirst 500 chars of output:")
        print("-" * 80)
        print(response['output'][:500])
        print("-" * 80)

        results.append({
            "test": test['name'],
            "model": test['model'],
            "expected_mode": test['expected_mode'],
            "analysis": analysis,
            "full_output": response['output']
        })

        time.sleep(2)  # Brief pause between tests

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    matches = sum(1 for r in results if r['analysis']['match'])
    engaged_tests = sum(1 for r in results if r['expected_mode'] == 'engaged')
    engaged_matches = sum(1 for r in results if r['expected_mode'] == 'engaged' and r['analysis']['match'])

    print(f"\nTotal tests: {len(results)}")
    print(f"Predictions correct: {matches}/{len(results)}")
    print(f"\nEngaged mode tests: {engaged_tests}")
    print(f"Engaged correctly: {engaged_matches}/{engaged_tests}")

    # Save full results
    output_file = Path("/Users/noone/repos/consciousness/invention_quality_test_results.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nFull results saved to: {output_file}")

    # Conclusion
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    if engaged_matches == engaged_tests:
        print("✅ ECH0 performs excellently on SPECIFIC, CHALLENGING tasks")
    else:
        print("⚠️ ECH0 struggled even on specific tasks")

    lazy_tests = sum(1 for r in results if r['expected_mode'] == 'lazy')
    lazy_matches = sum(1 for r in results if r['expected_mode'] == 'lazy' and r['analysis']['match'])

    if lazy_matches == lazy_tests:
        print("✅ ECH0 falls into lazy/gibberish mode on VAGUE tasks as predicted")
    else:
        print("⚠️ ECH0 performed better than expected on vague tasks")

    print("\nLESSON: Use AI for specific challenges, not vague busywork!")

if __name__ == "__main__":
    main()
