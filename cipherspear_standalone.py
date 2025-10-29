#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.

CipherSpear — SQL Injection Pattern Analysis Tool
MIT License - Full source code, modify freely

Safe, read-only validation of database exposure through pattern matching.
No live exploitation - pure static analysis for defensive security.

Features:
- Pattern-based detection of SQL injection vectors
- URL, query string, and form data parsing
- Risk scoring (low/medium/high)
- Multiple technique detection (blind, boolean, time-based, union, etc.)
- JSON output for automation
"""

from __future__ import annotations

import argparse
import json
import re
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import parse_qsl, urlparse


TOOL_NAME = "CipherSpear"
VERSION = "1.0.0-standalone"

# Pattern definitions for common SQL injection techniques
SUSPICIOUS_PATTERNS: Sequence[Tuple[re.Pattern[str], str, int]] = [
    (re.compile(r"(?:'|\")\s*(?:or|and)\s+1\s*=\s*1", re.IGNORECASE), "boolean-tautology", 4),
    (re.compile(r"union\s+select", re.IGNORECASE), "union-select", 3),
    (re.compile(r"sleep\(\s*\d+\s*\)", re.IGNORECASE), "time-based-delay", 2),
    (re.compile(r"benchmark\(", re.IGNORECASE), "timing-benchmark", 2),
    (re.compile(r"(?:--|#)\s*$"), "inline-comment", 1),
    (re.compile(r"/\*.*\*/", re.IGNORECASE | re.DOTALL), "multiline-comment", 1),
    (re.compile(r"load_file\s*\(", re.IGNORECASE), "file-read", 3),
    (re.compile(r"into\s+outfile", re.IGNORECASE), "file-write", 3),
    (re.compile(r"xp_cmdshell", re.IGNORECASE), "command-exec", 4),
    (re.compile(r"regexp\s+'[^']*'", re.IGNORECASE), "pattern-match", 1),
]

SAMPLE_VECTORS: Sequence[str] = (
    "GET /search?term=pulse' OR 1=1-- HTTP/1.1",
    "POST /api/user HTTP/1.1\n{id: 4, \"username\": \"admin\" }",
    "username=guest&password=guest",
    "GET /inventory?category=electronics&sort=price%20desc HTTP/1.1",
    "https://example.internal/login?user=admin&pass='; sleep(5); --",
    "SELECT * FROM users WHERE id=1 UNION SELECT NULL,NULL,NULL",
    "admin'--",
    "1' OR '1'='1",
    "'; DROP TABLE users; --",
    "admin' OR 1=1/*",
)


@dataclass
class VectorAssessment:
    """Analysis result for a single injection vector."""
    vector: str
    risk_score: int
    risk_label: str
    findings: List[str]
    parameters: List[Tuple[str, str]]
    recommendation: str

    def as_dict(self) -> Dict[str, object]:
        payload = asdict(self)
        payload["parameter_count"] = len(self.parameters)
        return payload


def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="CipherSpear - SQL Injection Pattern Analysis Tool",
        epilog="MIT License - Corporation of Light"
    )
    parser.add_argument("--dsn", help="Target database DSN (e.g. postgresql://user@host/db) - for documentation only, not used in analysis.")
    parser.add_argument("--tech", default="", help="Comma separated techniques to emphasize (e.g. blind,bool,time).")
    parser.add_argument("--queries", help="Path to file containing candidate injection vectors (one per line).")
    parser.add_argument("--vector", action="append", help="Inline injection vector to analyze (repeatable).")
    parser.add_argument("--demo", action="store_true", help="Analyse built-in sample vectors.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    parser.add_argument("--output", help="Write the detailed JSON payload to the specified path.")
    return parser


def load_vectors(path: Optional[str], inline: Optional[Sequence[str]], demo: bool) -> List[str]:
    """Load vectors from file, inline args, or demo samples."""
    vectors: List[str] = []
    if path:
        try:
            entries = Path(path).read_text(encoding="utf-8").splitlines()
            for entry in entries:
                entry = entry.strip()
                if entry and not entry.startswith("#"):
                    vectors.append(entry)
        except FileNotFoundError:
            print(f"[warn] File not found: {path}")
    if inline:
        vectors.extend(item for item in inline if item)
    if demo or not vectors:
        vectors.extend(SAMPLE_VECTORS)
    return vectors


def extract_parameters(vector: str) -> List[Tuple[str, str]]:
    """
    Extract parameter key/value pairs from URLs, query strings, or form bodies.
    """
    pairs: List[Tuple[str, str]] = []
    if "://" in vector:
        parsed = urlparse(vector)
    else:
        parsed = urlparse(f"http://dummy/{vector.lstrip('/')}")
    pairs.extend(parse_qsl(parsed.query, keep_blank_values=True))
    fragments = parsed.fragment.split("&") if parsed.fragment else []
    for fragment in fragments:
        if "=" in fragment:
            key, value = fragment.split("=", maxsplit=1)
            pairs.append((key, value))
    if "=" in vector and not pairs:
        for chunk in vector.split("&"):
            if "=" not in chunk:
                continue
            key, value = chunk.split("=", maxsplit=1)
            pairs.append((key, value))
    return pairs


def assess_vector(vector: str, techniques: Sequence[str]) -> VectorAssessment:
    """
    Analyze a single vector for SQL injection patterns.

    Returns risk assessment with:
    - Risk score (0-15+)
    - Risk label (low/medium/high)
    - List of findings (pattern names)
    - Extracted parameters
    - Recommendation for mitigation
    """
    findings: List[str] = []
    score = 0

    # Check against all known SQL injection patterns
    for pattern, label, severity in SUSPICIOUS_PATTERNS:
        if pattern.search(vector):
            findings.append(label)
            score += severity

    # Analyze parameters for common injection indicators
    params = extract_parameters(vector)
    for _, value in params:
        if "'" in value or "\"" in value:
            findings.append("quote-injection")
            score += 1
        if re.search(r"(select|update|delete)\s+\w+", value, re.IGNORECASE):
            findings.append("embedded-sql")
            score += 2

    # Boost score for technique-specific patterns
    if any(t in {"blind", "time"} for t in techniques) and "time-based-delay" in findings:
        score += 2

    # Determine risk level
    risk_label = "low"
    if score >= 8:
        risk_label = "high"
    elif score >= 4:
        risk_label = "medium"

    # Generate specific recommendation
    recommendation = "Review parameterised queries and input validation."
    if "file-write" in findings or "command-exec" in findings:
        recommendation = "⚠️  CRITICAL: Immediate mitigation required; high-impact primitives detected."
    elif "union-select" in findings:
        recommendation = "Verify column alignment and sanitise UNION clauses."
    elif "time-based-delay" in findings:
        recommendation = "Implement input validation to prevent time-based blind injection."
    elif "boolean-tautology" in findings:
        recommendation = "Use parameterized queries to prevent boolean-based injection."

    return VectorAssessment(
        vector=vector,
        risk_score=score,
        risk_label=risk_label,
        findings=sorted(set(findings)),
        parameters=params,
        recommendation=recommendation,
    )


def sanitise_dsn(dsn: str) -> Dict[str, object]:
    """Parse and sanitize DSN, redacting passwords."""
    parsed = urlparse(dsn)
    redacted_netloc = parsed.netloc
    if "@" in redacted_netloc:
        userinfo, hostinfo = redacted_netloc.split("@", maxsplit=1)
        if ":" in userinfo:
            user, _ = userinfo.split(":", maxsplit=1)
        else:
            user = userinfo
        redacted_netloc = f"{user}@{hostinfo}"
    return {
        "scheme": parsed.scheme or "unknown",
        "netloc": redacted_netloc,
        "path": parsed.path or "/",
        "params": parsed.params,
    }


def print_human_output(assessments: List[VectorAssessment], techniques: Sequence[str], dsn: Optional[str]) -> None:
    """Print human-readable analysis results."""
    print(f"\n{'='*80}")
    print(f"CipherSpear {VERSION} - SQL Injection Pattern Analysis")
    print(f"{'='*80}\n")

    if dsn:
        dsn_info = sanitise_dsn(dsn)
        print(f"Target: {dsn_info['scheme']}://{dsn_info['netloc']}{dsn_info['path']}")

    if techniques:
        print(f"Techniques: {', '.join(techniques)}")

    print(f"Vectors analyzed: {len(assessments)}\n")

    # Summary statistics
    totals = {
        "low": sum(1 for item in assessments if item.risk_label == "low"),
        "medium": sum(1 for item in assessments if item.risk_label == "medium"),
        "high": sum(1 for item in assessments if item.risk_label == "high"),
    }

    print(f"Risk Summary:")
    print(f"  🟢 Low:    {totals['low']}")
    print(f"  🟡 Medium: {totals['medium']}")
    print(f"  🔴 High:   {totals['high']}")
    print()

    # Detailed findings
    for i, assessment in enumerate(assessments, 1):
        risk_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}[assessment.risk_label]
        print(f"{i}. {risk_icon} [{assessment.risk_label.upper()}] Score: {assessment.risk_score}")
        print(f"   Vector: {assessment.vector[:80]}{'...' if len(assessment.vector) > 80 else ''}")

        if assessment.findings:
            print(f"   Findings: {', '.join(assessment.findings)}")

        if assessment.parameters:
            print(f"   Parameters: {len(assessment.parameters)} detected")
            for key, value in assessment.parameters[:3]:  # Show first 3
                print(f"     - {key}={value[:40]}{'...' if len(value) > 40 else ''}")

        print(f"   💡 {assessment.recommendation}")
        print()


def render_output(args: argparse.Namespace, assessments: List[VectorAssessment], techniques: Sequence[str]) -> int:
    """Render output in requested format."""
    totals = {
        "low": sum(1 for item in assessments if item.risk_label == "low"),
        "medium": sum(1 for item in assessments if item.risk_label == "medium"),
        "high": sum(1 for item in assessments if item.risk_label == "high"),
    }

    payload = {
        "tool": TOOL_NAME,
        "version": VERSION,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dsn": sanitise_dsn(args.dsn) if args.dsn else {"scheme": "demo", "netloc": "localhost"},
        "techniques": list(techniques),
        "vectors_processed": len(assessments),
        "findings": totals,
        "assessments": [assessment.as_dict() for assessment in assessments],
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print_human_output(assessments, techniques, args.dsn)

    if args.output:
        Path(args.output).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"[info] Detailed JSON report written to: {args.output}")

    return 0


def run(args: argparse.Namespace) -> int:
    """Main execution logic."""
    techniques = [chunk.strip().lower() for chunk in args.tech.split(",") if chunk.strip()]
    vectors = load_vectors(args.queries, args.vector, args.demo)

    if not vectors:
        print("[error] No vectors to analyze. Use --demo, --vector, or --queries.")
        return 1

    print(f"[info] CipherSpear {VERSION}")
    print(f"[info] Analyzing {len(vectors)} vector(s)...")

    start_time = time.time()
    assessments = [assess_vector(vector, techniques) for vector in vectors]
    elapsed = time.time() - start_time

    print(f"[info] Analysis complete in {elapsed:.2f}s\n")

    return render_output(args, assessments, techniques)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
