import sys
import socket
import csv
import json 
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Function to scan a single port
def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5) 
                        
            if s.connect_ex((target, port)) == 0:
                banner = "No banner"
                try:
                    banner = s.recv(1024).decode().strip() or "Silent Service"
                except:
                    banner = "Protected/No Banner"
                
                # Return a dictionary for easy exporting
                return {"port": port, "status": "open", "banner": banner}
    except:
        pass
    return None

#Define a target
if len(sys.argv) < 2:
    print("Usage: python3 portscanner.py <ip>")
    sys.exit()

target = socket.gethostbyname(sys.argv[1])
open_ports = []

print(f"Scanning {target}...")

#Collect results using Threading
with ThreadPoolExecutor(max_workers=100) as executor:
    #Submit all tasks and filter out the 'None' results (closed ports)
    futures = [executor.submit(scan_port, target, port) for port in range(1, 1025)]
    for f in futures:
        res = f.result()
        if res:
            open_ports.append(res)
            print(f"Found: Port {res['port']} is OPEN")

#Export
csv_file = "scan_results.csv"
with open(csv_file, mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["port", "status", "banner"])
    writer.writeheader()
    writer.writerows(open_ports)

# 4. Export to JSON
json_file = "scan_results.json"
with open(json_file, 'w') as f:
    json.dump(open_ports, f, indent=4)

print("-" * 30)
print(f"Scan complete. Results saved to {csv_file} and {json_file}")