#!/usr/bin/env python
'''Copyright 2010 Joseph A Lewis III

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


'''
#Imports
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep, path
from SocketServer import ThreadingMixIn
import threading
import mimetypes
import time
import sys
import os
import socket
import cgi
import uuid
import urlparse


#Used as part of LiteNotes
try:
    import SQL_browser
except ImportError:
    pass


#Settings
TRY_EXTERNAL_BIND = True
THREADING = False
OPEN_BROWSER = False #opens browser on start.

#Data
port_number = 8000
indexpath = "/index.py"
webdir = curdir + "/Site"

host_name = "localhost"

if TRY_EXTERNAL_BIND:
    try:
        #Find our external ip
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 80))
        host_name = s.getsockname()[0]
    except:
        #Use internal ip (localhost).
        pass

authenticated = {}
shutdown_hook = []  #Upon shutdown of the server, each item here is called once, a good way to shut down threads.

class RequestHandler(BaseHTTPRequestHandler):

    global webdir
    global indexpath
    global authenticated
    POST_DICT = None
    COOKIE = None

    def do_HEAD(self):
        '''
        Sends the headders for the content, by guessing the mime
        based on the extention
        '''
        mime = mimetypes.guess_type(self.path) #Guess MIME
        self.send_response(200) #Send Client OK Response
        self.send_header('Content-type', mime)
        self.end_headers()

    def authenticate(self):
        a = str(uuid.uuid4())
        authenticated[a] = {'UUID':a}
        return 'sid = ' + a

    def deauthenticate(self):
        try:
            if self.COOKIE:
                authenticated.pop(self.COOKIE['sid'])
        except ValueError:
            print("Problem deauthenticating. %s")

    def redirect(self, url, cookie=True):
        '''Sends a redirect to the specified url.
        A SESSION will be started (if not already) if the cookie
        attribute is True.
        '''
        self.send_response(302) #Send Client REDIRECT Response
        self.send_header('Location', url)
        if not self.SESSION and cookie:
            self.send_header('Set-Cookie', self.authenticate())
        self.end_headers()

    def send_200(self, mime_type="text/html", cookie=True, headers={}):
        '''Sends a 200 response..
        Default mime and content are "text/html and blank respectively.
        A SESSION will be started (if not already) if the cookie
        attribute is True.

        '''
        self.send_response(200) #Send Client OK Response
        self.send_header('Content-type', mime_type)

        if not self.SESSION and cookie:
            self.send_header('Set-cookie', self.authenticate())
        
        for item in headers.keys():
            self.send_header(str(item), str(headers[item]))

        self.end_headers()

    def get_file_contents(self, path):
        '''Returns the contents of the requested file. If no contents found
        returns a blank string.'''
        try:
            a = open(path, 'rb')
            tmp = a.read()
            a.close()
            return tmp
        except IOError:
            return ""

    def parse_cookie(self):
        try:
            cookie_dict = {}

            c = self.headers['Cookie']
            c = c.split(';')

            for i in c:
                i = i.split('=')
                cookie_dict[i[0].strip()] = i[1].strip()
            self.COOKIE = cookie_dict
            return cookie_dict
        except:
            return None

    def do_GET(self):
        '''Sends the client the web page/file that they requested.
        This also takes care of the index file.

        Variables available to the client are POST_DICT, a dictionary
        of form_name and value attributes, None if no data was POSTed.
        The variable SESSION stores information about this particular
        session it is a dictionary. The variable QUERY_DICT stores
        information about the query string at the end of the url.
        '''

        filepath = urlparse.urlparse(self.path).path
        COOKIE = self.parse_cookie()

        #Get session informaiton.
        try:
            self.SESSION = authenticated[COOKIE['sid']]
        except: #Bad or no cookie.
            self.SESSION = None

        #Get the query information
        #Get the query string and query dictionary so it becomes easier to tell
        #what arguments were passed along with the url.
        query_string = urlparse.urlparse(self.path).query

        #Create the dictionary from the query string and make it global.
        self.QUERY_DICT = urlparse.parse_qs(query_string)

        #Make things more accessable to scripts.
        SESSION = self.SESSION
        QUERY_DICT = self.QUERY_DICT
        POST_DICT = self.POST_DICT

        try:
            #If the path is blank show the index
            if filepath == "/":
                filepath = indexpath

            #Hide non-public files.
            myfile = filepath.split("/")[-1]
            if myfile and myfile.startswith(".") or myfile.startswith("noweb"):
                raise IOError  #404 error, disguise the path. :)

            if filepath.endswith(".py") or filepath.endswith(".cgi"):
                with open(webdir + filepath) as f:
                    exec(f.read())
                return

            else:
                #Show The Headder
                mime = mimetypes.guess_type(filepath) #Guess MIME
                self.send_response(200) #Send Client OK Response
                self.send_header('Content-type', mime)
                self.end_headers()

                #Send the user the web file
                f = open(webdir + filepath)
                self.wfile.write(f.read())
                f.close()


        except(IOError):
            '''Show the 404 error for pages that are unknown.'''
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write("Error 404")

    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        formdata = {}
        for k in form.keys():
            formdata[k] = form[k].value

        self.POST_DICT = formdata
        #Do a standard get now.
        self.do_GET()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    '''Handles requests in a separate thread.'''

def start():
    '''Sets up and starts the webserver.'''
    print ("Started HTTPServer, press Control + C to quit.")
    print ("%s Server Starts at - http://%s:%s" % (time.asctime(), host_name, port_number) )

    #Start the server
    if THREADING:
        server = ThreadedHTTPServer((host_name, port_number), RequestHandler)
    else:
        server = HTTPServer((host_name, port_number), RequestHandler)
    try:
        if OPEN_BROWSER:
            import webbrowser
            webbrowser.open("http://%s:%d" % (host_name, port_number))
        server.serve_forever()
    except KeyboardInterrupt:
        print ("\n"*2)
        print ("%s Server Stops" % (time.asctime()))
        print ("%s Calling shutdown_hook items, waiting for threads to finish:" % (time.asctime()))
        for item in shutdown_hook:
            item()
        while threading.active_count() > 1:
            time.sleep(1)
        print ("%s Done." % (time.asctime()))
        server.server_close()

def parse_cli():
    '''
    Attempts to grab a host and portname from the command line, host
    should be argument 1 and port should be argument 2

    '''
    global host_name
    global port_number

    if len(sys.argv) == 3:
        hostname = sys.argv[1]
        port_number = int(sys.argv[2])

    elif len(sys.argv) == 2:
        port_number = int(sys.argv[1])

    print ("To set the host and port, pass a hostname and port number as arguments:")
    print ("    %s [hostname] portnumber" % sys.argv[0])


if __name__ == '__main__':
    parse_cli()
    start()