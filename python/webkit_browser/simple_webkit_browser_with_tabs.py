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

    Copyright 2010-08-21 Joseph Lewis <joehms22@gmail.com>
'''

import gtk 
import webkit 

#Constants
BROWSER_NAME = "Simple Browser"

class MyWebBrowser(gtk.VBox):
    def __init__(self):
        #Init the program, essentially just create the gtk environment
        self.label = gtk.Label("") #Holds the title

        
        #Create the vbox to hold the menubar and gtkwindow
        self.vbox = gtk.VBox(False, 2)
        
        self.view = webkit.WebView()
        self.view.open("http://www.google.com/")
        self.view.connect('title-changed', self.update_title_bar)
        self.view.connect('document-load-finished', self.doc_load_finished)
        
        self.sw = gtk.ScrolledWindow() 
        self.sw.add(self.view) 
        
        self.make_menu_bar()
        
        self.vbox.pack_end(self.sw)
        
        
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
        '''Goes to the url provided in the input box.  Also adds www
        and http, if needed.'''
        url = self.url_entry.get_text()
        
        #if not url.startswith("www.") and not url.startswith("http://"):
        #    url = "http://www."+url
            
        if not url.startswith("http://"):
            url = "http://"+url
        
        self.view.open(url)

    def update_title_bar(self, webview, frame, title):
        '''Updates the title bar when a webpage title is changed.'''
        self.label.set_label(title)
        
    def doc_load_finished(self, webview, unknown):
        '''Changes browser settings when a url is loaded, like location bar, and 
        title.'''
        #Set the title for the page
        self.label.set_label(str(self.view.get_property("title")))
        #Set the new uri
        self.url_entry.set_text( self.view.get_property("uri") )
        
    def page_back(self, event):
        '''Go back a page.'''
        self.view.go_back()
        
    def page_forward(self, event):
        '''Go forward a page.'''
        self.view.go_forward()
        

class MyNotebook(gtk.Notebook):

  def __init__(self):
    gtk.Notebook.__init__(self)
    #set the tab properties
    #self.set_property('homogeneous', True)

  def new_tab(self):
    #Create a new browser to put in the tab
    browser = MyWebBrowser()
    browser_label = browser.label
    browser_vbox = browser.vbox
    browser_vbox.show_all()
    nbpages = self.get_n_pages()
    
    self.append_page(browser_vbox)
    #we create a "Random" image to put in the tab
    image = gtk.Image()
    nbpages = self.get_n_pages()
    icon = gtk.STOCK_ABOUT
    image.set_from_stock(icon, gtk.ICON_SIZE_DIALOG)
    #self.append_page(image)
   
    #creation of a custom tab. the left image and
    #the title are made of the stock icon name
    #we pass the child of the tab so we can find the
    #tab back upon closure
    label, tochild = self.create_tab_label(browser_label, browser_vbox)
    label.show_all()
    
    browser.label = tochild
   
    self.set_tab_label_packing(image, True, True, gtk.PACK_START)
    #self.set_tab_label(image, label)
    self.set_tab_label(browser_vbox, label)
    image.show_all()
    self.set_current_page(nbpages)
 
  def create_tab_label(self, title, tab_child):
    box = gtk.HBox()
    title = gtk.Label("Tab")
    closebtn = gtk.Button()
    #the close button is made of an empty button
    #where we set an image
    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
    closebtn.connect("clicked", self.close_tab, tab_child)
    closebtn.set_image(image)
    closebtn.set_relief(gtk.RELIEF_NONE)
    box.pack_start(title, True, True)
    box.pack_end(closebtn, False, False)
    return box, title
 
  def close_tab(self, widget, child):
    pagenum = self.page_num(child)
 
    if pagenum != -1:
      self.remove_page(pagenum)
      child.destroy()
        
def on_destroy(win):
    gtk.main_quit()
 
def on_delete_event(widget, event):
    gtk.main_quit()

def new_tab(widget):
    notebook.new_tab()
  
if __name__ == "__main__":
    window = gtk.Window()
    
    window.set_title( BROWSER_NAME )
    window.resize(600,400)
    
    box = gtk.VBox()
    button = gtk.Button("New Tab")
    box.pack_start(button,False)
    button.connect("clicked", new_tab)

    notebook = MyNotebook()
    box.pack_start(notebook)
    window.add(box)
    window.connect("destroy", on_destroy)
    window.connect("delete-event", on_delete_event)
    window.show_all()
    gtk.main()
