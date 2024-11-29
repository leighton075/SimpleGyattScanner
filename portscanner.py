import pyfiglet
import sys
import socket
from datetime import datetime
from ipaddress import ip_address, AddressValueError
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((target, port))
            if result == 0:
                print(f"[*] Port {port} is open")
                return port
    except Exception as e:
        pass
    return None

def main():

    ascii_banner = pyfiglet.figlet_format("Simple Port Scanner")
    print(ascii_banner)

    # Target Input
    target = input("Target IP: ").strip()
    try:
        # Validate IP Address
        ip_address(target)
    except AddressValueError:
        print("Invalid IP address format. Exiting.")
        sys.exit()

    # Scan Start
    print("_" * 50)
    print("")
    print(f"Scanning {target}")
    print(f"Scanning started at: {str(datetime.now())}")
    print("_" * 50)

    # Threaded Scanning for all ports
    open_ports = []
    ports_to_scan = range(1, 65536)

    try:
        with ThreadPoolExecutor(max_workers=100) as executor:
            # Use tqdm to display progress
            with tqdm(total=len(ports_to_scan), desc="Scanning Ports", unit="port") as progress:
                futures = {executor.submit(scan_port, target, port): port for port in ports_to_scan}
                for future in futures:
                    result = future.result()
                    if result:
                        open_ports.append(result)
                    progress.update(1)  # Update progress bar

    except KeyboardInterrupt:
        print("\nExiting due to user interruption.")
        sys.exit()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit()

    # Summary
    print("\nScan complete!")
    print("_" * 50)
    if open_ports:
        print(f"Open ports on {target}: {', '.join(map(str, open_ports))}")
    else:
        print(f"No open ports found on {target}.")
    print(f"Scan finished at: {str(datetime.now())}")
    print("_" * 50)

if __name__ == "__main__":
    main()
