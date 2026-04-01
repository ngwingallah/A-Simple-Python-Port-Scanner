import sys
import socket
import csv
import json 
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Function to scan a single port
def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0) 
            result = s.connect_ex((target, port))
                        
            if result == 0:
                banner = "No banner"
                try:
                    # Attempt to receive the banner
                    banner_bytes = s.recv(1024)
                    if banner_bytes:
                        banner = banner_bytes.decode('utf-8', errors='ignore').strip()
                    else:
                        # Probe for silent services like HTTP
                        s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
                        banner_bytes = s.recv(1024)
                        if banner_bytes:
                            banner = banner_bytes.decode('utf-8', errors='ignore').splitlines()[0]
                except:
                    banner = "Service detected (No banner sent)"
                
                # Return the data dictionary to the main loop
                return {"port": port, "status": "open", "banner": banner}
    except:
        pass
    return None

#Define a target
if len(sys.argv) < 2:
    print("Usage: python3 portscanner.py <ip_or_hostname>")
    sys.exit()

try:
    target = socket.gethostbyname(sys.argv[1])
except socket.gaierror:
    print("\n[✘] Error: Hostname could not be resolved.")
    sys.exit()

open_ports = []
start_time = datetime.now()

print("=" * 50)
print(f"Scanning Target: {target}")
print(f"Started at: {start_time}")
print("=" * 50)

#Collect results using Threading
try:
    with ThreadPoolExecutor(max_workers=100) as executor:
        # Create a list of tasks for ports 1-1024
        futures = [executor.submit(scan_port, target, port) for port in range(1, 1025)]
        for f in futures:
            res = f.result()
            if res:
                open_ports.append(res)
                # Print immediately so you can see progress
                print(f"[+] Port {res['port']:5} is OPEN | Banner: {res['banner']}")
except KeyboardInterrupt:
    print("\n[!] Scan interrupted by user. Saving partial results...")

# Export
if open_ports:
    # Create unique name using IP and Time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    safe_target = target.replace(".", "_")
    
    csv_file = f"scan_{safe_target}_{timestamp}.csv"
    json_file = f"scan_{safe_target}_{timestamp}.json"

    print(f"\n[+] Attempting to save {len(open_ports)} results...")
    
    # Export to CSV
    try:
        with open(csv_file, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["port", "status", "banner"])
            writer.writeheader()
            writer.writerows(open_ports)
        print(f"[✔] CSV saved: {os.path.abspath(csv_file)}")
    except Exception as e:
        print(f"[✘] Failed to save CSV: {e}")

    # Export to JSON
    try:
        with open(json_file, 'w') as f:
            json.dump(open_ports, f, indent=4)
        print(f"[✔] JSON saved: {os.path.abspath(json_file)}")
    except Exception as e:
        print(f"[✘] Failed to save JSON: {e}")
else:
    print("\n[!] No open ports found. No files created.")

print(f"\nScanning finished at: {datetime.now()}")