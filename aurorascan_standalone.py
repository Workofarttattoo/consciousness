#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.

AuroraScan — Standalone Network Port Scanner
MIT License - Full source code, modify freely

Inspired by nmap, AuroraScan performs non-invasive TCP connect probes with:
- Async concurrent scanning
- Banner grabbing
- Multiple port profiles (recon, core, full)
- JSON output for automation
- OWASP ZAP integration
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import json
import socket
import time
from dataclasses import dataclass, asdict
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


TOOL_NAME = "AuroraScan"
VERSION = "1.0.0-standalone"

DEFAULT_TIMEOUT = 1.5
DEFAULT_CONCURRENCY = 64
DEFAULT_ZAP_SCHEME = "auto"

PORT_PROFILES: Dict[str, Sequence[int]] = {
    "recon": [
        22, 53, 80, 110, 123, 135, 139, 143, 161, 179, 389, 443,
        445, 465, 502, 512, 513, 514, 554, 587, 631, 636, 8080, 8443,
    ],
    "core": [
        21, 22, 23, 25, 53, 80, 111, 135, 139, 143, 161, 389, 443,
        445, 548, 587, 5900, 8080,
    ],
    "full": list(range(1, 1025)),
}

PROFILE_DESCRIPTIONS: Dict[str, str] = {
    "recon": "High-signal ports for rapid situational awareness.",
    "core": "Essential services commonly exposed by workstations and servers.",
    "full": "Complete TCP sweep across ports 1-1024.",
}


def iter_profiles() -> Iterable[Tuple[str, Sequence[int], str]]:
    for key, ports in PORT_PROFILES.items():
        yield key, ports, PROFILE_DESCRIPTIONS.get(key, "")


@dataclass
class PortObservation:
    port: int
    status: str
    response_time_ms: float
    banner: Optional[str] = None


@dataclass
class TargetReport:
    target: str
    resolved: str
    elapsed_ms: float
    observations: List[PortObservation]

    def as_dict(self) -> Dict[str, object]:
        return {
            "target": self.target,
            "resolved": self.resolved,
            "elapsed_ms": self.elapsed_ms,
            "observations": [asdict(obs) for obs in self.observations],
        }


async def probe_port(host: str, port: int, timeout: float) -> Tuple[int, str, float, Optional[str]]:
    """Probe a single port with banner grabbing."""
    start = time.perf_counter()
    try:
        conn = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(conn, timeout=timeout)
        elapsed = (time.perf_counter() - start) * 1000
        banner = None
        try:
            # Try to grab banner
            writer.write(b"\n")
            await asyncio.wait_for(writer.drain(), timeout=timeout)
            peek = await asyncio.wait_for(reader.read(128), timeout=timeout)
            banner = peek.decode(errors="ignore").strip() if peek else None
        except (asyncio.TimeoutError, ConnectionError):
            banner = None
        finally:
            writer.close()
            with contextlib.suppress(Exception):
                await writer.wait_closed()
        return port, "open", elapsed, banner
    except asyncio.TimeoutError:
        elapsed = (time.perf_counter() - start) * 1000
        return port, "filtered", elapsed, None
    except ConnectionRefusedError:
        elapsed = (time.perf_counter() - start) * 1000
        return port, "closed", elapsed, None
    except OSError:
        elapsed = (time.perf_counter() - start) * 1000
        return port, "error", elapsed, None


async def scan_target(
    host: str,
    ports: Sequence[int],
    timeout: float,
    concurrency: int,
) -> TargetReport:
    """Scan all ports on a single target."""
    try:
        resolved = socket.gethostbyname(host)
    except socket.gaierror:
        resolved = "unresolved"

    connect_host = resolved if resolved != "unresolved" else host

    semaphore = asyncio.Semaphore(concurrency)
    observations: List[PortObservation] = []

    async def worker(port: int) -> None:
        async with semaphore:
            result_port, status, elapsed, banner = await probe_port(connect_host, port, timeout)
            observations.append(PortObservation(result_port, status, elapsed, banner))

    start = time.perf_counter()
    tasks = [asyncio.create_task(worker(port)) for port in ports]
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        for task in tasks:
            task.cancel()
        raise
    observations.sort(key=lambda item: item.port)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return TargetReport(host, resolved, elapsed_ms, observations)


def parse_ports(port_arg: Optional[str], profile: str) -> Sequence[int]:
    """Parse port specification from args."""
    if port_arg:
        ports: List[int] = []
        for chunk in port_arg.split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            if "-" in chunk:
                start_str, end_str = chunk.split("-", maxsplit=1)
                start_port = int(start_str)
                end_port = int(end_str)
                ports.extend(range(start_port, end_port + 1))
            else:
                ports.append(int(chunk))
        return sorted(set(p for p in ports if 1 <= p <= 65535))
    return PORT_PROFILES.get(profile, PORT_PROFILES["recon"])


def parse_targets(target_arg: str) -> List[str]:
    """Parse comma-separated targets."""
    targets: List[str] = []
    for chunk in target_arg.split(","):
        target = chunk.strip()
        if target:
            targets.append(target)
    return targets


