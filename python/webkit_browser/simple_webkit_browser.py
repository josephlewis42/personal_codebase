#!/usr/bin/env python
'''
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Copyright 2010 Joseph Lewis <joehms22@gmail.com>
'''

import gtk 
import webkit 

#Constants
BROWSER_NAME = "Simple Browser"

class MyWebBrowser(gtk.Window):
    def __init__(self):
        #Init the program, essentially just create the gtk environment.
        #Create the vbox to hold the menubar and gtkwindow
        self.vbox = gtk.VBox(False, 2)
        
        self.view = webkit.WebView()
        self.view.open("http://localhost/")
        self.view.connect('title-changed', self.update_title_bar)
        self.view.connect('document-load-finished', self.doc_load_finished)
        
        self.sw = gtk.ScrolledWindow() 
        self.sw.add(self.view) 
        
        self.make_menu_bar()
        
        self.win = gtk.Window() 
        self.win.set_size_request(760, 500)
        self.vbox.pack_end(self.sw)
        self.win.add(self.vbox)


        self.win.show_all()
        self.win.connect('delete_event', gtk.main_quit)
        
    def make_menu_bar(self):
        '''Makes the menu bar for the program, pretty simple really.'''
        #Make the hbox to fit everything in.
        self.menu_box = gtk.HBox(False, 5)
        
        #Make the back button and set it up.
        self.back_button = gtk.Button(stock=gtk.STOCK_GO_BACK)
        self.menu_box.pack_start(self.back_button, False, False, 0)
        self.back_button.connect("pressed",self.page_back)
        
        #Make the forward button and set it up.
        self.forward_button = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
        self.menu_box.pack_start(self.forward_button, False, False, 0)
        self.forward_button.connect("pressed",self.page_forward)
        
        #The Refresh button
        #The home button
        #The url entry box
        self.url_entry = gtk.Entry()
        self.menu_box.pack_start(self.url_entry, True, True, 0)

        #The go button
        self.go_button = gtk.Button("Go")
        self.menu_box.pack_start(self.go_button, False, False, 0)
        self.go_button.connect("pressed",self.go_to_url)
        
        self.vbox.pack_start(self.menu_box, False, False, 0)
        
    def go_to_url(self, event):
        '''Goes to the url provided in the input box.'''
        self.view.open(self.url_entry.get_text())

    def update_title_bar(self, webview, frame, title):
        '''Updates the title bar when a webpage title is changed.'''
        self.win.set_title(title)
        
    def doc_load_finished(self, webview, unknown):
        '''Changes browser settings when a url is loaded, like location bar, and 
        title.'''
        #Set the title for the page
        self.win.set_title(BROWSER_NAME + " - " + str(self.view.get_property("title")))
        #Set the new uri
        self.url_entry.set_text( self.view.get_property("uri") )
        
    def page_back(self, event):
        '''Go back a page.'''
        self.view.go_back()
        
    def page_forward(self, event):
        '''Go forward a page.'''
        self.view.go_forward()

if __name__ == "__main__":
   webbrowser = MyWebBrowser()
   gtk.main()
