#!/usr/bin/env python
'''Provides a RepRap Object for the RepRap Franklin.

This is used as the abstract RepRap and has a set of toolheads, a
firmware, a printing bed and other small components, like fans.

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

import firmware
import toolheads


class _PrintBed:
    ''' A printing bed representation.

    TODO Add ability to turn on/off lines from certain toolheads.

    To start printing to a canvas just set the canvas variable to a
    Tk.Canvas instance.
    '''

    lines = []  #All of the lines on the canvas.
    layer = []  #The current z layer's lines.
    layer_z = 0.0  #The z value of the current layer.
    canvas = None  #The canvas for the printer.

    #Physical properties
    temperature = 22.22 #Room temp.
    pressure = 0  #Holding pressure in bar.
    #Dimensions (mm)
    dim_x = 250
    dim_y = 250
    dim_z = 125

    scale = 1.5  #This many px = 1 mm, can't be below 1 for sanity.

    bed_width = None
    bed_height = None

    def __init__(self):
        #Setup scaling.
        self.bed_height = (self.dim_y + self.dim_z) * self.scale
        self.bed_width = (self.dim_x + self.dim_z) * self.scale
        self.max_y = self.dim_y * self.scale  #Max y value
        self.max_x = self.dim_x * self.scale  #Max x value

    def reset(self):
        #Clears the bed and re-draws the border lines.
        if self.canvas != None:

            y = self.dim_y * self.scale  #Max y value
            x = self.dim_x * self.scale  #Max x value

            #Horizontal Line
            self.canvas.create_line((0, y, self.bed_width, y), fill="black")

            #Vertical Line
            self.canvas.create_line((x, 0, x, self.bed_height), fill="black")

            #Denoting the areas.
            self.canvas.create_text(10, 10, text="XY")
            self.canvas.create_text(x+10, 10, text="YZ")
            self.canvas.create_text(10, y+10, text="XZ")
            self.canvas.create_text(x+45,y+10, text="Current Layer")

    def add_line(self, coord1, coord2, toolhead):

        #Scale the coordinates properly.
        coord1.scale(self.scale)
        coord2.scale(self.scale)

        self.lines.append((coord1, coord2, toolhead))

        x1 = coord1.x
        y1 = coord1.y
        z1 = coord1.z

        x2 = coord2.x
        y2 = coord2.y
        z2 = coord2.z

        #Immediately draw to the canvas.
        if self.canvas != None:
            #XY
            self.canvas.create_line((x1, y1, x2, y2), fill=toolhead.color, width=toolhead.width)
            #YZ
            self.canvas.create_line((self.bed_width-z1, y1, self.bed_width-z2, y2), fill=toolhead.color, width=toolhead.width)
            #XZ
            self.canvas.create_line((x1, self.bed_height-z1, x2, self.bed_height-z2), fill=toolhead.color, width=toolhead.width)

            #Draw lines for the current layer in the corner.
            if z2 != self.layer_z:  #If the z layer has moved, erase the corner.
                for line in self.layer:
                    self.canvas.delete(line)
                self.layer_z = z2
                self.layer = []


            x1 += self.max_x - (self.max_x / 4.0) #Cut 1/4 off all edges.
            x2 += self.max_x - (self.max_x / 4.0)
            y1 += self.max_y - (self.max_y / 4.0)
            y2 += self.max_y - (self.max_y / 4.0)

            j = self.canvas.create_line((x1,y1,x2,y2), fill=toolhead.color, width=toolhead.width)
            self.layer.append(j)


class Chamber:
    '''A chamber representation for the RepRap'''
    temperature = 22.22  #Room temp.

class RepRap:
    '''A reprap model, has a print bed, firmware and toolheads.'''

    #Physical properties.
    fan = False  #On = True
    stop = False
    idle_hold_on = True
    paused = False


    def __init__(self):
        '''Sets up the RepRap and some nice variables:
        current_firmware:   An initalized instance of a pice of firmware.
        bed:                The print bed.
        chamber:            The chamber for the device.

        possible_toolheads: The toolheads in each slot of the machine,
                            corresponds to the T number in GCode.
        current_toolhead:   A pointer to the currently used toolhead,
                            automatically 0.
        '''
        self.current_firmware = firmware.full.Firmware(self)
        self.bed = _PrintBed()
        self.chamber = Chamber()

        self.possible_toolheads = [toolheads.basic.BasicExtruder(),]
        self.current_toolhead = self.possible_toolheads[0]


    def change_toolhead(self, number):
        '''Changes to toolhead N if possible.'''
        try:
            self.current_toolhead = self.possible_toolheads[number]
        except Exception, e:
            print ("Couldn't change toolhead: %s" % e)


    def move_toolhead(self, c1, c2):
        '''Moves the toolhead from coordinates 1 to 2, drawing
        along the way if applicable.

        '''

        if self.current_toolhead.extrude_rate > 0:
            self.bed.add_line(c1, c2, self.current_toolhead)