def load_targets_from_file(path: Optional[str]) -> List[str]:
    """Load targets from file (one per line)."""
    if not path:
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return [line.strip() for line in handle if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print("[warn] Target file not found; ignoring.")
        return []


def display_profiles() -> None:
    """Display available scan profiles."""
    print("[info] Available scan profiles:")
    for name, ports, description in iter_profiles():
        print(f"  - {name:<10} ({len(ports)} ports)  {description}")


def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="AuroraScan - Professional Network Port Scanner",
        epilog="MIT License - Corporation of Light"
    )
    parser.add_argument("targets", nargs="?", help="Comma-separated hostnames or IP addresses.")
    parser.add_argument("--targets-file", help="Path to file containing one target per line.")
    parser.add_argument("--list-profiles", action="store_true", help="Show built-in scanning profiles and exit.")
    parser.add_argument("--ports", help="Comma/range list of ports to scan (e.g., 22,80,4000-4010).")
    parser.add_argument("--profile", default="recon", choices=list(PORT_PROFILES.keys()), help="Port profile preset.")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Per-connection timeout in seconds.")
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY, help="Concurrent connection attempts.")
    parser.add_argument("--json", action="store_true", help="Emit results as JSON instead of human-readable text.")
    parser.add_argument("--output", help="Optional path to write JSON results.")
    parser.add_argument("--tag", default="aurorascan", help="Label included in JSON output.")
    parser.add_argument("--zap-targets", help="Write discovered open services to a file for OWASP ZAP import.")
    parser.add_argument("--zap-scheme", choices=["http", "https", "auto"], default=DEFAULT_ZAP_SCHEME, help="Scheme used when generating ZAP URLs (auto guesses from port).")
    parser.add_argument("--demo", action="store_true", help="Run demo scan against localhost.")
    return parser


def print_human(results: Iterable[TargetReport]) -> None:
    """Print results in human-readable format."""
    for report in results:
        open_observations = [obs for obs in report.observations if obs.status == 'open']
        other_counts: Dict[str, int] = {}
        for obs in report.observations:
            if obs.status != 'open':
                other_counts[obs.status] = other_counts.get(obs.status, 0) + 1
        print(f"[info] Target: {report.target} ({report.resolved}) - {report.elapsed_ms:.2f} ms total")
        if open_observations:
            print('    PORT  STATUS   LAT(ms)  BANNER')
            for obs in open_observations:
                banner = (obs.banner or '')[:48]
                print(f"    {obs.port:>4}/tcp  open    {obs.response_time_ms:>7.2f}  {banner}")
        else:
            print('    No open ports detected under the selected profile.')
        if other_counts:
            summary = ', '.join(f"{status}:{count}" for status, count in sorted(other_counts.items()))
            print(f"    Other responses - {summary}")
        print('')


def write_json(results: Iterable[TargetReport], path: Optional[str], tag: str) -> None:
    """Write results as JSON."""
    payload = {
        "tool": tag or TOOL_NAME.lower(),
        "version": VERSION,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "results": [report.as_dict() for report in results],
    }
    if path:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        print(f"[info] Results written to {path}")
    else:
        print(json.dumps(payload, indent=2))


def write_zap_targets(results: Iterable[TargetReport], path: Optional[str], default_scheme: str) -> None:
    """Write discovered services in OWASP ZAP import format."""
    if not path:
        return
    entries: List[str] = []
    seen = set()
    for report in results:
        host = report.target
        for obs in report.observations:
            if obs.status != "open":
                continue
            scheme = default_scheme
            if scheme == "auto":
                scheme = "https" if obs.port in {443, 8443, 9443, 9444} else "http"
            if (host, obs.port, scheme) in seen:
                continue
            seen.add((host, obs.port, scheme))
            if (scheme == "http" and obs.port == 80) or (scheme == "https" and obs.port == 443):
                url = f"{scheme}://{host}"
            else:
                url = f"{scheme}://{host}:{obs.port}"
            entries.append(url)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(entries) + ("\n" if entries else ""))
    print(f"[info] ZAP target list written to {path} ({len(entries)} endpoint(s)).")


def run_scan(
    targets: Sequence[str],
    ports: Sequence[int],
    *,
    timeout: float,
    concurrency: int,
) -> List[TargetReport]:
    """Execute the scan."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [
        scan_target(target, ports, timeout, concurrency)
        for target in targets
    ]
    try:
        reports = loop.run_until_complete(asyncio.gather(*tasks))
    finally:
        loop.run_until_complete(asyncio.sleep(0))
        loop.close()
    return reports


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_profiles:
        display_profiles()
        return 0

    # Demo mode
    if args.demo:
        print("[info] Running demo scan against localhost common ports...")
        targets = ["localhost"]
        ports = [22, 80, 443, 8080, 8443, 3000, 5000]
    else:
        targets: List[str] = []
        if args.targets:
            targets.extend(parse_targets(args.targets))
        targets.extend(load_targets_from_file(args.targets_file))
        if not targets:
            parser.error("No targets specified. Provide targets argument, --targets-file, or --demo.")

        ports = parse_ports(args.ports, args.profile)
        if not ports:
            parser.error("No ports selected after parsing profile and overrides.")

    print(f"[info] AuroraScan {VERSION}")
    print(f"[info] Starting scan against {len(targets)} target(s) on {len(ports)} port(s).")
    print(f"[info] Timeout: {args.timeout}s, Concurrency: {args.concurrency}")

    start_time = time.time()
    reports = run_scan(
        targets,
        ports,
        timeout=args.timeout,
        concurrency=args.concurrency,
    )
    elapsed = time.time() - start_time

    if args.json or args.output:
        write_json(reports, args.output, args.tag)
    else:
        print_human(reports)

    if args.zap_targets:
        write_zap_targets(reports, args.zap_targets, args.zap_scheme)

    # Summary
    total_open = sum(
        sum(1 for obs in report.observations if obs.status == 'open')
        for report in reports
    )
    print(f"[info] Scan complete in {elapsed:.2f}s - {total_open} open ports found")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
