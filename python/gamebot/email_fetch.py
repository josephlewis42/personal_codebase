#!/usr/bin/env python
'''Provides an ability to send and recieve emails.

The EmailInterface class allows checking of an email box on demand,
along with on a fixed interval.

Copyright 2011 Joseph Lewis <joehms22@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.


'''

import threading
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import email
import os
import poplib

__author__ = "Joseph Lewis"
__copyright__ = "Copyright 2011, Joseph Lewis"
__license__ = "GPL"
__version__ = ""

DEBUG = False


class SimpleMessage:
    subject = ""
    to = ""
    personfrom = ""
    def __init__(self, raw_email):
        
        self.message = raw_email
        self.clean = raw_email.lower()
        
        lines = self.clean.split("\n")
        
        for line in lines:
            if line.startswith("from:"):
                self.personfrom = line[6:]
            if line.startswith("to:"):
                self.to = line[4:]
            if line.startswith("subject:"):
                self.subject = line[9:]

class NotConfiguredException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class EmailInterface( threading.Thread ):
    
    _smtp_configured = False
    _pop_configured = False
    kill_me = False
    time = 0
    
    
    def __init__(self, callback=None, time=None):
        ''' Connects every time seconds to check for new mail. If there
        is new mail, mail_callback will be called and passed the new message
        one message per call.
        
        '''
        self.time = time
        self.callback = callback
                
        threading.Thread.__init__(self)
        
    
    def configure_smtp(self, username, password, host, port):
        self._smtp_configured = True
        self.smtp_url = host
        self.smtp_port = port
        self.smtp_username = username
        self.smtp_password = password
        
        if DEBUG:
            print("Setting up SMTP: %s@%s:%s" % (username, host, port))
        
    
    def configure_pop(self, username, password, host, port=110, SSL=False):
        self._pop_configured = True
        self.pop_host = host
        self.pop_port = port
        self.pop_username = username
        self.pop_password = password
        self.pop_SSL = SSL

        if DEBUG:
            print("Setting up POP: %s@%s:%s" % (username, host, port))
        
    
    def run(self):
        if not isinstance(self.time, (float,int,long)):
            return
        
        while not self.kill_me:
            time.sleep(self.time)
            
            try:
                if DEBUG:
                    print ("%s - Checking mail" % (time.strftime("%Y-%m-%d %H:%M:%S")))
                msgs = self.check_mail()
            except NotConfiguredException:
                print("POP not yet configured.")
            
            if DEBUG:
                print ("%s - %s messages." % (time.strftime("%Y-%m-%d %H:%M:%S"), len(msgs))) 
            for i in msgs:
                if callable(self.callback):
                    self.callback(i)
        
        
    def kill():
        '''Kills the mail checking thread.'''
        self.kill_me = False
        
        
    def check_mail(self):
        '''Checks the mail for the given account, returns a list of 
        messages in the Inbox.
        
        If POP is not configured a NotConfiguredException is raised.
        '''
        
        if not self._pop_configured:
            raise NotConfiguredException
        
        msgs = []
        
        if self.pop_SSL:
            pop = poplib.POP3_SSL(self.pop_host, self.pop_port)
        else:
            pop = poplib.POP3(self.pop_host, self.pop_port)

        try:
            pop.user(self.pop_username)
            pop.pass_(self.pop_password)
            
            numMessages = len(pop.list()[1])
            
            for i in range(numMessages):
                
                message = ""
                for line in pop.retr(i+1)[1]:
                    message += line+"\n"
                msgs.append(message)

        finally:
            pop.quit()

        return msgs
        
    
    def send_mail(self, to, subject, body, attachments=[], full_attachments={}):
        '''Sends a message to the given recipient, attachments
        is a list of file paths to attach, they will be attached with 
        the given names, and if there is a problem they won't be 
        attached and the message will still be sent.
        
        PARAMATERS:
        to - Email address to send the message to. (String)
        subject - Subject of the email (String)
        body - Body of the email (html allowed) (String)
        attachments - A list of attachments to the message.
        full_attachments - A dict of things to attach, name => data.
                           each name should be unique.
        
        Raises a NotConfiguredException if smtp has not yet been set
        up.
        '''
        
        if not self._smtp_configured:
            raise NotConfiguredException, "SMTP is not configured."
        
        # Setup the message
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = to
        msg['Subject'] = subject

        # Attach the body.
        msg.attach(MIMEText(body, 'html'))

        # Attach each attachment.
        for attach in attachments:
            with open(attach, 'rb') as o:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(o.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                       'attachment; filename="%s"' % os.path.basename(attach))
                msg.attach(part)
                
        # Attach everything from the full attachments dictionary.
        for name in full_attachments.keys():
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(full_attachments[name])
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % (name))
            msg.attach(part)

        # Beam me up Scotty!
        mailServer = smtplib.SMTP(self.smtp_url, self.smtp_port)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(self.smtp_username, self.smtp_password)
        mailServer.sendmail(self.smtp_username, to, msg.as_string())
        mailServer.close()

        if DEBUG:
            print ("%s - Message sent to: %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), to))