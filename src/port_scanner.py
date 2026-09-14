import socket

from pyfiglet import Figlet


figlet = Figlet(font="Graffiti")

print("=" * 60)
print(figlet.renderText("Port Scanner"))
print("Author: MOOKTY")
print("Version: 1.0")
print("=" * 60)
print("Simple TCP Connect Port Scanner")
print()

target = input("Enter target: ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

for port in range(start_port, end_port + 1):
    try:
        scanner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scanner_socket.settimeout(1)

        result = scanner_socket.connect_ex((target, port))

        if result == 0:
            print(f"Port {port} is open")

        scanner_socket.close()
    except Exception:
        print("Error occurred")
