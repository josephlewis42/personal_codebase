#!/usr/bin/env python
'''
A simple AI mouse named Randall.

    Copyright (c) 2011 Joseph Lewis <joehms22@gmail.com>

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

from AI import *
from AI import world
from AI import body
from AI import limbic
from AI import maslow
from AI import mapper
from AI import logos

import time

class Randall( world.Actor ):
    '''Randall is an actor in a world, Actors have basic attributes and systems.
    '''

    def setup_organs(self):
        self.my_body = body.Body()

        #Hunger is a good thing...
        def hunger_update(old):
            return old + 2

        stomach = body.Organ("stomach", hunger_update, self.response_network)
        self.my_body.append(stomach)

        #Thirst!
        def thirst_update(old):
            return old + 2

        thirst = body.Organ("thirst", thirst_update, self.response_network)
        self.my_body.append(thirst)

        #What goes in must come out.
        def bladder_update(old):
            old_value = self.my_body["stomach"].last_value
            new_value = self.my_body["stomach"].value

            return old + ((new_value - old_value) / 2.0)

        bladder = body.Organ("bladder", bladder_update, self.response_network)
        self.my_body.append(bladder)

        #Sleep, deep sleep.
        def sleep(old):
            return old + .25

        s = body.Organ("sleep", sleep, self.response_network)
        self.my_body.append(s)


    def setup_emotions(self):
        self.emotions = limbic.generate_plutchik_limbic(self.response_network)
        #TODO fix emotions

    def setup_mind(self):
        mind = logos.Mind(self.needs, self, autostart=False)

        logos.quick_search_and_go(['food', 'water'], mind)

        self.mind = mind


    def setup_needs(self):
        needs = maslow.Heirarchy(maslow.PHYSIOLOGICAL, self.response_network)  #Basic needs with updown registers

        needs['food'].update_function = self.my_body["stomach"].get_value
        needs['water'].update_function = self.my_body["thirst"].get_value
        #needs['sleep'].update_function = self.my_body["sleep"].get_value
        #needs['excretion'].update_function = self.my_body["bladder"].get_value

        #Remove all without update function (reads: that we aren't using).
        needs.clean_needs()

        self.needs = needs

class map_functions:
    def food(self, actor):
        actor.my_body["stomach"].value = 0
        return "Stomach for %s set to 0" % (actor.name)

    def water(self, actor):
        actor.my_body["thirst"].value = 0
        return "Thirst for %s set to 0" % (actor.name)

    def lever(self, actor):  #Levers give food.
        actor.my_body["stomach"].value = 0
        return "Lever pressed: Stomach for %s set to 0" % (actor.name)

def newrandall():
    '''Makes a new randall and returns the world he lives in.'''
    import sys, os

    m = map_functions()

    mypath = os.path.abspath( __file__ )
    mydirpath = mypath[:mypath.rfind(os.sep)]

    #mygridpath = os.path.join(mydirpath, "AI","mazes","totem.map")
    mygridpath = os.path.join(mydirpath, "AI","mazes","pavlov.map")
    #mygridpath = os.path.join(mydirpath, "AI","mazes","617161.map")

    mygrid = mapper.make_from_mapfile(mygridpath)
    #mapper.map2HTML(mygridpath)

    m = mapper.interface_from_grid(mygrid, m)

    w = world.World(mygrid, m, move_time=1)

    #world.DEBUGGING = True
    r = Randall("Randall", w, 0,0)
    w.append(r)
    return w

if __name__ == "__main__":

    w = newrandall()
    try:
        print "Press Control + C to quit."
        while True:
            time.sleep(1)
            #j = m.fetch_news()
            #if j:
            #    print j
    except KeyboardInterrupt:
        w.kill()
