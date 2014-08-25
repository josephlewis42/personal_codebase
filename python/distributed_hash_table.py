#!/usr/bin/env python3
import SocketServer, subprocess, sys
from threading import Thread

HASH_LENGTH = 32
NUM_HASHES = 2**HASH_LENGTH
START_HASH = 0
END_HASH = 0
port = 8000

next_host = ""
next_port = ""
prev_host = ""
prev_port = ""

hashed_items = {}


def recv_all(socket):
	total_data=[]
	while True:
		data = socket.recv(1024)
		if not data: break
		total_data.append(data)
	return "".join(total_data)


def pipe_command(request, host, port):

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	sock.connect((host, port))
	sock.send(request)
	
	response = recv_all(sock)
	sock.close()
	return response

class SingleTCPHandler(SocketServer.BaseRequestHandler):
	"One instance per connection.  Override handle(self) to customize action."
	def handle(self):
		# self.request is the client connection
		cmd = self.read_token() # read the command
		
		cmd = cmd.upper()
		
		if cmd == "SEARCH":
			self.search()
			
		elif cmd == "SET_LEFT":
			self.set_left()
			
		elif cmd == "SET_RIGHT":
			self.set_right()
			
		elif cmd == "STORE":
			self.store()
			
		elif cmd == "DELETE":
			self.delete()
			
		self.request.close()
	
	def read_token(self):
		"""Reads a token from the input, discarding beginning whitespace and 
		consuming a single whitepsace character after the token
		
		"""
		WHITESPACE = " \t\r\n"
		
		data = ""
		
		char = self.request.recv(1)
		while char in WHITESPACE:
			char = self.request.recv(1)
		
		while char not in WHITESPACE and char is not None:
			data += char
			char = self.request.recv(1)
		
		return data
	
	
	def hash_in_range(self, hashvalue):
		return hashvalue >= START_HASH and hashvalue < END_HASH
	
	def search(self):
		hashvalue = int(self.read_token())
		
		if self.hash_in_range(hashvalue):
			if hashvalue in hashed_items:
				self.request.send(hashed_items[hashvalue])
		else:
			self.request.send(pipe_command("SEARCH " + str(hashvalue), next_host, next_port))
			
	def set_left(self):
		prev_host = self.read_token()
		prev_port = int(self.read_token())
		
	def set_right(self):
		next_host = self.read_token()
		next_port = int(self.read_token())

	def store(self):
		hashvalue = int(self.read_token())
		
		data = recv_all(self.request)
	
		if self.hash_in_range(hashvalue):
			hashed_items[hashvalue] = data
			print("stored: {}".format(hashvalue))
		else:
			self.request.send(pipe_command("STORE " + str(hashvalue) + " " + data, next_host, next_port))
	
	def delete(self):
		hashvalue = int(self.read_token())
	
		if self.hash_in_range(hashvalue):
			hashed_items[hashvalue] = None
			print("deleted: {}".format(hashvalue))
		else:
			self.request.send(pipe_command("DELETE " + str(hashvalue) + " ", next_host, next_port))		
		


class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	# Ctrl-C will cleanly kill all spawned threads
	daemon_threads = True
	# much faster rebinding
	allow_reuse_address = True

	def __init__(self, server_address, RequestHandlerClass):
		SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)



if __name__ == "__main__":
	nodeid = int(sys.argv[1])
	maxnodes = int(sys.argv[2])
	port = int(sys.argv[3])
	
	keyspace = NUM_HASHES / maxnodes
	START_HASH = nodeid * keyspace
	END_HASH = (nodeid + 1) * keyspace
	
	print("taking hashes between: {} and {} on port {}".format(START_HASH, END_HASH, port))
	
	
	server = SimpleServer(("", port), SingleTCPHandler)
	server.serve_forever()
