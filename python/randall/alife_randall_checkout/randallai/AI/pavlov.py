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


The pavlov module provides a condition response mechanism.

Events can be registered with pavlov, pavlov will then create
associations with events that are closely spaced.

NOTE:  This was the original class built for the project, and
is therefore the most primitive.  It has bad built-in constants,
messy comments, non-elegant code, etc. and could me made many times
better with a little work.

'''

import threading
import time
import sys

#Turn the variable DEBUGGING to True if you want to see debugging
#messages for this module.
DEBUGGING = False

__version__ = 1.1
__author__ = "Joseph Lewis <joehms22@gmail.com>"

ASSOCIATION_TO_EVENT = 1.0   #The amount of association neededed before one event triggers another
ASSOCIATION_PER_SECOND = 0.2  #The amount to raise association per second that is left in the amount of time since the last neuron call to this one.
DISASSOCIATION_PER_CALL = 0.05  #The amount of association to remove per disassoc call.
MAX_ASSOCIATION_TIME = 3.0  #The number of seconds until two events get no association added when they are fired.

class Neuron:
    _evt_a = None
    _evt_b = None

    _evt_a_time = 0
    _evt_b_time = 0

    assoc = 0.0

    def __init__(self, event_a, event_b):
        '''Create a new Neuron that "remembers" how often two events
        are registered in proximity to one another.

        Paramaters:
        event_a -- The first event.
        event_b -- The second event.

        WARNING: Do not use this class directly unless you are
        absoloutly sure you know what you are doing, it is better to
        instantiate a ResponseNetwork, which will build and manage
        Neurons for you.

        '''

        self._evt_a = event_a
        self._evt_b = event_b

        if DEBUGGING:
            print("Neuron created between %s, %s" % (event_a, event_b))


    def _evt_time_diff(self):
        '''The difference in the times each event was last called.
        Always positive.

        '''
        return abs(self._evt_a_time - self._evt_b_time)


    def _closeness_to_perfect(self):
        '''The measure of how close the events were to being in sync,
        closer events mean more related events.

        '''
        return (MAX_ASSOCIATION_TIME - self._evt_time_diff()) / MAX_ASSOCIATION_TIME


    def send_event(self, e):
        '''If the association is above the threshold return the event
        that was not put in as a paramater, else return None.
        '''
        if self.assoc >= ASSOCIATION_TO_EVENT:
            if DEBUGGING:
                print("Response between %s, %s " % (self._evt_a, self._evt_b))

            if e == self._evt_b:
                return self._evt_a
            return self._evt_b
        return None


    def register_event(self, e):
        '''If the event given is one of those that this Neuron registers
        and it is in a close enough proximity to the other event this
        Neuron registers, add association between the two relative to
        how close they are (closer = more association).  If the
        association is higher than the threshold return the event that
        was not called.

        Paramaters:
        e -- The event that might be in this Neuron that is needed to be
             updated.


        '''
        if e in (self._evt_a, self._evt_b):
            #Update time for appropriate event
            if e == self._evt_a:
                self._evt_a_time = time.time()
            else:
                self._evt_b_time = time.time()

            #If times close enough together add association.
            if self._evt_time_diff() < MAX_ASSOCIATION_TIME:
                self.assoc += self._closeness_to_perfect() * ASSOCIATION_PER_SECOND

                #Notify of updated association
                if DEBUGGING:
                    print("%s, %s Association: %.2f%%" % (self._evt_a, self._evt_b, self.percent_associated()))

        #If assoc high enough, return the event not yet sent.
        return self.send_event(e)


    def decrement_assoc(self, multiplier=1):
        '''Decrements the association, based off the DISASSOCIATION_PER_CALL
        variable.  The optional paramater multiplier can make up for
        _very_ large neural nets by multiplying the disassoc time.

        Paramaters:
        multiplier -- DEFAULT:1 Multiplies the disassoc call by a
                      this number. (int/float)

        '''
        self.assoc -= DISASSOCIATION_PER_CALL * multiplier

        if self.assoc < 0:
            self.assoc = 0

    def percent_associated(self):
        '''Returns the association of the two events as a percent,
        useful for user output, but should not be used anywhere else.
        (float)

        '''
        return (float(self.assoc)/float(ASSOCIATION_TO_EVENT)) * 100


class ResponseNetwork(threading.Thread):
    '''A rudimentary condition response "brain".  Conditions are
    registered, then the brain is started.  Any time the class is
    notified with a condition it judges the closeness of that condition
    with others, if they commonly occur together then an association is
    built.  When an association meets a supplied threshhold both events
    are triggered, in this fashion rudimentary behavior may be observed.


    WARNING:
    The response network is not meant to be shut down and turned back
    on at will, once off returning to an on state may cause bizarre
    crashes.  Instead use a function that halts updates for a variable
    amount of time.


    '''

    _neurons = []  #A list of created neurons.
    _cr = {}       #A dictionary of condition > response pairs.
    _awake = True  #Set to false to have the thread kill itself.


    def __init__(self, update_time=1, autostart=False):
        '''Sets up the response-network.

        Paramaters:
        update_time -- A function that returns a float as the number of
                       seconds until the organs update and fire events,
                       or just a float. DEFAULT: 1 (function, float)
        autostart -- Should pavlov bootstrap it's own thread (true) or are
                     you going to call start() manually (false)?  (bool)
                     Default: False
        Note:
        Why use a function for update_time?  Well, what if your device
        wanted to go to sleep but still retain all of it's conditions
        and responses?  What about suspending condition response
        memory loss while in a state of panic?  Maybe the charging
        station is a long way away for your robot, and you don't want it
        to forget while it is making the trip.


        '''
        self._update_time = update_time
        threading.Thread.__init__ ( self )

        if autostart:
            self.start()


    def __getitem__(self, key):
        '''Emulates a list or dictionary, called with a tuple of the
        emotion cross, or an index.  Raises IndexError if not found.

        Example:
            >>> ResponseNetwork[('one','two')]
            <class Neuron at 0x0000007b>

            >>> ResponseNetwork[0]
            <class Neuron at 0x0000002a>

            >>> ResponseNetwork[None]
            IndexError

        '''
        #Check for strings
        try:
            for n in self._neurons:
                if n._evt_a in key and n._evt_b in key:
                    return n
        except TypeError:
            pass

        #Check for indexes
        try:
            return self._neurons[key]
        except TypeError:
            pass

        #else raise error
        raise IndexError


    def __len__(self):
        '''Returns the number of neurons.'''
        return len(self._neurons)


    def register_con_res(self, condition, response=None):
        '''Registers a condition with a response.

        Paramaters:
        condition -- Any object, usually a string, used to identify
                     a condition. (any)
        response -- A function, or None.  The response will be run any
                    time the condition is created. DEFAULT:None
                    (__call__ or None)

        Note:
        If no response is created then a lambda is generated that
        performs the operation "1+1"; in very large systems this could
        be a problem with speed or memory storage.

        Warning:
        If the response does not have the __call__ attribute (is a
        function) then the default lambda is generated, no warning will
        be given.

        It is assumed you know what you are doing!

        '''

        #If thread alive, we must add them to the active list right now.
        if self.is_alive():
            for cond2 in self._cr.keys():
                self._neurons.append(Neuron(cond2, condition))

        #Add to the dictionary now.
        if hasattr(response, '__call__'):
            self._cr[condition] = response
        else:
            self._cr[condition] = (lambda : 1+1)


    def change_response(self, condition, response):
        '''Changes the response for a given condition that is allready
        registered.

        '''
        self._cr[condition] = response


    def _setup_net(self):
        '''Sets up the neural net with the current conditions and
        responses in the dictionary.

        '''
        self._neurons = []

        #Get a list of all the conditions
        tmp = self._cr.keys()

        #Add a neuron bridging all possible keys
        for i in range(0, len(tmp)):
            for j in range(i + 1, len(tmp)):
                self._neurons.append(Neuron(tmp[i], tmp[j]))

        if DEBUGGING:
            print('-' * 30)
            print("Total Neurons: %i" % (len(self._neurons)))


    def run(self):
        '''A pretty simple run method, decrements all of the
        associations in the neurons on a schedule.

        '''
        #Set up neurons
        self._setup_net()

        #Allow starting
        self._awake = True

        #Decrement from here on in until the network is killed.
        while self._awake:
            #Get the time until the next decrement.
            if hasattr(self._update_time, '__call__'):
                ut = float(self._update_time())
            else:
                ut = self._update_time

            time.sleep(ut)

            for n in self._neurons:
                n.decrement_assoc()

    def condition(self, c, autoappend=True):
        '''Sends a condition through the neural network creating
        responses and association between the neurons.

        Paramaters:
        c -- The condition to begin registering events from.
        autoappend -- If the condition is not known about yet, should
                      it be added to the neural net?  Yes makes the
                      creature more resiliant and able to learn, but
                      harder to debug. (boolean) Default: True

        '''
        if autoappend:
            if c not in self._cr.keys():
                self.register_con_res(c)

        #Holds conditions already fired so there are no infinite loops.
        done_conditions = set()
        fired = set()
        #Holds the conditions that have yet to be processed
        new_conditions = [c]

        if DEBUGGING:
           print("=" * 80)

        while new_conditions:
            c = new_conditions.pop()
            done_conditions.add(c)

            if DEBUGGING:
                print("Condition raised: %s" % (str(c)))

            for n in self._neurons:
                #Only fire neurons once
                if n not in fired:
                    resp = n.register_event(c)

                #Not null and not called before
                if resp and resp not in done_conditions:
                    if resp not in new_conditions:
                        new_conditions.append(resp)
                    fired.add(n)

        #Call all of the responses now.
        for c in done_conditions:
            r = self._cr[c]
            if hasattr(r, '__call__'):
                r()


    def lookup_association(self, c):
        '''Returns a list of all the things associated with the given
        condition.  A complete reverse-lookup.

        If a and b are associated, and b and c, and c and d, and c
        and f, then a reverse lookup for a would return [b,c,d,f].

        Note: This does not raise association between Neurons.

        Paramaters:
        c -- The condition to lookup events from.

        '''
        #Hold conditions already fired so there are no infinite loops.
        done_conditions = set()  #Conditions already checked.
        fired = set()            #Neurons already fired.
        #Holds the conditions that have yet to be processed, but have
        #been fired by a neuron.
        new_conditions = [c]

        if DEBUGGING:
           print("=" * 80)
           print("Reverse lookup on condition: %s" % (str(c)))

        while new_conditions:
            c = new_conditions.pop()
            done_conditions.add(c)

            if DEBUGGING:
                print("Condition checked: %s" % (str(c)))

            for n in self._neurons:
                #Only fire neurons once
                if n not in fired:
                    resp = n.send_event(c)

                #If the Neuron was fired, and the condition hasn't
                #allready been sent.
                if resp and resp not in done_conditions:
                    if resp not in new_conditions:
                        new_conditions.append(resp)
                    fired.add(n)

        return list(done_conditions)


    def get_neuron(self, evt1, evt2):
        '''Returns the Neuron that bridges the two events, returns None
        if the Neuron doesn't exist.

        '''
        try:
            return self.__getitem__((evt1, evt2))
        except IndexError:
            return None

    def get_association(self, evt1, evt2):
        '''Returns a tuple (association, assoc_to_event) for the Neuron
        bridging the given two events, Returns (None, None) if Neuron
        doesn't exist.

        '''
        n = self.get_neuron(evt1, evt2)

        if n != None:
            return (n.assoc, n.assoc_to_evt)

        return (None, None)


    def sleep(self):
        '''Kills the thread.'''
        self._awake = False


    def export_csv(self):
        '''Returns a string representation of a csv file.  This can be
        written to a file later.

        The columns and rows are the neuron names, and in the cells
        between are the percentages of association between the two.

        The csv is comma delimited and single quotes designate cell
        contents.

        Neurons that don't exist will be blank, neurons with 0
        association will be 0.0000.

        '''

        output = ""
        tmp = self._cr.keys()  #Get all the conditions now so it doesn't change.
        tmp.sort()

        #Get a list of every neuron and it's value for quick lookup
        #later on.
        neuron_snapshot = {}

        for n in self._neurons:
            neuron_snapshot[(n._evt_a, n._evt_b)] = n.percent_associated()


        #Write column header.
        output += "''," #Blank for first col (row headers).
        for k in tmp:
            output += "'%s'," % (str(k))
        output += "\n"

        #Write rows
        for i in tmp:
            #Row header
            output += "'%s'," % (i)

            #Row contents
            for j in tmp:

                #Try fetching the percent forward and backward, if not
                #found that means we are comparing a key to itself,
                #which has no value, for sanity purposes.
                try:
                    percent = neuron_snapshot[(i,j)]
                except:
                    try:
                        percent = neuron_snapshot[(j,i)]
                    except:
                        percent = ""

                output += "'%s'," % (str(percent))

            #End this line.
            output += "\n"

        return output

    def export_HTML_table(self, hidezeros=True):
        '''Returns a string representation of an HTML table.  This can
        be written to a file later.

        The columns and rows are the neuron names, and in the cells
        between are the percentages of association between the two.

        Neurons that don't exist will be blank.

        Paramaters:
        hidezeros - If the neuron is zero hide the value. (bool)
                    DEFAULT: True

        '''
        output = ""
        tmp = self._cr.keys()  #Get all the conditions now so it doesn't change.
        tmp.sort()

        #Get a list of every neuron and it's value for quick lookup
        #later on.
        neuron_snapshot = {}

        for n in self._neurons:
            neuron_snapshot[(n._evt_a, n._evt_b)] = n.percent_associated()


        #Write column header.
        output += "<table>\n<tr><th></th>" #Blank for first col (row headers).
        for k in tmp:
            output += "<th>%s</th>" % (str(k))
        output += "</tr>\n"

        #Write rows
        for i in tmp:
            #Row header
            output += "<tr><th>%s</th>" % (i)

            #Row contents
            for j in tmp:

                #Try fetching the percent forward and backward, if not
                #found that means we are comparing a key to itself,
                #which has no value, for sanity purposes.
                try:
                    percent = neuron_snapshot[(i,j)]
                except:
                    try:
                        percent = neuron_snapshot[(j,i)]
                    except:
                        percent = None

                if not percent or hidezeros and int(percent) == 0:
                    output += "<td></td>"
                else:
                    output += "<td>%.2f</td>" % (percent)

            #End this line.
            output += "</tr>\n"

        output += "</table>"
        return output

if __name__ == "__main__":

    DEBUGGING = True

    r = ResponseNetwork()
    r.register_con_res('a')
    r.register_con_res('b')
    r.register_con_res('c')
    r.register_con_res('d')

    r.start()
    time.sleep(1)
    print r[1]



    r.condition('a')
    r.condition('b')
    r.condition('a')
    r.condition('b')
    r.condition('a')
    r.condition('b')
    r.condition('a')
    r.condition('b')
    r.condition('a')
    r.condition('b')
    r.condition('a')
    time.sleep(5)
    r.condition('a')
    r.condition('c')
    r.condition('a')
    r.condition('c')
    r.condition('a')
    r.condition('c')
    r.condition('a')

    print r.lookup_association('a')
    r.sleep()