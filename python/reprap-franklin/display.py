#!/usr/bin/env python
'''Provides a main GUI for the RepRap Franklin.

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

from Tkinter import *
import tkMessageBox
import tkFileDialog
import time

import firmware
import inputs
import reprap


__author__ = "Joseph Lewis"
__copyright__ = "Copyright 2011 Joseph Lewis <joehms22@gmail.com>, GPL2 license."
__license__ = "GPL"
__version__ = "20110311"


#Filetypes for tk open/save dialogs.
GCODE_FILETYPE = ("GCode Files", ".gcode")
PS_FILETYPE = ("Post Script", ".ps")
ALL_FILETYPE = ("All Files", ".*")


class Display:
    '''A GUI display for the program.'''

    waittime = 0.1  #Time to sleep between drawing cycles.

    def speed_closer(self, time):
        '''Creates and returns a function for setting the wait_time to
        a certain value.

        Paramaters:
            time - The time to create the function for setting waittime to.
        Return:
            A function that sets waittime to the given time.

        '''
        def settime():
            self.waittime = time
            self.notify("Setting delay to: %s, this may take a moment." % (time))
        return settime


    def timer(self):
        '''Called by inputs to delay their inputs for a user determined
        amount of time.  Also pauses if the emulated RepRap is paused.

        '''
        time.sleep(self.waittime)

        while self.rep.paused:
            time.sleep(1)



    def save(self):
        '''Saves the print bed view as a post-script file.'''
        loc = tkFileDialog.asksaveasfilename(defaultextension=".ps", filetypes=[PS_FILETYPE])

        if not loc:
            self.notify("Save image canceled.")
            return

        try:
            f = open(loc, 'w')
            f.write( self.canvas.postscript() )

            self.notify("Saved image to %s" % (loc))

        except IOError, e:
            self.notify("Couldn't save image: %s." % (e))


    def file_input(self):
        loc = tkFileDialog.askopenfilename(filetypes=[GCODE_FILETYPE, ALL_FILETYPE])
        if not loc:
            return

        f = inputs.file_input.FileInput(self.rep, loc, self.timer)
        f.start()
        self.notify("Using file %s as input." % (loc))


    def unix_input(self):
        '''Setus up the input as a unix socket.'''
        loc = tkFileDialog.askopenfilename()
        if not loc:
            return

        f = inputs.unix_socket.UNIXSocketInput(self.rep, loc, self.timer)
        f.start()
        self.notify("Using file %s as input." % (loc))


    def firmware_changer(self, fw):
        '''Takes in a class and returns a function to change to the
        firmware represented by the given class.

        '''
        def change_firmware():
            self.rep.current_firmware = fw(self.rep)
            self.notify("Changed firmware to %s" % fw.title)

        return change_firmware

    def toggle_paused(self):
        '''Toggles the paused state of the RepRap.'''
        self.rep.paused = not self.rep.paused
        if self.rep.paused:
            self.notify("Paused")
        else:
            self.notify("Un-Paused")


    def setup_reprap(self):
        '''Draw the text and dividing lines on the bed.'''
        self.rep = reprap.RepRap()

        bed = self.rep.bed  #Shorten future commands by nine chars.

        #Place to draw the output.
        self.canvas = Canvas(self.root, width=bed.bed_width, height=bed.bed_height, bg="#6BB56B")

        self.canvas.pack(side=TOP)
        bed.canvas = self.canvas

        bed.reset()  #Draw dividing lines for displays.

    def clear_canvas(self):
        #print dir(self.rep.bed.xy_canvas)
        self.rep.bed.canvas.delete(ALL)
        self.rep.bed.reset()



    def notify(self, text):
        '''Notifies the user of an event.'''

        t = time.strftime("%H:%M:%S")

        text = "%s - %s\n" % (t, text)

        self.notify_panel.insert(END, text)
        self.notify_panel.see(END)


    def __init__(self):
        root = Tk(className=" RepRap Franklin")
        self.root = root

        #Setup Menus
        menu = Menu(root)
        root.config(menu=menu)

        filemenu = Menu(menu)
        menu.add_cascade(label="Display", menu=filemenu)
        filemenu.add_command(label="Save As...", command=self.save)
        filemenu.add_command(label="Clear", command=self.clear_canvas)
        filemenu.add_command(label="Quit", command=exit)

        repmenu = Menu(menu)
        menu.add_cascade(label="RepRap", menu=repmenu)

        #Add all the possible firmwares.
        fw_menu = Menu(repmenu)
        repmenu.add_cascade(label="Change Firmware", menu=fw_menu)
        for i in firmware.full.Firmware.__subclasses__():
            fw_menu.add_command(label=i.title, command=self.firmware_changer(i))

        repmenu.add_separator()
        repmenu.add_command(label="Pause", command=self.toggle_paused)

        #Input menu (select gcode source)
        inputmenu = Menu(menu)
        menu.add_cascade(label="Input Source", menu=inputmenu)
        inputmenu.add_command(label="File...", command=self.file_input)
        inputmenu.add_command(label="UNIX Socket...", command=self.unix_input)

        #Speed menu
        speed_menu = Menu(menu)
        menu.add_cascade(label="Delay", menu=speed_menu)

        for i in [0, 0.005, 0.01, 0.1, 0.2, 0.5, 1, 2, 5]:
            speed_menu.add_command(label="%s seconds" % i, command=self.speed_closer(i))


        #Notification panel for the user.
        self.notify_panel = Text(root, height=5)
        self.notify_panel.pack(side=BOTTOM)

        self.setup_reprap()

        self.notify(__copyright__)

        mainloop()

if __name__ == "__main__":
    d = Display()