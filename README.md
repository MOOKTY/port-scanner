# >_ Port Scanner

A simple interactive TCP connect port scanner built as an early cybersecurity and Python networking project.

```text
mohammad@lab:~/port-scanner$ python src/port_scanner.py
============================================================
PORT SCANNER
Author: MOOKTY
Version: 1.0
============================================================
Simple TCP Connect Port Scanner

Enter target: 127.0.0.1
Enter start port: 20
Enter end port: 100
Port 22 is open
Port 80 is open
```

## Features

- Interactive target and port-range prompts
- Sequential TCP connect scanning
- IPv4 sockets through `socket.AF_INET`
- TCP sockets through `socket.SOCK_STREAM`
- One-second connection timeout per port
- Reports ports for which `connect_ex()` returns `0`
- Terminal banner generated with `pyfiglet`

## How it works

The script asks for a target, start port, and end port. It loops through the inclusive range one port at a time, creates a TCP/IPv4 socket, applies a one-second timeout, and calls `connect_ex((target, port))`. A result of `0` is printed as an open port.

This is a TCP connect scanner. It does not use SYN scanning, service detection, concurrency, or command-line arguments.

## Requirements

- Python 3.10 or newer
- Network access to a system you are authorized to scan
- `pyfiglet==1.0.4`

## Installation

```bash
git clone https://github.com/MOOKTY/port-scanner.git
cd port-scanner
python -m venv .venv
```

Activate the virtual environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# Linux or macOS
source .venv/bin/activate
```

Install the dependency:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the interactive scanner:

```bash
python src/port_scanner.py
```

Then enter the requested target and inclusive port range.

## Example

```text
Enter target: 192.0.2.10
Enter start port: 1
Enter end port: 1024
Port 22 is open
Port 80 is open
```

`192.0.2.10` is an IANA documentation address. Replace it with an authorized lab target.

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
- `pyfiglet` for the terminal banner
- `unittest` and `subprocess` for integration testing

## Current limitations

- Scanning is sequential, so large ranges can be slow.
- Inputs are interactive and are not validated before scanning.
- Only IPv4 TCP targets are supported.
- The scanner reports open ports only; it does not identify services or versions.
- Connection errors produce a general error message.

## Future improvements

Potential improvements can be explored in later versions without changing this repository's representation of version 1.0.

## Authorized use only

Use this tool only on systems you own or have explicit permission to test. Unauthorized scanning may violate policies or laws. You are responsible for obtaining authorization and using the software ethically.

## Author

Mohammad Okasha  
GitHub: [@MOOKTY](https://github.com/MOOKTY)
