#!/usr/bin/env python
'''Provides an interface between the RepRap Franklin and a UNIX socket.

VirtualBox can be configured to use a UNIX socket as an interface to
the virtual machine's serial port, this class opens up that file
and communicates with the RepRap software running on the given machine.


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
import socket

class UNIXSocketInput( threading.Thread ):

    def __init__(self, reprap, source, delay=None):
        self.reprap = reprap
        self.source = source
        self.delay = delay

        threading.Thread.__init__(self)
        self.daemon = True


    def run(self):
        #try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.source)
        s.send("start\n")  #Supposedly needed (the RepRap wiki)

        buf = ""  #Buffer for commands.

        while 1:
            buf += s.recv(2048)

            if "\n" in buf:  #Break up commands.
                line, buf = buf.split("\n", 1)

                retcode = self.reprap.current_firmware.execute_gcode(line)

                s.send(retcode)

            if callable(self.delay):
                self.delay()
            else:
                time.sleep( float(self.delay) )



        #except Exception, exc:
        #    print("Exception: %s" % (exc))


        print("Done reading from file.")
