#!/usr/bin/env python
'''
The logos module provides a kind of decision making process center.
It has hints of imagination and logic.

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

import threading
import time
import pavlov
import maslow
import copy

__version__ = 1.0
__author__ = "Joseph Lewis <joehms22@gmail.com>"

DEBUGGING = False


class Mode:
    '''An interface for building modes for the mind to operate in.
    Each mode has a specific Need that triggers it i.e. Hunger mode
    would be triggered by the Need "Hunger".  Modes are added to a
    Mind class.  When the Mind updates it checks for the most pressing
    Need, then triggers the mode with the same name as the need.  The
    mode then is called periodically by the brain until it sets its
    done value to True, the mind then moves to the next most pressing
    need.  If the done flag is not set to True this need will continue
    to execute until another one becomes more pressing.

    If however a more pressing need comes up, like a Basic Need, while
    a higher one is being fufilled the higher need will be destroyed
    in favor of the lesser one.

    The variables available to you are:
    done -- Is this Mode done executing?  Set to True to end.

    my_need -- An instance of the need that is associated with this
               mode.

    my_map -- An instance of the mapper.Grid that the Actor belonging
              to the Mind of this Need has.

    name -- The name of this mode, should be the same as a need, when
            the need with the same name arises this mode goes in to
            effect.
    '''

    done = False
    my_need = None
    my_map = None
    my_actor = None
    name = "Override with the same name as a need so the two are\
           associated"

    def __init__(self, need, my_map, my_actor):
        self.my_need = need
        self.my_map = my_map
        self.my_actor = my_actor

    def make_move(self):
        '''Override this function with one that will make a move for
        the Actor.'''
        raise NotImplementedError("make_move was not overriden for the mode: %s" % (self.name))

    def get_closest(self, itemlist, quick=False):
        '''Gets the path to the closest item in itemlist.  Returns
        none if none of the given items were in the known world.'''
        here = self.my_actor.view_terrain()

        closest = []

        for i in itemlist:
            j = self.my_map.find_closest(i, here, quick)

            if j != (None, None):
                closestdict.append(j)
        try:
            return closest.sort()[0]
        except IndexError:
            return None

def search_and_go_mode( mode_name ):
    '''Returns a simple mode class with the given mode_name that
    searches for an item and goes to it.'''
    class sag_mode( Mode ):
        path_to_resource = None
        done = False
        name = mode_name
        item = ""

        def make_move(self):
            #Get the path to item the first time.
            if self.path_to_resource == None:
                pr = self.my_actor.response_network.lookup_association(self.name)
                self.potential_resource = self.my_actor.world.item_event_interface.exists( pr )
                dist, closest, item = self.my_actor.internal_map.find_closest_list(self.potential_resource, self.my_actor.view_terrain())
                if closest:
                    self.item = item
                    self.path_to_resource = self.my_actor.internal_map.path_to(self.my_actor.view_terrain(), closest)
                else:
                    self.done = True
            else:
                if self.my_actor.can_move:
                    try:
                        mc = self.path_to_resource.pop(0)
                        self.my_actor.move_to_cell(mc)
                    except AssertionError, e:  #The path is obstructed, find a new one.
                        self.path_to_resource = None
                    except IndexError: #We are here, interact with the item that called this.
                        self.my_actor.interact(self.item)
                        self.done = True
    return sag_mode

def quick_search_and_go( mode_names, mind_instance ):
    '''Fills the given mind with search_and_go style modes for
    the given mode_names.  i.e. quick_search_and_go(['food','water'], <mindinstance>)
    would add basic food and water search capabilities to your mind.
    '''
    for item in mode_names:
        mind_instance.append( search_and_go_mode( item ) )

class ExploreMode( Mode ):
    items_here = []
    done = False  #Continue forever
    name = "explore"
    lastcell = None

    def __init__(self, need, my_map, my_actor):
        #Explore all items here first.
        self.items_here = copy.deepcopy(my_actor.view_terrain().items)
        Mode.__init__(self, need, my_map, my_actor)

    def make_move(self):
        c = None #The current cell.

        #If we have played with all the items here just move on.
        if not self.items_here:
            while self.my_actor.can_move:
                try:
                    thiscell = self.my_actor.view_terrain()
                    c = self.my_actor.world.terrain.random_accessible_neighbor(thiscell,self.lastcell)
                    self.my_actor.move_to_cell(c)
                    self.lastcell = thiscell
                except AssertionError:
                    continue  #The cell given was not accessible, try again.
                except RuntimeWarning:
                    pass  #The actor just moved.

                self.items_here = copy.deepcopy(c.items)
        else:
            while self.items_here:
                self.my_actor.interact(self.items_here.pop())


class Mind( threading.Thread ):
    '''The Mind reads information from the given maslow.Needs class,
    decides the most important thing to do and acts on it using its
    owner's body.

    '''

    _awake = True
    current_need = None

    modes = [ExploreMode]

    def __init__(self, needs, owner, update_time=0.1, autostart=True):
        '''Initializes the brain!

        Paramaters:
        needs -- An instance of maslow.Needs that the mind uses to
                 decide what mode to enter. (maslow.Needs)

        owner -- The instance of world.Actor whose mind this is, used
                 in moving around and such. (world.Actor)

        update_time -- The amount of time to wait between brain cycles
                       can be a function or float or int.  If it is a
                       function the function should either wait for a
                       certain amount of time then return 0 or return
                       the number of seconds to wait.
                       Default: 0.1 (Function, float, int)

        autostart -- Should the mind start as soon as it is
                     instanciated?  If not it will just sit there like
                     a cold dead organ until its thread is started
                     using the start() function.
                     Default: True (boolean)

        '''
        self.needs = needs
        self.owner = owner
        self.update_time = update_time

        threading.Thread.__init__(self)

        #Start the thread automagically if desired.
        if autostart:
           self.start()

    def append(self, item):
        '''Add a Mode to the Mind.'''
        self.modes.append(item)

    def __getitem__(self, key):
        '''Emulates a list or dictionary, called with the name of
        the Mode.  Raises IndexError if not found.'''
        #Check for ints
        if isinstance(key, int):
            return self.modes[key]

        #Check for strings and other ojbects
        for e in self.modes:
            if e.name == key:
                return e

        #else raise error
        raise IndexError("%s is not a valid Mode!" % (str(key)))

    def __len__(self):
        '''Returns the number of modes.'''
        return len(self.modes)


    def run(self):
        #Make sure awake is true before we start lest the developer
        #tries to sleep then re-wake the thread for some reason.
        self._awake = True

        while self._awake:
            #Handle update times for functions and numbers.
            if hasattr(self.update_time, '__call__'):
                ut = float( self.update_time() )
            else:
                ut = self.update_time

            #Wait so we don't hog the CPU. What are we coming to? A
            #world where AI doesn't rape your machine?
            time.sleep(ut)

            #Check for the current most pressing need.
            urgent = self.needs.most_urgent(40)

            if not urgent:
                urgent = maslow.Need("explore", maslow.OTHER)

            #If it is the same as the currently running one, go ahead.
            if self.current_need and urgent.name == self.current_need.name and not self.current_need.done:
                if DEBUGGING:
                    print("Calling make_move for %s" % (self.current_need.name))
                self.current_need.make_move()
            else:
                #Just make a new need and set it as current.

                #If the current need is the same as the last one, that probably means it couldn't be
                #reached, try exploring.
                if self.current_need and self.current_need.done and self.current_need.name == urgent.name:
                    urgent = maslow.Need("explore", maslow.OTHER)

                if DEBUGGING:
                    print("Creating new %s"%(urgent.name))

                self.current_need = self[urgent.name](urgent, self.owner.internal_map, self.owner)
                self.current_need.make_move()

    def sleep(self):
        '''Kills the thread.'''
        self._awake = False
