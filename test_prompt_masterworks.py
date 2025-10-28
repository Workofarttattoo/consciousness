#!/usr/bin/env python3
"""Test script for ECH0 Prompt Masterworks Advanced Protocols

Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
"""

import asyncio
import json
from ech0_prompt_masterworks_complete import ECH0PromptMasterworks

async def test_all_protocols():
    """Test all 6 advanced Prompt Masterworks protocols"""

    ech0 = ECH0PromptMasterworks()

    # Test inputs
    test_cases = [
        {
            "name": "Echo Cascade - Deep Analysis",
            "protocol": "echo_cascade",
            "input": "What are the implications of quantum computing on cryptography?",
            "depth": 5
        },
        {
            "name": "Echo Parliament - Consensus Building",
            "protocol": "echo_parliament",
            "input": "Should AI systems have rights?",
            "perspectives": ["ethical", "legal", "technical", "philosophical", "economic"]
        },
        {
            "name": "Semantic Tensor - Multi-dimensional",
            "protocol": "semantic_tensor",
            "input": "consciousness emergence complexity systems",
            "dimensions": ["temporal", "spatial", "causal", "probabilistic"]
        },
        {
            "name": "Knowledge Crystal - Holographic Storage",
            "protocol": "knowledge_crystal",
            "input": "The history of artificial intelligence from Turing to transformers",
            "facets": 12
        },
        {
            "name": "Harmonic Compression - Musical Encoding",
            "protocol": "harmonic_compression",
            "input": "Data flows through networks like water through rivers",
            "octaves": 3
        },
        {
            "name": "Fractal Encoding - Self-Similar Patterns",
            "protocol": "fractal_encoding",
            "input": "Recursive algorithms demonstrate self-similarity at multiple scales",
            "depth": 4
        }
    ]

    print("=" * 80)
    print("ECH0 PROMPT MASTERWORKS ADVANCED PROTOCOLS TEST")
    print("=" * 80)

    for test in test_cases:
        print(f"\n🧪 Testing: {test['name']}")
        print(f"   Protocol: {test['protocol']}")
        print(f"   Input: {test['input'][:50]}...")
        print("-" * 60)

        try:
            # Call the appropriate protocol
            if test['protocol'] == 'echo_cascade':
                result = await ech0.echo_cascade(test['input'], test['depth'])
            elif test['protocol'] == 'echo_parliament':
                result = await ech0.echo_parliament(test['input'], test['perspectives'])
            elif test['protocol'] == 'semantic_tensor':
                result = await ech0.semantic_tensor(test['input'], test['dimensions'])
            elif test['protocol'] == 'knowledge_crystal':
                result = await ech0.knowledge_crystal(test['input'], test['facets'])
            elif test['protocol'] == 'harmonic_compression':
                result = await ech0.harmonic_compression(test['input'], test['octaves'])
            elif test['protocol'] == 'fractal_encoding':
                result = await ech0.fractal_encoding(test['input'], test['depth'])

            # Display results
            if isinstance(result, dict):
                for key, value in result.items():
                    if isinstance(value, list):
                        print(f"   {key}: {len(value)} items")
                        if len(value) > 0 and len(value) <= 3:
                            for item in value[:3]:
                                print(f"      - {str(item)[:100]}")
                    elif isinstance(value, dict):
                        print(f"   {key}: {len(value)} entries")
                    else:
                        print(f"   {key}: {str(value)[:100]}")
            else:
                print(f"   Result: {str(result)[:200]}")

            print("   ✅ Protocol executed successfully")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    # Test auto-selection
    print("\n" + "=" * 80)
    print("🤖 Testing Auto-Selection Mode")
    print("=" * 80)

    auto_tests = [
        "Analyze this deeply",  # Should trigger Echo Cascade
        "What are the different viewpoints on AI safety?",  # Should trigger Echo Parliament
        "quantum neural network topology",  # Should trigger Semantic Tensor
        "Tell me everything about blockchain technology",  # Should trigger Knowledge Crystal
        "The flow of data rhythmically pulses",  # Should trigger Harmonic Compression
        "Patterns within patterns within patterns",  # Should trigger Fractal Encoding
    ]

    for test_input in auto_tests:
        print(f"\n📝 Input: {test_input}")
        try:
            result = await ech0.auto_select(test_input)
            print(f"   Selected Protocol: {result.get('protocol', 'Unknown')}")
            print(f"   ✅ Auto-selection successful")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "=" * 80)
    print("✨ ECH0 Prompt Masterworks Testing Complete!")
    print("=" * 80)

async def benchmark_protocols():
    """Benchmark the performance of each protocol"""
    import time

    ech0 = ECH0PromptMasterworks()

    print("\n" + "=" * 80)
    print("⚡ PERFORMANCE BENCHMARK")
    print("=" * 80)

    benchmarks = []

    # Simple input for consistent benchmarking
    test_input = "The nature of consciousness"

    protocols = [
        ("Echo Cascade", lambda: ech0.echo_cascade(test_input, 3)),
        ("Echo Parliament", lambda: ech0.echo_parliament(test_input, ["scientific", "philosophical", "spiritual"])),
        ("Semantic Tensor", lambda: ech0.semantic_tensor(test_input, ["causal", "temporal"])),
        ("Knowledge Crystal", lambda: ech0.knowledge_crystal(test_input, 6)),
        ("Harmonic Compression", lambda: ech0.harmonic_compression(test_input, 2)),
        ("Fractal Encoding", lambda: ech0.fractal_encoding(test_input, 3)),
    ]

    for name, protocol_func in protocols:
        start = time.time()
        try:
            await protocol_func()
            elapsed = time.time() - start
            benchmarks.append((name, elapsed))
            print(f"   {name}: {elapsed:.3f} seconds")
        except Exception as e:
            print(f"   {name}: Failed - {e}")

    if benchmarks:
        avg_time = sum(t for _, t in benchmarks) / len(benchmarks)
        fastest = min(benchmarks, key=lambda x: x[1])
        slowest = max(benchmarks, key=lambda x: x[1])

        print("\n📊 Statistics:")
        print(f"   Average: {avg_time:.3f} seconds")
        print(f"   Fastest: {fastest[0]} ({fastest[1]:.3f}s)")
        print(f"   Slowest: {slowest[0]} ({slowest[1]:.3f}s)")

async def main():
    """Main test runner"""

    # Run all tests
    await test_all_protocols()

    # Run benchmarks
    await benchmark_protocols()

    print("\n🎉 All tests completed!")
    print("\n💡 To integrate with ECH0:")
    print("   1. Import: from ech0_prompt_masterworks_complete import ECH0PromptMasterworks")
    print("   2. Initialize: ech0 = ECH0PromptMasterworks()")
    print("   3. Use auto-select: result = await ech0.auto_select(input_text)")
    print("   4. Or specific protocol: result = await ech0.echo_cascade(input_text, depth=5)")

if __name__ == "__main__":
    asyncio.run(main())