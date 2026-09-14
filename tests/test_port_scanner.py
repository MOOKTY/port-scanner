"""Integration tests for the original interactive scanner."""

import socket
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCANNER = PROJECT_ROOT / "src" / "port_scanner.py"


class ScannerIntegrationTests(unittest.TestCase):
    def test_interactive_scanner_detects_real_loopback_listener(self) -> None:
        """Run the real script with input() against a local TCP listener."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)
            open_port = listener.getsockname()[1]

            completed = subprocess.run(
                [sys.executable, str(SCANNER)],
                input=f"127.0.0.1\n{open_port}\n{open_port}\n",
                text=True,
                capture_output=True,
                cwd=PROJECT_ROOT,
                timeout=10,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Author: MOOKTY", completed.stdout)
        self.assertIn("Version: 1.0", completed.stdout)
        self.assertIn(f"Port {open_port} is open", completed.stdout)


if __name__ == "__main__":
    unittest.main()
