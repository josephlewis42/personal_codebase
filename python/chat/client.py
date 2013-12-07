#!/usr/bin/python

from socket import *

#Define Variables
host = "localhost"
port = 21567
buf = 1024
addr = (host,port)
username = "User"

# Create socket
UDPSock = socket(AF_INET,SOCK_DGRAM)


def setup():
    '''
    Sets up the user profile, and the connection to the other computer
    '''
    #Import Globals
    global host
    global port
    global addr
    global username
    
    
    print "Where do you want to connect to?"
    host = raw_input('Host >> ')
    if not host:
        host = "localhost"
    print "What port, the usual is 21567?"
    port = raw_input('Port >> ')
    if not port:
        port = 21567
    addr = (host,int(port))
    print "";
    username = raw_input('Username >> ')
    if not username:
        username = "User"
    
def startTalking():
    print "===Enter message to send to server===";

    # Send messages
    while (1):
	    data = raw_input('>> ')
	    if not data:
		    #Close the port on the server so it can exit
	        UDPSock.sendto(data,addr)
	    	break
	    else:
	    	if(UDPSock.sendto(username + " : " + data,addr)):
	    		print "Sending message '",data,"'....."
    
    # Close socket
    UDPSock.close()

def start():
    setup()
    startTalking()

if __name__ == '__main__':
    # This code runs when script is started from command line
    start()
    SystemExit()
    exit()
