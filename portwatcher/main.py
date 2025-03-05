import socket
import time
import json
import os

LOG_FILE = "port_status.json"

def scan_ports(host="localhost", ports=range(1, 1025)):  # Limiting to 1024 for speed
    """Scan ports on a given host and return open/closed ports."""
    open_ports = []
    closed_ports = []

    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Timeout for faster scanning
            result = s.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
            else:
                closed_ports.append(port)

    return open_ports, closed_ports

def load_previous_status():
    """Load previous port status from the log file."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_status(open_ports, closed_ports):
    """Save current port status to the log file."""
    status = {"open_ports": open_ports, "closed_ports": closed_ports, "timestamp": time.ctime()}
    with open(LOG_FILE, "w") as f:
        json.dump(status, f, indent=4)

def detect_changes(previous_status, current_open_ports):
    """Detect if any port has closed or opened."""
    previous_open_ports = set(previous_status.get("open_ports", []))
    newly_closed = previous_open_ports - set(current_open_ports)
    newly_opened = set(current_open_ports) - previous_open_ports

    return list(newly_opened), list(newly_closed)

def main():
    """Main function to scan ports and log changes."""
    print("🔍 Scanning ports...")

    open_ports, closed_ports = scan_ports()
    previous_status = load_previous_status()
    newly_opened, newly_closed = detect_changes(previous_status, open_ports)

    if newly_opened:
        print(f"🔵 New open ports: {newly_opened}")
    if newly_closed:
        print(f"🔴 Ports closed: {newly_closed}")

    save_status(open_ports, closed_ports)
    print(f"✅ Scan complete. Log saved in {LOG_FILE}")

if __name__ == "__main__":
    main()
