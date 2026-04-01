import sys
import socket 
from datetime import datetime

#Define a target
if len(sys.argv) == 2:
    #Translate hostname name to IPv4
    target = socket.gethostbyname(sys.argv[1])
else:
    print("Please enter target's hostname or IP address")

#Show scan info
print("=" * 45)
print("Scan target: " + target)
print("Scanning started: " + str(datetime.now()))
print("=" * 45)

#Run the scan 
try:
    #Scan  specified ports
    for port in range (1, 1023):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        #scan results
        results = s.connect_ex((target,port))
        if results == 0:
            print("Port number {} is open".format(port))
        s.close()

#Interrupt a scan
except KeyboardInterrupt:
    print("\n scan interrupted by user")
    sys.exit()