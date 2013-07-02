#!/usr/bin/env python
'''Provides an Extruder base class for the RepRap.

All extruders extend this class, and can therefore be chosen by the
user at runtime.

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

class Toolhead(object):
    color = "white"  #Color to print in
    name = ""  #Name of the extruder to show the user.
    width = 1  #Width of a line to print (1 is good for most purposes)

    #Actual attribues.
    extrude_rate = 0
    temperature = 22.22  #Room temp (celsius)
    valve_open = False

    def open_valve(self):
        self.valve_open = True

    def close_valve(self):
        self.valve_open = False