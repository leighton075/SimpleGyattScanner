import nmap
import time
import os
import platform

def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    response = os.system(f"ping {param} 1 {host}")
    
    if response == 0:
        return True # Host is reachable
    else:
        return False # Host is unreachable or blocking pings

def scan_os(target_ip):
    nm = nmap.PortScanner()
    
    print(f"Scanning {target_ip} for OS...")
    nm.scan(target_ip, arguments="-O")
    
    if target_ip in nm.all_hosts():
        if 'osmatch' in nm[target_ip]:
            os_details = nm[target_ip]['osmatch']
            print(f"OS detected: {os_details[0]['name']} ({os_details[0]['accuracy']}%)")
        else:
            print(f"Could not detect OS for {target_ip}")
    else:
        print(f"Host {target_ip} not found in the scan results.")

def scan_subnet(subnet):
    nm = nmap.PortScanner()
    
    print(f"Scanning subnet: {subnet}")
    nm.scan(hosts=subnet, arguments="-O")
    
    # Check through hosts
    for host in nm.all_hosts():
        print(f"Host: {host}")
        if 'osmatch' in nm[host]:
            os_details = nm[host]['osmatch']
            print(f"OS detected: {os_details[0]['name']} ({os_details[0]['accuracy']}%)")
        else:
            print(f"OS not detected for {host}")
        print("-" * 50)

def main():
    target = input("Enter a target IP address or subnet (e.g., 192.168.1.0/24): ")
    
    if not ping(target):
        print(f"Host {target} is unreachable or blocking pings.")
    else:
        print(f"Host {target} is reachable, proceeding with scan...")
    
    # Check to see if what they entered was a single ip or subnet
    if '/' not in target:
        scan_os(target)
    else:
        scan_subnet(target)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Scan completed in {end_time - start_time:.2f} seconds.")
