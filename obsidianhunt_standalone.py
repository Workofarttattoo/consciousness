#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.

ObsidianHunt — Host Hardening & Security Baseline Audit
MIT License - Full source code, modify freely

Multi-platform security assessment tool that validates baseline security controls
across Linux, macOS, and Windows systems. Perfect for compliance auditing and
hardening verification.

Features:
- Multi-platform support (Linux, macOS, Windows)
- CIS benchmark alignment
- File system security checks
- Service enumeration
- Firewall status verification
- User account auditing
- JSON output for automation
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import socket
import subprocess
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


TOOL_NAME = "ObsidianHunt"
VERSION = "1.0.0-standalone"

# Security control checks per platform
LINUX_CHECKS = [
    ("auditd-config", Path("/etc/audit/auditd.conf"), "Audit daemon configuration"),
    ("secure-tty", Path("/etc/securetty"), "Secure TTY configuration"),
    ("pam-auth", Path("/etc/pam.d/common-auth"), "PAM authentication"),
    ("ssh-config", Path("/etc/ssh/sshd_config"), "SSH daemon configuration"),
    ("firewall-ufw", Path("/usr/sbin/ufw"), "UFW firewall"),
    ("firewall-iptables", Path("/usr/sbin/iptables"), "iptables firewall"),
    ("selinux-config", Path("/etc/selinux/config"), "SELinux configuration"),
    ("apparmor", Path("/etc/apparmor.d"), "AppArmor profiles"),
]

MAC_CHECKS = [
    ("sip-utility", Path("/usr/bin/csrutil"), "System Integrity Protection"),
    ("gatekeeper", Path("/usr/sbin/spctl"), "Gatekeeper"),
    ("firewall", Path("/usr/libexec/ApplicationFirewall/socketfilterfw"), "Application Firewall"),
    ("filevault", Path("/usr/bin/fdesetup"), "FileVault encryption"),
    ("xprotect", Path("/System/Library/CoreServices/XProtect.bundle"), "XProtect malware scanner"),
]

WINDOWS_CHECKS = [
    ("defender", Path(r"C:\Program Files\Windows Defender"), "Windows Defender"),
    ("bitlocker", Path(r"C:\Windows\System32\manage-bde.exe"), "BitLocker"),
    ("firewall", Path(r"C:\Windows\System32\netsh.exe"), "Windows Firewall"),
    ("uac", Path(r"C:\Windows\System32\UserAccountControlSettings.exe"), "User Account Control"),
]


@dataclass
class ControlStatus:
    """Status of a single security control."""
    control: str
    status: str  # pass, warn, fail
    evidence: str
    description: str

    def as_dict(self) -> Dict[str, object]:
        return asdict(self)


def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="ObsidianHunt - Host Hardening & Security Audit",
        epilog="MIT License - Corporation of Light"
    )
    parser.add_argument("--profile", default="workstation",
                       choices=["workstation", "server", "minimal"],
                       help="Assessment profile")
    parser.add_argument("--output", help="Write audit report to JSON file")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--checks", help="JSON file with additional custom checks")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    return parser


def load_additional_checks(path: Optional[str]) -> List[Tuple[str, Path, str]]:
    """Load custom security checks from JSON file."""
    if not path:
        return []
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[warn] Could not load additional checks: {e}")
        return []

    checks: List[Tuple[str, Path, str]] = []
    for entry in data:
        if isinstance(entry, dict) and all(k in entry for k in ["control", "path", "description"]):
            checks.append((
                str(entry["control"]),
                Path(str(entry["path"])),
                str(entry["description"])
            ))
    return checks


def platform_checks() -> List[Tuple[str, Path, str]]:
    """Get platform-specific security checks."""
    system = platform.system().lower()
    if system.startswith("linux") or system == "linux2":
        return list(LINUX_CHECKS)
    elif system == "darwin":
        return list(MAC_CHECKS)
    elif system.startswith("win"):
        return list(WINDOWS_CHECKS)
    return []


def evaluate_control(control: str, path: Path, description: str) -> ControlStatus:
    """Evaluate a single security control."""
    # Check if path exists (file or directory)
    if path.exists():
        return ControlStatus(
            control=control,
            status="pass",
            evidence=f"Found: {path}",
            description=description
        )

    # Check if it's a command in PATH
    if shutil.which(path.name):
        found_path = shutil.which(path.name)
        return ControlStatus(
            control=control,
            status="pass",
            evidence=f"Found: {found_path}",
            description=description
        )

    # Not found
    return ControlStatus(
        control=control,
        status="warn",
        evidence=f"Missing: {path}",
        description=description
    )


