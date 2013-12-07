'''
Copyright 2009 Joseph A Lewis III Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License. 
'''

#Imports
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep, path
import mimetypes
import time
import sys
import os
import socket

#Data
port_number = 8000
indexpath = "/index.html"
_404 = "/404.html"
webdir = curdir + "/siteroot"
errordir = "/errors"
host_name = ""

class RequestHandler(BaseHTTPRequestHandler):
    
    global webdir
    global indexpath
    
    def do_HEAD(self):
        '''
        Sends the headders for the content, by guessing the mime
        based on the extention
        '''
        mime = mimetypes.guess_type(self.path) #Guess MIME
        self.send_response(200) #Send Client OK Response
        self.send_header('Content-type', mime)
        self.end_headers()
    
    def do_GET(self):
        '''
        Sends the client the web page/file that they requested.
        This also takes care of the index file.
        '''
        
        #Show The Headder
        mime = mimetypes.guess_type(self.path) #Guess MIME
        self.send_response(200) #Send Client OK Response
        self.send_header('Content-type', mime)
        self.end_headers()
        try:
            #If the path is blank show the index
            if self.path == "/":
                self.path = indexpath
            
            #Send the user the web file
            f = open(webdir + self.path)
            self.wfile.write(f.read())
            f.close()
        except(IOError):
            '''
            Show the 404 error for pages that are unknown.
            '''
            f = open(webdir + errordir + _404)
            self.wfile.write(f.read())
            f.close()

def start():
    '''
    Sets up and starts the webserver.
    '''
    #Imports
    global host_name
    global port_number
    
    #Tell the admin when the server started
    print "Started HTTPServer, press Control + C to quit."
    print time.asctime(), "Server Starts - Host:%s Port:%s" % (host_name, port_number)
    
    #Start the server
    server = HTTPServer((host_name,port_number), RequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print time.asctime(), "Server Stops"
        server.server_close()

def read_config():
    import ConfigParser
    
    global port_number
    global indexpath
    global _404
    global webdir
    global errordir
    global host_name
    global password
    
    config = ConfigParser.ConfigParser()
    config.read(curdir + '/Configuration/configure.cfg')
    
    #Set all vars from the file
    _404 = config.get('Pages', '_404')
    webdir = curdir + config.get('Pages', 'siteroot')
    errordir = config.get('Pages', 'error_dir')
    indexpath = config.get('Pages', 'index')
    config.get('Server', 'host_name') # The commented section gets the hostname from the file #host_name = socket.gethostname()
    port_number = int(config.get('Server', 'port'))
def main():
    read_config()
    start()
if __name__ == '__main__':
    main()
