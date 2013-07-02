#!/usr/bin/env python
'''Provides a fullly implemented GCode parser for Franklin.

Commands can be passed in one at a time through the execute_gcode
function, returncodes will be returned.


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

import string

#Implements a full gcode parser.
class GCode:
    '''Takes a single line of GCode, and parses it in to its parts.

    ==All of the below types have a default None value.==
    cmd_type - The type of command, G,M,T
    checksum - The checksum of the command.
    checksum_pass - Whether or not the checksum is correct. (boolean)
    comment - The comment for the line of GCode
    cmd - The command i.e. G28
    line_number - The line number of the current command.
    S,P,X,Y,Z,I,J,F,R,Q,E,N - Optional arguments, values will be None
                              or int/float.

    '''
    cmd_type = None
    checksum = None
    checksum_pass = None
    comment = None
    cmd = None
    line_number = None
    #Paramaters.
    S = P = X = Y = Z = I = J = F = R = Q = E = N = G = M = T = None

    def grab_int(self, string):
        '''Grabs the paramater from a code as an int, if not possible
        returns None.

        '''
        try:
            return int(string[1:])
        except:
            return None

    def __init__(self, code):
        '''Creates a GCode object from a line of GCode.'''
        #Cut off comment.
        if ';' in code:
            code, self.comment = code.split(";", 2)

        #Cut off checksum.
        if '*' in code:
            code, cs = code.split("*", 2)
            self.checksum = int(cs)

            #Verify the checksum
            v = 0
            for c in code:
                v = v ^ ord(c)
            self.checksum_pass = (v == self.checksum)

        #Make sure this isn't an END statment
        if code.startswith("END"):
            return

        #Make sure all letters have spaces in front of them.
        for c in string.ascii_letters:
            code = code.replace(c, ' %s'%(c))

        #Split in to individual paramaters.
        cmds = code.split()

        for c in cmds:

            if c.startswith('N'):  #Line number command.
                n = self.grab_int(c)
                self.line_number = n
                self.N = n

            elif c[0] == 'G':
                self.G = self.grab_int(c)
                self.cmd_type = 'G'
                self.cmd = c

            elif c[0] == 'M':
                self.M = self.grab_int(c)
                self.cmd_type = 'M'
                self.cmd = c

            elif c[0] == 'T':
                self.T = self.grab_int(c)
                self.cmd_type = 'T'
                self.cmd = c

            else: #All other types are floats.
                try:
                    t = c[0]
                    val = float(c[1:])

                    exec("self.%s = %s" % (t, val))
                except ValueError as exc:  #Empty string causes, but how does that happen?
                    print("\n\nError while parsing %s: %s" % (c, exc))
                except SyntaxError, e:
                    print ("ERROR: SyntaxError %s" % (e))
                    print ("     : %s" % (c))
                    print ("     : %s" % (code))


class Coords:
    '''A representation of x,y,z and e coordinates for the RepRap'''
    x = 0
    y = 0
    z = 0
    e = 0

    def __init__(self, gc=None, co=None):
        '''Creates a new coordinate system with all zero coordinates,
        unless a paramater is passed.

        gc - An instance of GCode, X,Y,Z,E values are taken from here.

        '''
        if gc:
            self.setup(gc)

        if co:
            self.x = co.x
            self.y = co.y
            self.z = co.z
            self.e = co.e

    def copy(self):
        '''Returns a copy of the current coordinates.'''
        return Coords(co=self)

    def __str__(self):
        return "X:%s Y:%s Z:%s E:%s" % (self.x, self.y, self.z, self.e)

    def setup(self, gc):
        '''Sets the variables from a GCode instance.'''
        if gc.X:
            self.x = gc.X
        if gc.Y:
            self.y = gc.Y
        if gc.Z:
            self.z = gc.Z
        if gc.E:
            self.e = gc.E

    def offset(self, other):
        '''Offsets these coordinates from another, extrude value
        is copied.'''
        self.x += other.x
        self.y += other.y
        self.z += other.z
        self.e = other.e

    def in_to_mm(self):
        '''Multiplies all coordinates by 25.4, the number of mm in an
        inch.

        '''
        self.scale(25.4)  #Num of mm in an in

    def scale(self, factor):
        '''Scales all coordinates by factor, including e.'''
        self.x *= factor
        self.y *= factor
        self.z *= factor
        self.e *= factor

class Firmware (object):
    '''The firmware baseclass, all GCodes are implemented here as
    functions that take in a GCode class as their paramater.

    The function need not return any value, but if it does it needs
    to be a string, not newline terminated.  If nothing is returned
    an ok is sent back to the machine.

    '''
    title = ""

    origin = Coords()  #Origin of the machine.

    display = Coords()  #Center of display.
    display.x = 125  #Center of grid (mm)
    display.y = 125  #Center of grid (mm)

    last = Coords()  #The last location the toolhead was at.
    last.offset(origin) #Set current location to origin.

    line_number = 0  #The current line number.

    absolute = True  #Type of positioning Flase is Relative.

    units_mm = True  #Are the units in mm:True in:False
    STEPS_PER_MM = 2 #Number of steps per mm

    #Default debugging level for RepRap
    debug_echo = False
    debug_info = True
    debug_errors = True

    #Information about the RepRap Firmware
    #Extruder count will be generated at runtime and appended at the end.
    FIRMWARE_INFO = "PROTOCOL_VERSION:0.1 FIRMWARE_NAME:FiveD MACHINE_TYPE:Mendel"


    def __init__(self, reprap):
        '''Starts the firmware with the given reprap.'''
        self.reprap = reprap


    def debug(self, msg):
        '''Prints a debugging message.'''
        if self.debug_info:
            print ("DEBUG: %s" % (msg))

    def error(self, msg):
        '''Print an error message if errors is on.'''
        if self.debug_errors:
            print("ERROR: %s" % (msg))

    def warning(self, msg):
        '''Print a warning message.'''
        if self.debug_errors:
            print ("WARNING: %s" % (msg))


    def mm(self, value):
        '''If the current units are not mm, converts to mm.'''
        if not self.units_mm:
            return 25.4 * value


    def steps(self, value):
        '''Returns the number of steps that a distance comprises of.
        Any unit conversions are done here.
        '''
        return self.STEPS_PER_MM * self.mm(value)


    def G0(self, gc):
        co = self.last.copy()  #Start off with last values.
        co.setup(gc)  #Set up for the given values.

        if not self.units_mm:
            co.in_to_mm()

        #If we are offsetting from origin.
        if self.absolute:
            co.offset(self.origin)
        else:  #If we are offsetting from last position.
            co.offset(self.last)

        #Draw line from the last place to the current place, pass
        #duplicate coordinate systems though so the printbed
        #can scale without messing us up.
        dco = self.display.copy()
        dco.offset(co)
        dcl = self.display.copy()
        dcl.offset(self.last)
        self.reprap.move_toolhead(dco, dcl)

        #Set the current location to last.
        self.last = co

        if self.debug_echo:
            self.debug("G0/G1: Move to %s" % (self.last))
        pass

    G1 = G0  #The rep-rap firmware uses the same code for G0/G1


    def G28(self, gc):
        self.debug("G28: Move to origin.")
        if gc.X or gc.Y or gc.Z:
            if gc.X:
                self.last.x = self.origin.x
            if gc.Y:
                self.last.y = self.origin.y
            if gc.Z:
                self.last.z = self.origin.z

        else:
            self.last = self.origin.copy()


    def G4(self, gc):
        self.debug("G4: Dwelling")


    def G20(self, gc):  #Units to inches.
        self.debug("G20: Setting units to Inches")
        self.units_mm = False


    def G21(self, gc):  #Units to mm.
        self.debug("G21: Setting units to Milimeters")
        self.units_mm = True


    def G90(self, gc):
        self.debug("G90: Setting absolute positioning.")
        self.absolute = True


    def G91(self, gc):
        self.debug("G91: Setting relative positioning.")
        self.relative = True


    def G92(self, gc):
        #Must move before debug.
        self.origin.setup(gc)

        self.debug("G92: Setting new position: %s" % (self.origin))


    def M0(self, gc):
        self.debug("M0: Stop")
        self.reprap.stop = True


    def M84(self, gc):
        self.debug("M84: Stop idle hold.")
        self.reprap.idle_hold_on = False


    def M104(self, gc):
        self.debug("M104: Set temperature (fast) %s" % (gc.S))
        self.reprap.current_toolhead.temperature = int(gc.S)


    def M105(self, gc):
        self.debug("M104: Get extruder temperature.")

        tt = self.reprap.current_toolhead.temperature
        bt = self.reprap.bed.temperature

        return "ok T:%s B:%s" % (int(tt), int(bt))


    def M106(self, gc):
        self.debug("M106: Fan on.")
        self.reprap.fan = True


    def M107(self, gc):
        self.debug("M106: Fan off.")
        self.reprap.fan = False


    def M108(self, gc):
        self.debug("M108: Set extruder speed to %s." % (gc.S))
        self.error("M108: DEPRECATION WARNING: Use M113 instead.")
        if gc.S:
            self.reprap.current_toolhead.extrude_rate = gc.S


    def M109(self, gc):
        self.debug("M109: Set extruder temperature to %s." % (int(gc.S)))
        if gc.S:
            self.reprap.current_toolhead.temperature = int(gc.S)


    def M110(self, gc):
        self.debug("M110: Set current line number to %s." % (gc.N))

        if gc.N:
            self.line_number = int(gc.N)


    def M111(self, gc):
        self.debug("M111: Set debug level: %s" % (gc.S))
        if gc.S:
            self.debug_echo = int(gc.S) >> 0 & 1
            self.debug_errors = int(gc.S) >> 2 & 1
            self.debug_info = int(gc.S) >> 1 & 1

    def M112(self, gc):
        self.debug("M112: Emergency stop.")
        self.error("M112: Emergency stop.")
        self.reprap.stop = True

    def M113(self, gc):
        self.debug("M113: Set extruder PWM")
        self.reprap.current_toolhead.extrude_rate = 10
        if gc.S:
            self.reprap.current_toolhead.extrude_rate = int(gc.S * 10)

    def M114(self, gc):
        self.debug("M114: Get current position: %s." % (self.last))
        return "ok C: %s" % (self.last)


    def M115(self, gc):
        nt = len(self.reprap.possible_toolheads) #Number of toolheads
        output = "ok %s EXTRUDER_COUNT:%s" % (self.FIRMWARE_INFO, nt)

        self.debug("M115: Get firmware version and capabilities.")
        self.debug("    >> %s" % (output))

        return output

    def M116(self, gc):
        self.debug("M116: Wait.")


    def M117(self, gc):
        self.debug("M117: Get zero position.")
        return "ok C: X:0 Y:0 Z:0 E:0"

    def M126(self, gc):
        self.debug("M126: Open valve.")
        self.reprap.current_toolhead.open_valve()


    def M127(self, gc):
        self.debug("M126: Close valve.")
        self.reprap.current_toolhead.close_valve()


    def M140(self, gc):
        self.debug("M140: Set bed temperature to %s (fast)." % (int(gc.S)))
        if gc.S:
            self.reprap.bed.temperature = int(gc.S)


    def M141(self, gc):
        self.debug("M141: Set chamber temperature to %s (fast)." % (int(gc.S)))
        if gc.S:
            self.reprap.chamber.temperature = int(gc.S)


    def M142(self, gc):
        self.debug("M142: Set holding pressure to %s." % (int(gc.S)))
        if gc.S:
            self.reprap.bed.pressure = int(gc.S)


    def M226(self, gc):
        self.debug("M226: GCode initiated pause.")
        self.reprap.paused = True


    def M227(self, gc):
        self.debug("M227: Enable reverse and prime, does nothing.")


    def M228(self, gc):
        self.debug("M228: Disalbe auto reverse and prime, does nothing.")


    def M229(self, gc):
        self.debug("M229: Enable reverse and prime, does nothing.")


    def M230(self, gc):
        self.debug("M230: Disable/Enable wait for temp change, does nothing.")


    def T(self, gc):
        try:
            new_toolhead = self.reprap.possible_toolheads[gc.T]
            self.debug("T: Select tool #%s, %s" % (gc.T, new_toolhead.name))

            self.reprap.current_toolhead = new_toolhead

        except:
            self.error("T: ERROR: Couldn't select the given toolhead, does it exist?")


    def illegal_use_command(self, gc):
        '''Use this as a command replacement for any commands that
        aren't implemented in your hardware.

        EXAMPLE: If M111 isn't allowed in your firmware, do:
        >>> M111 = illegal_use_command
        >>> M111(gc)
        The command M111 is not legal for this firmware!
        >>>

        '''
        self.warning("The command %s is not legal for this firmware!" % gc.cmd)


    def execute_gcode(self, cmd):
        '''Executes a single gcode command (cmd).'''
        gc = GCode(cmd)  #Create a GCode representation of the cmd.

        #If the user wants echo debugging.
        if self.debug_echo:
            print(cmd)

        if gc.cmd_type == 'T':
            self.T(gc)

        elif gc.cmd != None:
            try:
                retcode = eval("self.%s(gc)" % (gc.cmd))

                if retcode != None:
                    return retcode + "\n"
            except AttributeError, e:
                print ("ERROR: %s is not a valid command." % (gc.cmd))
                print ("%s" % (e))

        return "ok\n"


class FullWare (Firmware):
    title = "Full Implementation"