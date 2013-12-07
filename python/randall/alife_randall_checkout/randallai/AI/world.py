#!/usr/bin/env python
'''
The world provides a place for actors to interact.  All Actors should
have some basic variables (cheifly location and hunger), these can
be accessed by the organs so the animal can "sense" what is going on
around it.  Having the variables here also ensures that the Actors
don't know about them, and therefore nothing gets hard coded in to an
animal.

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

import mapper
import copy
import pavlov
import threading
import time

__version__ = 1.0
DEBUGGING = False

class Actor:
    '''A simple instance of an actor.'''
    image = None  #The location of the actor's image.
    world = None  #The world in which the actor lives.
    response_network = None  #The condition-response mechanism for this animal
    my_body = None  #The organ systems for this Actor
    emotions = None  #The emotion systems for this Actor
    internal_map = None  #The map this actor has of the world it lives in.
    needs = None  #The needs of this Actor, maslow.Heirarchy
    can_move = False  #Set to false when the actor moves, reset by
                      #the world.
    mind = None  #logos.Mind controler.

    _css_move_history = [] #Stores the css selectors of the past 100 moves.

    def __init__(self, name, world, x, y, z=0, seed=100):
        '''Initializes the actor.

        Arguments:
        seed - The seed to set the Actor's decision process to. Default: 100
        x - The x location of the Actor in the world. (int)
        y - The y location of the Actor in the world. (int)
        z - The z location of the Actor in the world. (int) Default: 0
        name - A string to be used as the Actor's name. (String)

        '''
        self.seed = seed
        self.name = name
        self.world = world
        self.x = x
        self.y = y
        self.z = z

        self.setup()

        self._css_move_history.append(self.view_terrain().css_id)

    def __str__(self):
        return "%s At:(%i,%i,%i)" % (self.name, self.x, self.y, self.z)

    def view_terrain(self):
        '''Acts as a kind of eyes for an actor, returns the cell in the world
        where the actor is located.'''

        #Never give the actor the original, they might learn to use it to break
        #or expand their matrix!
        #return copy.deepcopy(self.world.terrain.cell_at(self.x, self.y, self.z))
        return self.world.terrain.cell_at(self.x, self.y, self.z)

    def move_to_cell(self, cell):
        '''Move to the location at the given cell if possible.'''
        return self.move_to(cell.x, cell.y, cell.z)

    def move_to(self, x, y, z):
        '''Moves the actor to the given x, y, z if possible.

        Errors Raised:
        AssertionError -- The Cell at x,y,z is not accessable from the
                          current location.

        IndexError -- The cell at the supplied x,y,z is beyond the
                      edge of the world!

        RuntimeWarning -- The Actor has moved too recently and is
                          unable to do it again at this time.

        '''

        here = self.world.map_grid.cell_at(self.x, self.y, self.z)
        try:
            there = self.world.map_grid.cell_at(x,y,z)
        except IndexError:
            raise IndexError("The cell at %i,%i,%i is out of bounds." % (x,y,z))

        #Update the actor's current map.
        self.internal_map.update_or_add(here)

        #Are they touching, and accessable, and the actor can move
        #at this time?
        if self.world.map_grid.is_touching(here, there):
            if self.world.map_grid.is_accessable(here, there):
                if self.can_move:
                    self.x = x
                    self.y = y
                    self.z = z
                    self.can_move = False
                    if DEBUGGING:
                        print "%s moving to %s" % (self.name, str(there))
                    self._css_move_history.append(there.css_id)
                    if len(self._css_move_history) > 100:
                        self._css_move_history = self._css_move_history[-100:]
                    return
                else:
                    raise RuntimeWarning("The actor %s moved too recently." % (self.name))

        raise AssertionError("%s can't access cell %s from %s" % (self.name, str(there), str(here)))

    def move_north(self):
        '''Moves the actor north if possible.'''
        self.move_to(self.x, self.y-1, self.z)

    def move_south(self):
        '''Moves the actor south if possible.'''
        self.move_to(self.x, self.y+1, self.z)

    def move_west(self):
        '''Moves the actor west if possible.'''
        self.move_to(self.x-1, self.y, self.z)

    def move_east(self):
        '''Moves the actor east if possible.'''
        self.move_to(self.x+1, self.y, self.z)

    def move_up(self):
        '''Moves the actor up a floor if possible.'''
        self.move_to(self.x, self.y, self.z-1)

    def move_down(self):
        '''Moves the actor down a floor if possible.'''
        self.move_to(self.x, self.y, self.z+1)


    def setup_map(self):
        '''Override me if needed.  Sets up a blank mapper.Map with the same
        size as the world map, just filled with Nones.  This is the one the
        Actor uses in it's brain.

        Sets: internal_map'''
        self.internal_map = mapper.Grid(self.world.terrain._x,
                                        self.world.terrain._y,
                                        self.world.terrain._z,
                                        name="%s's internal map"%(self.name))

    def setup_pavlov(self):
        '''Override me if needed.  Sets up a blank pavlov.ResponseNetwork and
        stores it to the response_network variable. The response_network has
        been started.

        Sets: response_network

        '''
        self.response_network = pavlov.ResponseNetwork(autostart=True, update_time=5)

    def setup_organs(self):
        raise NotImplementedError, "You didn't override the setup_organs function."

    def setup_emotions(self):
        '''Set up your emotions by overriding this class.  At the end set
        self.emotions to an instance of limbic.Limbic.'''
        raise NotImplementedError, "You didn't override the setup_emotions function."

    def setup_mind(self):
        '''Set up the mind by overriding this class.  At the end set
        self.mind to an instance of logos.Mind'''
        raise NotImplementedError, "You didn't override the setup_mind function."

    def setup_needs(self):
        '''Sets up the needs system for this creature, the self.needs should be
        an instance of maslow.Heirarchy by the end of this method.'''
        raise NotImplementedError, "You didn't override the setup_needs function."


    def setup_special(self):
        '''Put anything here that you need called at the end of the setup.'''
        pass

    def setup_threads(self):
        '''Starts the threads on all of the classes, if they are allready
        started does nothing.'''
        if DEBUGGING:
            print ('Starting Actor "%s"' % (self.name))
        if not self.response_network.is_alive():
            if DEBUGGING:
                print " -> Response Network"
            self.response_network.start()

        if not self.my_body.is_alive():
            if DEBUGGING:
                print " -> Body"
            self.my_body.start()

        if not self.emotions.is_alive():
            if DEBUGGING:
                print " -> Emotions"
            self.emotions.start()

        if not self.mind.is_alive():
            if DEBUGGING:
                print " -> Mind"
            self.mind.start()

        if DEBUGGING:
            print "[Success]"

    def setup(self):
        '''Sets up the Actor's basic systems, this in turn calls the setup
        functions, after this is run all threads should be started.'''
        self.setup_pavlov()
        self.setup_map()
        self.setup_organs()
        self.setup_emotions()
        self.setup_needs()
        self.setup_mind()
        self.setup_special()
        self.setup_threads()

    def interact(self, item_name):
        '''Call with an item in the current cell to interact with it.'''
        self.world.item_event_interface.interact(self, item_name)

    def kill(self):
        '''Kills the actor and its respective threads.'''
        if DEBUGGING:
            print 'Killing Actor "%s"' % (self.name)
        if self.response_network.is_alive():
            if DEBUGGING:
                print " -> Response Network"
            self.response_network.sleep()

        if self.my_body.is_alive():
            if DEBUGGING:
                print " -> Body"
            self.my_body.sleep()

        if self.emotions.is_alive():
            if DEBUGGING:
                print " -> Emotions"
            self.emotions.sleep()

        if self.mind.is_alive():
            if DEBUGGING:
                print " -> Mind"
            self.mind.sleep()

        if DEBUGGING:
            print "[Success]"

    def fetch_move_history(self):
        '''Clears and returns the move history for this actor.'''
        a = self._css_move_history
        self._css_move_history = []
        return a

class World (threading.Thread):
    '''A simple 3d world for actors to reside in.'''
    actors = []
    terrain = "Depreciated, use map_grid instead"
    map_grid = None
    item_event_interface = None
    _awake = True


    def __init__(self, map_grid, item_event_interface, move_time=1, autostart=True):
        '''
        Creates the world from a mapfile and class containing
        instructions for that mapfile.

        Paramaters:
        map_grid --
        item_event_interface --
        move_time -- The amount of time to wait between Actor moves
                     can be a function or float or int.  If it is a
                     function the function should either wait for a
                     certain amount of time then return 0 or return
                     the number of seconds to wait.
                     Default: 0.1 (Function, float, int)

        autostart -- Should the World start as soon as it is
                     instanciated?  If not the Actors will not be able
                     to move until its thread is started using the
                     start() function.
                     Default: True (boolean)
        '''
        self.terrain = map_grid
        self.map_grid = map_grid
        self.item_event_interface = item_event_interface
        self.move_time = move_time

        threading.Thread.__init__(self)

        #Start the thread automagically if desired.
        if autostart:
           self.start()

    def __getitem__(self, key):
        '''Emulates a list or dictionary, called with the name of
        the actor.  Raises IndexError if not found.'''
        #Check for strings
        for e in self.actors:
            if e.name == key:
                return e

        #Check for ints
        return self.actors[key]

        #else raise error
        raise IndexError

    def __len__(self):
        '''Returns the number of actors.'''
        return len(self.actors)

    def keys(self):
        '''Returns a list of all the names of the actors.'''
        k = []

        for e in self.actors:
            k.append(e.name)

        return k

    def add_actor(self, actor):
        '''Depreciated, use World.append instead'''
        self.actors.apend(actor)

        raise DeprecationWarning("Use World.append instead of World.add_actor")

    def append(self, actor):
        '''Appends an actor to the list.'''
        self.actors.append(actor)

    def run(self):
        '''Waits for the amount of time specified by move_time then
        resets the Actor's can_move to True allowing their bodies
        to move again, that way they don't buzz around the world.'''
        #Make sure awake is true before we start lest the developer
        #tries to sleep then re-wake the thread for some reason.
        self._awake = True

        while self._awake:
            #Handle update times for functions and numbers.
            if hasattr(self.move_time, '__call__'):
                ut = float( self.move_time() )
            else:
                ut = self.move_time

            #Wait so we don't hog the CPU. What are we coming to? A
            #world where AI doesn't rape your machine?
            time.sleep(ut)

            for a in self.actors:
                a.can_move = True

    def sleep(self):
        self._awake = False

    def kill(self):
        '''Kills the world and all actors within.'''
        self._awake = False
        for a in self.actors:
            a.kill()
