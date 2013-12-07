#!/usr/bin/env python
'''
Copyright (c) 2010 Joseph Lewis <joehms22@gmail.com>

SIMPLE DNS TEST SERVER

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''

import socket
import time

UDP_IP = 'localhost'
UDP_PORT = 53  #53 is the standard for DNS.
BUFFER_SIZE = 1024
LOG_FILENAME = "DNS.log"

qdb = {'google.p2p':'74.125.230.80','home.p2p':'192.121.86.88','localhost.p2p':'127.0.0.1'}

class DNS():
    ''' This class is for creating a simple DNS server.'''
    
    def start(self):
        '''Starts the DNS and gets it listening.'''
               
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind( (UDP_IP, UDP_PORT) )
            
            print("Server starts at: %s:%d" % (UDP_IP, UDP_PORT))
            self.log_time() 
        except socket.error,e:
            print("Error connecting to socket: %s" % (e))
            exit()
        while True:  #Accept Unlimited Connections
            try:  #If the connection closes before ready it will cause an error.

                #Receive data
                data, addr = s.recvfrom(BUFFER_SIZE)

                #If there is garbage notify the admin.
                if not data: break

                #Get a response.
                query, ip, packet = self.proc_data(data)

                #Send the packet back.
                self.log(str(addr) + " : " + query + " <--> " + ip)
                s.sendto(packet, addr)
            except KeyboardInterrupt:
                print("Control + c pressed exit() called...")
                self.log_time()
                exit()
            except:
                self.log("Connection error, possibly a portscan.")
                self.log_time()
                

                
    def log_time(self):
        '''Logs the current time.'''
        self.log('Time UTC:   ' + str(time.asctime(time.gmtime())) + "\n")
        self.log('Time Local: ' + str(time.asctime(time.localtime())) + "\n")
                
    def log(self, data):
        '''Logs any data sent to the file specified by LOG_FILENAME.'''
        
        print( str( data.replace("\n", "") ) )  #Give visual feedback.
        
        log_file = open(LOG_FILENAME, 'a')
        log_file.write( str(data) )
        log_file.close()

    def proc_data(self, data):
        ''' Processes the data. Return the return packet as a string. and the 
        query site.
        

            This is what the original packet looks like (taken from the rfc).
            http://www.faqs.org/rfcs/rfc1035.html
            
                                            1  1  1  1  1  1
              0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                      ID                       |  char 0,1
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |  char 2,3
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                    QDCOUNT                    |  char 4,5
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                    ANCOUNT                    |  char 6,7
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                    NSCOUNT                    |  char 8,9
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
            |                    ARCOUNT                    |  char 10,11
            +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


            
        '''
        #First 16 bits are query ID
        qid = data[0:2]

        #Next sixteen bits are query info (changes to strings of bits)
        first = bin(ord(data[2]))[2:]
        second = bin(ord(data[3]))[2:]

        #Query or response?
        qr = bool(int(first[0]))
        
        #Opcode (0,1 or 2) remove all but first four bits
        #opcode = eval('0b'+first[1:5])
        opcode = (ord(data[2]) >> 3) & 15 
        
        #QDCOUNT         an unsigned 16 bit integer specifying the number of
        #                entries in the question section.
        qdcount = data[4:6]
        
        #ANCOUNT         an unsigned 16 bit integer specifying the number of
        #                resource records in the answer section.
        ancount = data[6:8]
        
        #NSCOUNT         an unsigned 16 bit integer specifying the number of name
        #                server resource records in the authority records
        #                section.
        nscount = data[8:10]

        #ARCOUNT         an unsigned 16 bit integer specifying the number of
        #                resource records in the additional records section.
        arcount = data[10:12]
        
        #Query (for now assume that there is only one)
        #Query starts with a number of characters, then prints that 
        #number of chars, then another number, then prints that, etc
        #until we get a 0
        
        query = ''
        
        pos=12
        length=ord(data[pos])
        while length:
            query += data[pos+1 : pos+length+1] + '.'
            pos += length + 1
            length = ord(data[pos])
        #Remove trailing dot.
        query = query[:-1]

        #Only look up our domains
        if query.endswith('.p2p') and not query.endswith('.icann.p2p'):
            try:
                if query.startswith('www.'):  #Save db space by not storing wwws
                    query = query[4:]
                ip = qdb[query]
            except:
                self.log("Query not in DB: %s" % (query))
                ip = '0.0.0.0'
        else:
            try:
                ip = socket.gethostbyname(query)
            except:  #Can't reach dns, just send back nothing.
                ip = '0.0.0.0'


        #CONSTRUCT RESPONSE:
        response = ''
        
        #Add the query id
        response += qid
        
        #Add response header.
        #  0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
        #|QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
        response += chr(0b10000000) + chr(0b0000000)

        #Add qd count
        response += qdcount
        
        #Add answer count (same as qd count) FIXME Will fail with more than one msg.
        response += qdcount

        #Add aanswer coundt
        response += chr(0b0) + chr(0b0) + chr(0b0) + chr(0b0)

        #Add original question
        response += data[12:]

        #Add pointer for message compression: 
        #See RFC Section 4.1.4. Message compression
        response += chr(0b11000000) + chr(0b1100)

        #TYPE    two octets containing one of the RR type codes.  This
        #        field specifies the meaning of the data in the RDATA
        #        field.
        response += chr(0b00000000) + chr(0b00000001)
        
        #CLASS   two octets which specify the class of the data in the
        #        RDATA field.
        response += chr(0b00000000) + chr(0b00000001)

        #TTL     a 32 bit unsigned integer that specifies the time
        #        interval (in seconds) that the resource record may be
        #        cached before it should be discarded.  Zero values are
        #        interpreted to mean that the RR can only be used for the
        #        transaction in progress, and should not be cached.
        #
        #This should be the same length of time until next DNS cache update, for
        #now don't cache.
        response += chr(0b00000000) + chr(0b00000000) + chr(0b00000000) + chr(0b00000000)
        
        #RDLENGTH    an unsigned 16 bit integer that specifies the length in
        #            octets of the RDATA field.
        #
        #For now this is 4 bytes (size of an ip address)
        response += chr(0b00000000) + chr(0b00000100)
        
        #RDATA   a variable length string of octets that describes the
        #        resource.  The format of this information varies
        #        according to the TYPE and CLASS of the resource record.
        #        For example, the if the TYPE is A and the CLASS is IN,
        #        the RDATA field is a 4 octet ARPA Internet address.
        response += socket.inet_aton(ip)

        return (query, ip, response)
            
if __name__ == "__main__":

    print("Simple DNS server written by Joseph Lewis <joehms22@gmail.com>")

    value = ""
    while value != 'y' and value != 'n':
        value = raw_input("Do you want to bind externally y/n?")

    if value == 'y':
        #Find our external ip
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 80))
        UDP_IP = s.getsockname()[0]
    else:
        UDP_IP = 'localhost'
    DNS().start()
