import pyfiglet
import sys
import socket
from datetime import datetime

ascii_banner = pyfiglet.figlet_format("Simple  Port Scanner")
print(ascii_banner)

target = input(str("Target IP: "))

#Banner
print("_" * 50)
print()
print("Scanning " + target)
print ("Scanning started at: " + str(datetime.now()))
print("_" * 50)
print()

try:
    #Scan everyport in target
    for port in range(1,65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)

        #Return open ports
        result = s.connect_ex((target,port))
        if result == 0:
            print("[*] Port {} is open".format(port))
        s.close()

except KeyboardInterrupt:
    print("Exiting :(")
    sys.exit()

except socket.error:
    print("Host not responding :(")
    sys.exit()
    