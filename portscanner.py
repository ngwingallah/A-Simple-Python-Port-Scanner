import sys
import socket 
from datetime import datetime

#Define a target
if len(sys.argv) == 2:
    #Translate hostname name to IPv4
    try:
        target = socket.gethostbyname(sys.argv[1])
    except socket.gaierror:
        print("\n Hostname could not be resolved. Exiting.")
        sys.exit()
else:
    print("Usage: python3 portscanner.py <ip>")
    sys.exit()

#Show scan info
print("=" * 45)
print("Scan target: " + target)
print("Scanning started: " + str(datetime.now()))
print("=" * 45)

#Run the scan 
try:
    #Scan  specified ports
    for port in range(1, 1024):
        # Use a context manager (with) to automatically close the socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            socket.setdefaulttimeout(0.5) 
            result = s.connect_ex((target, port))
            if result == 0:
                print(f"Port {port:5}: OPEN")

#Interrupt a scan
except KeyboardInterrupt:
    print("\n Scan stopped by user.")
    sys.exit()
except socket.error:
    print("\n Server not responding. Exiting.")
    sys.exit()