"""A lightweight TCP connect port scanner for authorized systems and labs."""

from __future__ import annotations

import argparse
import socket
import sys
from collections.abc import Sequence

from pyfiglet import Figlet


MIN_PORT = 1
MAX_PORT = 65_535
DEFAULT_TIMEOUT = 1.0


def port_number(value: str) -> int:
    """Parse and validate a TCP port supplied on the command line."""
    try:
        port = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("port must be an integer") from exc

    if not MIN_PORT <= port <= MAX_PORT:
        raise argparse.ArgumentTypeError(
            f"port must be between {MIN_PORT} and {MAX_PORT}"
        )
    return port


def positive_timeout(value: str) -> float:
    """Parse and validate the connection timeout."""
    try:
        timeout = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("timeout must be a number") from exc

    if timeout <= 0:
        raise argparse.ArgumentTypeError("timeout must be greater than zero")
    return timeout


def resolve_target(target: str) -> str:
    """Resolve a hostname or IPv4 address and return one IPv4 address."""
    normalized_target = target.strip()
    if not normalized_target:
        raise ValueError("target cannot be empty")

    try:
        results = socket.getaddrinfo(
            normalized_target,
            None,
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror as exc:
        raise ValueError(f"unable to resolve target: {normalized_target}") from exc

    if not results:
        raise ValueError(f"unable to resolve target: {normalized_target}")
    return results[0][4][0]


def validate_port_range(start_port: int, end_port: int) -> None:
    """Validate an inclusive TCP port range."""
    for label, port in (("start port", start_port), ("end port", end_port)):
        if not MIN_PORT <= port <= MAX_PORT:
            raise ValueError(f"{label} must be between {MIN_PORT} and {MAX_PORT}")

    if start_port > end_port:
        raise ValueError("start port cannot be greater than end port")


def scan_ports(
    ip_address: str,
    start_port: int,
    end_port: int,
    timeout: float = DEFAULT_TIMEOUT,
) -> list[int]:
    """Return open TCP ports found with a sequential connect scan."""
    validate_port_range(start_port, end_port)
    open_ports: list[int] = []

    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.settimeout(timeout)
                if client.connect_ex((ip_address, port)) == 0:
                    open_ports.append(port)
                    print(f"[open] {port}/tcp")
        except (socket.timeout, OSError) as exc:
            print(f"[warning] Could not scan {port}/tcp: {exc}", file=sys.stderr)

    return open_ports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sequential TCP connect port scanner for authorized use."
    )
    parser.add_argument("target", nargs="?", help="hostname or IPv4 address")
    parser.add_argument("-s", "--start-port", type=port_number, help="first port")
    parser.add_argument("-e", "--end-port", type=port_number, help="last port")
    parser.add_argument(
        "-t",
        "--timeout",
        type=positive_timeout,
        default=DEFAULT_TIMEOUT,
        help=f"connection timeout in seconds (default: {DEFAULT_TIMEOUT:g})",
    )
    return parser


def collect_inputs(args: argparse.Namespace) -> tuple[str, int, int]:
    """Use CLI values when supplied and prompt for any missing values."""
    target = args.target or input("Target hostname or IPv4 address: ").strip()
    start_port = args.start_port
    end_port = args.end_port

    if start_port is None:
        start_port = port_number(input("Start port: ").strip())
    if end_port is None:
        end_port = port_number(input("End port: ").strip())

    validate_port_range(start_port, end_port)
    return target, start_port, end_port


def print_banner() -> None:
    print(Figlet(font="small").renderText("Port Scanner"))
    print("TCP connect scan | authorized systems only\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    print_banner()

    try:
        target, start_port, end_port = collect_inputs(args)
        ip_address = resolve_target(target)
    except (ValueError, argparse.ArgumentTypeError) as exc:
        parser.error(str(exc))

    print(f"Target: {target} ({ip_address})")
    print(f"Range:  {start_port}-{end_port}/tcp")
    print(f"Timeout: {args.timeout:g}s\n")

    open_ports = scan_ports(ip_address, start_port, end_port, args.timeout)
    print(f"\nScan complete: {len(open_ports)} open port(s) found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
