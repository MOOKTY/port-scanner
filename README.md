<div align="center">

# `>_` Port Scanner

**A focused TCP connect scanner for authorized hosts, security labs, and networking education.**

`Python` · `TCP/IP` · `Socket Programming`

</div>

---

```text
mohammad@lab:~/port-scanner$ python src/port_scanner.py 127.0.0.1 -s 20 -e 100
 ___          _     ___
| _ \___ _ _| |_  / __| __ __ _ _ _  _ _  ___ _ _
|  _/ _ \ '_|  _| \__ \/ _/ _` | ' \| ' \/ -_) '_|
|_| \___/_|  \__| |___/\__\__,_|_||_|_||_\___|_|

TCP connect scan | authorized systems only

Target: 127.0.0.1 (127.0.0.1)
Range:  20-100/tcp
Timeout: 1s

[open] 22/tcp
[open] 80/tcp

Scan complete: 2 open port(s) found.
```

## Overview

Port Scanner performs a sequential TCP connect scan across an inclusive port range. It uses the operating system's TCP stack to attempt a complete connection to each port and reports ports that accept the connection.

## Features

- Scans a hostname or IPv4 address using TCP connect attempts
- Accepts command-line arguments or interactive prompts
- Validates targets, port values, port order, and the valid `1-65535` range
- Supports a configurable connection timeout
- Resolves the target once before scanning
- Closes every socket safely through context management
- Reports clear validation and per-port socket errors
- Uses only one small third-party dependency for the terminal banner

## How it works

1. The target is resolved to an IPv4 address.
2. The requested port range is validated.
3. A TCP socket is created for each port in sequence.
4. `connect_ex()` attempts a full TCP connection.
5. A return value of `0` is reported as an open port.
6. The socket is closed automatically before the next port is scanned.

This is a TCP connect scanner, not a SYN scanner. It does not require raw-socket or administrator privileges.

## Requirements

- Python 3.10 or newer
- Network access to an authorized target

## Installation

```bash
git clone https://github.com/MOOKTY/port-scanner.git
cd port-scanner
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux or macOS
source .venv/bin/activate
```

Install the dependency:

```bash
python -m pip install -r requirements.txt
```

## Usage

```bash
python src/port_scanner.py TARGET -s START_PORT -e END_PORT
```

Optional timeout:

```bash
python src/port_scanner.py TARGET -s START_PORT -e END_PORT --timeout 0.5
```

Run without arguments to use interactive prompts:

```bash
python src/port_scanner.py
```

View all options:

```bash
python src/port_scanner.py --help
```

## Example

Scan ports 1 through 1024 on a local lab host:

```bash
python src/port_scanner.py 192.0.2.10 --start-port 1 --end-port 1024
```

Example output:

```text
Target: 192.0.2.10 (192.0.2.10)
Range:  1-1024/tcp
Timeout: 1s

[open] 22/tcp
[open] 80/tcp

Scan complete: 2 open port(s) found.
```

`192.0.2.10` is an IANA documentation address; replace it with an authorized lab target.

## Project structure

```text
port-scanner/
├── src/
│   ├── __init__.py
│   └── port_scanner.py
├── tests/
│   └── test_port_scanner.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Technologies used

- Python
- Standard-library `socket` module
- `argparse` for the CLI
- `pyfiglet` for the terminal banner
- `unittest` for dependency-free tests

## Current limitations

- Scanning is sequential, so large ranges can be slow.
- Only IPv4 TCP targets are supported.
- The scanner reports open ports only; it does not identify services or versions.
- Results depend on network latency, filtering, firewall rules, and the configured timeout.

## Future improvements

- Optional bounded concurrency for faster scans without excessive resource use
- IPv6 support
- Optional machine-readable output
- Additional automated tests for socket outcomes

## Authorized use only

Use this tool only on systems you own or have explicit permission to test. Unauthorized scanning may violate policies or laws. You are responsible for obtaining authorization and using the software ethically.

## Author

**Mohammad Okasha**  
GitHub: [@MOOKTY](https://github.com/MOOKTY)
