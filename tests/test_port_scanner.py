"""Unit and integration tests for the port scanner."""

import argparse
import socket
import unittest
from unittest.mock import patch

from src.port_scanner import (
    port_number,
    resolve_target,
    scan_ports,
    validate_port_range,
)


class ValidationTests(unittest.TestCase):
    def test_valid_port(self) -> None:
        self.assertEqual(port_number("443"), 443)

    def test_non_numeric_port(self) -> None:
        with self.assertRaises(argparse.ArgumentTypeError):
            port_number("https")

    def test_port_outside_range(self) -> None:
        for value in ("0", "65536"):
            with self.subTest(value=value):
                with self.assertRaises(argparse.ArgumentTypeError):
                    port_number(value)

    def test_reversed_range(self) -> None:
        with self.assertRaisesRegex(ValueError, "start port"):
            validate_port_range(100, 20)

    @patch("src.port_scanner.socket.getaddrinfo")
    def test_target_resolution(self, getaddrinfo) -> None:
        getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 0))
        ]
        self.assertEqual(resolve_target("localhost"), "127.0.0.1")

    @patch("src.port_scanner.socket.getaddrinfo", side_effect=socket.gaierror)
    def test_invalid_target(self, _getaddrinfo) -> None:
        with self.assertRaisesRegex(ValueError, "unable to resolve"):
            resolve_target("not-a-real-host.invalid")


class ScannerIntegrationTests(unittest.TestCase):
    def test_scan_ports_detects_real_loopback_listener(self) -> None:
        """Exercise the real scanner against a temporary local TCP listener."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)
            open_port = listener.getsockname()[1]

            self.assertEqual(
                scan_ports("127.0.0.1", open_port, open_port, timeout=0.5),
                [open_port],
            )


if __name__ == "__main__":
    unittest.main()
