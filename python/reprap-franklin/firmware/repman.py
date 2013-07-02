#!/usr/bin/env python
'''An emulator for RepMan specific commands (not complete)

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

import full

__author__ = "Joseph Lewis"
__copyright__ = "Copyright 2011, Joseph Lewis"
__license__ = "GPL"
__version__ = "1.0"


class RepMan (full.Firmware):
    title = "RepMan"

    def M101(self, gc):
        self.debug("M101: Turn extruder 1 on forward.")
        if self.reprap.current_toolhead.extrude_rate == 0:
            self.reprap.current_toolhead.extrude_rate = 1

    def M103(self, gc):
        self.debug("M103: Turn all extruders off.")
        for th in self.reprap.possible_toolheads:
            th.extrude_rate = 0
