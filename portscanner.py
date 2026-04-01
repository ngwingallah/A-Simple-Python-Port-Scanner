import sys
import socket 
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Function to scan a single port
def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2) # Banners can take a second to load
            result = s.connect_ex((target, port))
            
            if result == 0:
                banner = "No banner"
                try:
                    # 1. Try to receive data immediately (works for SSH, FTP, SMTP)
                    banner = s.recv(1024).decode().strip()
                    
                    # 2. If nothing received, try sending a generic probe (for HTTP)
                    if not banner:
                        s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
                        banner = s.recv(1024).decode().strip().split('\n')[0] # Get first line
                except:
                    # If we can't grab a banner, we still know it's open
                    banner = "Service detected (Banner protected/silent)"
                
                print(f"Port {port:5}: OPEN | Banner: {banner}")
    except:
        pass

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
   with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(1, 1024):
            executor.submit(scan_port, target, port)

except KeyboardInterrupt:
    print("\n Scan has stopped")
    sys.exit()

print(f"\nScanning finished at: {datetime.now()}")