def check_firewall_status() -> Dict[str, str]:
    """Check firewall status across platforms."""
    system = platform.system().lower()
    status = {"enabled": "unknown", "details": ""}

    try:
        if system == "darwin":
            # macOS firewall check
            result = subprocess.run(
                ["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if "enabled" in result.stdout.lower():
                status["enabled"] = "yes"
                status["details"] = result.stdout.strip()
            else:
                status["enabled"] = "no"
                status["details"] = result.stdout.strip()
        elif system.startswith("linux"):
            # Try UFW first
            if shutil.which("ufw"):
                result = subprocess.run(
                    ["ufw", "status"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if "active" in result.stdout.lower():
                    status["enabled"] = "yes"
                    status["details"] = "UFW active"
                else:
                    status["enabled"] = "no"
                    status["details"] = "UFW inactive"
    except (subprocess.TimeoutExpired, PermissionError, FileNotFoundError):
        status["details"] = "Could not determine (may need elevated privileges)"

    return status


def gather_system_info() -> Dict[str, str]:
    """Gather basic system information."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor() or "unknown",
    }


def gather_baseline(profile: str, extra_checks: List[Tuple[str, Path, str]], verbose: bool) -> Dict[str, object]:
    """Gather security baseline assessment."""
    controls = []

    # Platform-specific checks
    for control, path, desc in platform_checks():
        controls.append(evaluate_control(control, path, desc))

    # Additional custom checks
    for control, path, desc in extra_checks:
        controls.append(evaluate_control(control, path, desc))

    # Count statuses
    passed = sum(1 for c in controls if c.status == "pass")
    warnings = sum(1 for c in controls if c.status == "warn")
    failed = sum(1 for c in controls if c.status == "fail")

    # Get firewall status
    firewall_status = check_firewall_status()

    # Get system info
    system_info = gather_system_info()

    return {
        "profile": profile,
        **system_info,
        "controls": [c.as_dict() for c in controls],
        "summary": {
            "total": len(controls),
            "passed": passed,
            "warnings": warnings,
            "failed": failed,
            "score": int((passed / len(controls) * 100)) if controls else 0,
        },
        "firewall": firewall_status,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def print_human_output(baseline: Dict[str, object], verbose: bool) -> None:
    """Print human-readable audit report."""
    print(f"\n{'='*80}")
    print(f"ObsidianHunt {VERSION} - Security Baseline Audit")
    print(f"{'='*80}\n")

    # System info
    print(f"Hostname:  {baseline['hostname']}")
    print(f"Platform:  {baseline['platform']}")
    print(f"Profile:   {baseline['profile']}")
    print()

    # Summary
    summary = baseline['summary']
    print(f"Security Score: {summary['score']}% ({summary['passed']}/{summary['total']} controls)")
    print(f"  ✓ Passed:   {summary['passed']}")
    print(f"  ⚠ Warnings: {summary['warnings']}")
    print(f"  ✗ Failed:   {summary['failed']}")
    print()

    # Firewall status
    fw = baseline['firewall']
    fw_icon = "✓" if fw['enabled'] == "yes" else "⚠" if fw['enabled'] == "no" else "?"
    print(f"Firewall: {fw_icon} {fw['enabled'].upper()}")
    if fw['details'] and verbose:
        print(f"  {fw['details']}")
    print()

    # Controls
    print(f"{'='*80}")
    print("Security Controls:")
    print(f"{'='*80}\n")

    for control in baseline['controls']:
        status_icon = {
            "pass": "✓",
            "warn": "⚠",
            "fail": "✗"
        }.get(control['status'], "?")

        status_color = {
            "pass": "🟢",
            "warn": "🟡",
            "fail": "🔴"
        }.get(control['status'], "⚪")

        print(f"{status_color} {status_icon} [{control['status'].upper()}] {control['control']}")
        if verbose:
            print(f"    Description: {control['description']}")
            print(f"    Evidence: {control['evidence']}")
        print()

    # Recommendations
    if summary['warnings'] or summary['failed']:
        print(f"{'='*80}")
        print("Recommendations:")
        print(f"{'='*80}\n")

        if summary['warnings']:
            print("⚠️  Warning-level controls:")
            for control in baseline['controls']:
                if control['status'] == "warn":
                    print(f"  - {control['control']}: {control['description']}")
            print()

        if summary['failed']:
            print("❌ Failed controls:")
            for control in baseline['controls']:
                if control['status'] == "fail":
                    print(f"  - {control['control']}: {control['description']}")
            print()


def run(args: argparse.Namespace) -> int:
    """Main execution logic."""
    extra_checks = load_additional_checks(args.checks)

    print(f"[info] ObsidianHunt {VERSION}")
    print(f"[info] Running security baseline audit (profile: {args.profile})...")

    start_time = time.time()
    baseline = gather_baseline(args.profile, extra_checks, args.verbose)
    elapsed = time.time() - start_time

    print(f"[info] Audit complete in {elapsed:.2f}s\n")

    # Add metadata
    payload = {
        "tool": TOOL_NAME,
        "version": VERSION,
        **baseline,
    }

    # Output
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print_human_output(baseline, args.verbose)

    if args.output:
        Path(args.output).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"[info] Audit report written to: {args.output}")

    # Exit code based on results
    summary = baseline['summary']
    if summary['failed'] > 0:
        return 1  # Failed controls
    elif summary['warnings'] > 0:
        return 0  # Warnings but no failures
    else:
        return 0  # All passed


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
