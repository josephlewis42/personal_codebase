#!/usr/bin/python
#       get_firefox_bookmarks.py
#       
#       Copyright 2010 Joseph Lewis III <joehms22@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

'''
Gets firefox bookmarks and saves them to ~/Backup/Firefox Bookmarks as a
json document that can be restored in firefox manually later. 
Bookmarks > Organize Bookmarks [Import/Export]
'''

print 'Retrieveing Firefox Bookmarks, please shut down Firefox before doing this operation.'
import os

#Get folder location
firefoxdir = os.path.expanduser("~/.mozilla/firefox")
os.chdir(firefoxdir)

#Get Profile information
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('profiles.ini')
firefoxdir += "/" + config.get("Profile0", "Path") + "/bookmarkbackups"

os.chdir(firefoxdir)

#Get json documents in file
list = os.listdir(firefoxdir)

#Get the most recent bookmark save file
list.sort()
list.reverse()
firefoxdir += "/" + list[0] 

savedir = os.path.expanduser("~/Backup/Firefox Bookmarks/")

#copy it to savedir
import shutil
shutil.copy(firefoxdir, savedir)
