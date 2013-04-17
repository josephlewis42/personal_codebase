#!/usr/bin/env python3
''' A program to send messages via DNS queries.
Copyright 2013 Joseph Lewis <joehms22@gmail.com> | <joseph@josephlewis.net>

MIT License
'''

import subprocess

DNS_SERVER = '8.8.8.8'
DOMAIN_NAME = "www.testdnsflagsetting{}.com"
NORECURSE_OPT = "+norecurse"

msg = raw_input("Enter a message, or blank to receive: ")

def read_byte(byteno):
	byte = "0b"
	for i in range(byteno * 8, (byteno + 1) * 8):
		output = subprocess.check_output(['dig','@{}'.format(DNS_SERVER), DOMAIN_NAME.format(i), NORECURSE_OPT]) 
		if ";; AUTHORITY SECTION:" in output:
			byte += '1'
		else:
			byte += '0'
	
	return int(byte, 2) # converts binary to an int

def write_byte(byteno, byte):
	to_write = bin(byte)[2:].zfill(8) # gets binary representation of a byte
	for loc, b in enumerate(to_write):
		if b == '1':
			i = (byteno * 8) + loc
			subprocess.check_output(['dig','@{}'.format(DNS_SERVER), DOMAIN_NAME.format(i)])
			print "Wrote 1 at: {}".format(i)

if len(msg) == 0:
	message = ""
	for byte in range(1,read_byte(0) + 1): # first byte is length of message
		message += chr(read_byte(byte))
	
	if len(message) > 0:
		print message
	else:
		print "[No Message]"

else:
	total = len(msg)
	write_byte(0, total)
	for loc, char in enumerate(msg):
		write_byte(loc + 1, ord(char))
	
	print "Message written"
