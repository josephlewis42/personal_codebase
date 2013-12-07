#!/usr/bin/env python
'''
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

class Organ():
    '''
    The organ class represents a bodily need in a creature, for example
    hunger, it's value is between 0 and 100 and updated using the
    update_function supplied.

    This class can trigger events when the value reaches certain levels.
    These levels must be added to the dictionary "events" with the key
    being the condition sent to the pavlov.ResponseNetwork class
    supplied and value being a tuple of size 2 .

    For example:
       "hello":(2,20)

    Would trigger the event "hello" when this particular emotion was
    between (and including) 2 and 20.

    Alternatively you could use the add_event function.

    WARNING:
    If you see warnings from this class something has gone horribly
    wrong, but it will continue to function, albeit probably wrongly.
    The creature may begin to act sporatically or even violently, or may
    even commit suicide.


    '''

    value = 0
    last_value = 0
    events = {}
    name = "Defined at init"

    def __init__(self, name, update_function, pavlovrn):
        ''' Initializes the Organ.

        Paramaters:
        name -- The name of the organ for identification and warning
                purposes. (String)
        update_function -- The function called when the organ needs
                           it's value updated, should return a number
                           between 0 and 100 inclusive. (Function)
        pavlovrn -- An implementation of the pavlov.ResponseNetwork class.
                    (pavlov.ResponseNetwork)

        Raises:
        TypeError "ERROR: Wrong type of pavlov.ResponseNetwork class", this
        happens if the pavlov.ResponseNetwork class is not an instance
        of pavlov.ResponseNetwork.


        '''

        self.name = name
        self.update_function = update_function
        if isinstance(pavlovrn, pavlov.ResponseNetwork):
            self.response_network = pavlovrn
        else:
            raise TypeError, "ERROR: Wrong type of pavlov.ResponseNetwork class"

    def update(self):
        '''Updates the value of this Organ by calling the update
        function.  If the value is less than 0 it will be made to be
        equal to 0 and if it is > 100 the value will be set to 100.
        '''
        try:
            #Try providing the current value.
            try:
                v = self.update_function(self.value)
            except TypeError:
                v = self.update_function()

            #Check for illegal values.
            if v < 0:
                v = 0
            if v > 100:
                v = 100

            self.last_value = self.value
            self.value = v
        except TypeError:
            print("ERROR: The update function for %s is not a function!" % (self.name))
            raise
        except ValueError:
            print("ERROR: The update function for %s didn't return a number." % (self.name))
            raise

        self.send_events()

    def send_events(self):
        '''Sends events for values set in the events dictionary by the
        user.

        This class can trigger events when the value reaches certain levels.
        These levels must be added to the dictionary "events" with the key
        being the condition sent to the pavlov.ResponseNetwork class
        supplied and value being a tuple of size 2 .

        For example:
           "hello":(2,20)

        Would trigger the event "hello" when this particular emotion was
        between (and including) 2 and 20.

        Alternatively you could use the add_event function.

        NOTE:
        This function is called periodically by the Body class, it
        does not need to be done manually unless desired.

        '''
        for cond in self.events.keys():
            low, high = self.events[cond]
            if self.value in range(low, high + 1):
                self.response_network.condition(cond)

    def add_event(self, low, high, event_name):
        '''A convenience function for adding events to the emotion.

        Paramaters:
        low -- The low number to trigger the event.
        high -- The high number to stop triggering the event at.
        event_name -- The event sent to the pavlov.ResponseNetwork class.


        '''
        self.events[event_name] = (low, high)

    def autogen_events(self, step=10, start=0, stop=101):
        '''
        Autogenerates events for ranges starting at start ending at stop
        every stop numbers and adds them to the response_network neuron
        list.  Returns a list of these events.

        Example:
        >>> autogen_events(10, 20, 50)
        ['name_20','name_30','name_40']

        Where name is the name of this emotion.

        Event name_20 would be triggered from 20-29, name_30 30-49 and
        name_40 from 40-49.

        '''
        new_events = range(start, stop, step)
        #Add the maximum so we can get to the stop.
        new_events.append(stop)

        newnames = []
        x = 0

        while x < len(new_events) - 1:
            #Generate the name of this event.
            e_name = "%s_%d" % (self.name, new_events[x])
            newnames.append(e_name)

            #Generate new neurons
            self.response_network.register_con_res(e_name)

            #Generate it locally, subtract from the high so there aren't
            #conflicts in ranges.
            self.add_event(new_events[x], new_events[x+1] - 1, e_name)

            x += 1

        return newnames

    def get_value(self):
        '''A getter that is used by any function that needs a dynamic way
        to get the value. (I'm looking at you maslow!)
        '''
        return self.value

class Body(threading.Thread):
    '''A simple container for organs.

    To add organs, just append them to the variable "organs".'''
    organs = []
    _update_time = None
    _awake = True  #True if thread is running, false to kill it.

    def __init__(self, update_time=1, begin=True):
        '''Sets up the body.

        Paramaters:
        update_time -- A function that returns a float as the number of
                       seconds until the organs update and fire events,
                       or just a float. | DEFAULT:1 | (function, float)

        begin -- Whether or not to start the thred as soon as done
                 initializing.  If false, the thread won't ever trigger
                 events or check for value correctness unless you
                 manually start it by calling start()
                 DEFAULT: True (boolean)

        '''

        self._update_time = update_time

        threading.Thread.__init__(self)

        if begin:
            self.start()

    def run(self):
        self._awake = True

        while self._awake:
            #Handle update times for functions and numbers.
            if hasattr(self._update_time, '__call__'):
                ut = float(self._update_time())
            else:
                ut = self._update_time

            #Wait so we don't hog the cpu
            time.sleep(ut)

            #Have all the organs fetch new values
            #and fire events to the pavlov network.
            for organ in self.organs:
                organ.update()

    def sleep(self):
        '''Kills the thread.'''
        self._awake = False


    def __len__(self):
        '''Returns the number of organs registered.'''
        return len(self.organs)


    def __getitem__(self, key):
        '''Emulates a list or dictionary, called with the name of the
        organ, or an index.  Raises IndexError if not found.

        Example:
            >>> <Body>['eyes']
            <class Organ at 0x0000007b>

            >>> <Body>[0]
            <class Organ at 0x0000002a>

            >>> <Body>[None]
            IndexError

        '''
        #Check for strings
        try:
            for n in self.organs:
                if n.name == key:
                    return n
        except TypeError:
            pass

        #Check for indexes
        try:
            return self.organs[key]
        except TypeError:
            pass

        #else raise error
        raise IndexError

    def append(self, o):
        '''Adds the given organ (o) to the body.'''
        self.organs.append(o)
