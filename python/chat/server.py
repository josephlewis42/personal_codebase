# Server program

from socket import *

# Set the socket parameters
host = gethostname()
print host
port = 21567
buf = 1024
addr = (host,port)

# Check what port to open
print "What port, the usual is 21567?"
port = raw_input('Port >> ')
if not port:
    port = 21567
addr = (host,int(port))

# Create socket and bind to address
UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind(addr)

# Receive messages
while 1:
	data,addr = UDPSock.recvfrom(buf)
	if not data:
		print "Client has exited!"
		break
	else:
		print "\n" + data

# Close socket
UDPSock.close()
