#!/usr/bin/env python
'''
The limbic module is responsible for maintaining emotions.

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

__version__ = 1.0
__author__ = "Joseph Lewis <joehms22@gmail.com>"


def generate_plutchik_limbic(response_network):
    '''Returns a basic Limbic emotion system, in which emotions are
    (somewhat) tied together.  The emotions that begin with a > are
    dependant upon the two next to it and will contain the average of
    those two values.

    Based off Plutchik's Wheel of Emotions
    http://www.storiedmind.com/wp-content/uploads/2009/09/Wheel-of-Emotions2-441x450.jpg

    joy
    > love
    trust
    > submission
    fear
    > awe
    surprise
    > disapproval
    sadness
    > remorse
    disgust
    > contempt
    anger
    > aggressiveness
    anticipation
    > optimism
    joy

    Paramaters:
    response_network -- An implementation of the pavlov.ResponseNetwork
                        class.  (pavlov.ResponseNetwork)
    '''
    def average_emotion(emotion_one, emotion_two):
        def average():
            return (emotion_one.value + emotion_two.value) / 2
        return average

    l = Limbic()

    #Primary emotions
    l.emotions.append( Emotion("joy", response_network) )
    l.emotions.append( Emotion("trust", response_network) )
    l.emotions.append( Emotion("fear", response_network) )
    l.emotions.append( Emotion("surprise", response_network) )
    l.emotions.append( Emotion("sadness", response_network) )
    l.emotions.append( Emotion("disgust", response_network) )
    l.emotions.append( Emotion("anger", response_network) )
    l.emotions.append( Emotion("anticipation", response_network) )

    #Secondary emotions
    tmp = average_emotion(l['joy'], l['trust'])
    l.emotions.append( Emotion("love", response_network, tmp) )

    tmp = average_emotion(l['trust'], l['fear'])
    l.emotions.append( Emotion("submission", response_network, tmp) )

    tmp = average_emotion(l['fear'], l['surprise'])
    l.emotions.append( Emotion("awe", response_network, tmp) )

    tmp = average_emotion(l['surprise'], l['sadness'])
    l.emotions.append( Emotion("disapproval", response_network, tmp) )

    tmp = average_emotion(l['sadness'], l['disgust'])
    l.emotions.append( Emotion("remorse", response_network, tmp) )

    tmp = average_emotion(l['disgust'], l['anger'])
    l.emotions.append( Emotion("contempt", response_network, tmp) )

    tmp = average_emotion(l['anger'], l['anticipation'])
    l.emotions.append( Emotion("aggressiveness", response_network, tmp) )

    tmp = average_emotion(l['anticipation'], l['joy'])
    l.emotions.append( Emotion("optimism", response_network, tmp) )

    return l

class Emotion():
    '''
    The emotion class represents an emotion in a creature, for example
    happiness, it's value is between 0 and 100 and is raised or lowered
    through calls.

    This class can trigger events when the value reaches certain levels.
    These levels must be added to the dictionary "events" with the key
    being the condition sent to the pavlov.ResponseNetwork class
    supplied and value being a tuple of size 2 .

    For example:
       "hello":(2,20)

    Would trigger the event "hello" when this particular emotion was
    between (and including) 2 and 20.

    Alternatively you could use the add_event function.


    '''
    updown = None
    last_value = 0
    value = 0
    events = {}
    name = "Defined at init"


    def __init__(self, name, response_network, update_function=None, updown=True):
        ''' Initializes the Emotion.

        Paramaters:
        name -- The name of the emotion for identification and warning
                purposes. (String)
        response_network -- An implementation of the pavlov.ResponseNetwork
                            class.  (pavlov.ResponseNetwork)
        update_function -- The function called when the emotion needs
                           it's value updated, should return a number
                           between 0 and 100 inclusive. The function
                           will be passed the current value if possible.
                           You don't need to supply this. DEFAULT:None
                           (Function)
        updown -- A boolean, if true the conditions <emotionname>_up
                  and <emotionname>_down will be created, when the
                  emotion value is raised <emotionname>_up will be fired
                  and the opposite for lowering. (boolean) Default: True

        Raises:
        TypeError "ERROR: Wrong type of pavlov.ResponseNetwork class", this
        happens if the pavlov.ResponseNetwork class is not an instance
        of pavlov.ResponseNetwork.


        '''

        self.name = name
        self.update_function = update_function

        if isinstance(response_network, pavlov.ResponseNetwork):
            self.response_network = response_network
        else:
            raise TypeError, "ERROR: Wrong type of pavlov.ResponseNetwork class"

        #Do the updown setup.
        if updown:
            response_network.register_con_res("%s_up"%name)
            response_network.register_con_res("%s_down"%name)
            self.updown = updown


    def add_event(self, low, high, event_name):
        '''A convenience function for adding events to the emotion.

        Paramaters:
        low -- The low number to trigger the event.
        high -- The high number to stop triggering the event at.
        event_name -- The event sent to the pavlov.ResponseNetwork class.


        '''
        self.events[event_name] = (low, high)

    def update(self):
        '''Updates the value if a function was given at init, after that
        sends events to the ResponseNetwork by calling send_events().

        Returns the updated value.

        '''
        self.last_value = self.value

        if hasattr(self.update_function, '__call__'):
            try:
                self.value = self.update_function(self.value)
            except TypeError:
                self.value = self.update_function()

        self.send_events()

        return self.value

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
        This function is called periodically by the Limbic class, it
        does not need to be done manually unless desired.

        NOTE:
        This function is used for ensuring the value is really between
        0 and 100, if less than or greater than the value will be set to
        0 or 100.

        '''
        global value
        if self.value < 0:
            self.value = 0
        if self.value > 100:
            self.value = 100

        #Register raise and lowering of emotions.
        if self.updown:
            if self.value > self.last_value:
                self.response_network.condition("%s_up"%self.name)
            elif self.value < self.last_value:
                self.response_network.condition("%s_down"%self.name)

        #Register percentages.
        for cond in self.events.keys():
            low, high = self.events[cond]
            if self.value in range(low, high + 1):
                self.response_network.condition(cond)

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

class Limbic(threading.Thread):
    '''A simple container for Emotions.

    To add emotions, just append them to the variable "emotions".

    The Limbic class can get emotions just like a dictionary:
    <Limbic>[emotionname] will return the emotion whose name is that
    supplied.

    '''
    emotions = []
    _update_time = None
    _awake = True  #True if thread is running, false to kill it.

    def __init__(self, update_time=1, begin=True):
        '''Sets up the emotional system.

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
        threading.Thread.__init__ ( self )

        if begin:
            self.start()

    def __getitem__(self, key):
        '''Emulates a list or dictionary, called with the name of
        the emotion.  Raises IndexError if not found.'''
        #Check for strings
        for e in self.emotions:
            if e.name == key:
                return e

        #Check for ints
        return self.emotions[key]

        #else raise error
        raise IndexError

    def __len__(self):
        '''Returns the number of emotions.'''
        return len(self.emotions)

    def keys(self):
        '''Returns a list of all the names of the emotions.'''
        k = []

        for e in self.emotions:
            k.append(e.name)

        return k

    def run(self):
        while self._awake:
            #Handle update times for functions and numbers.
            if hasattr(self._update_time, '__call__'):
                ut = float(self._update_time())
            else:
                ut = self._update_time

            #Wait so we don't hog the cpu
            time.sleep(ut)

            #Have all the emotions fire events to the pavlov network.
            for emotion in self.emotions:
                emotion.update()

    def sleep(self):
        '''Kills the thread.'''
        self._awake = False


if __name__ == "__main__":
    def myresponse():
        print "I am happy"

    def loveup():
        print "Love raised"

    rn = pavlov.ResponseNetwork()
    rn.start()
    rn.register_con_res('happy80', myresponse)

    l = generate_plutchik_limbic(rn)
    l['joy'].add_event(80, 70, "happy80")
    rn.change_response('love_up', loveup)

    l['joy'].value = 100
    l['trust'].value = 80

    time.sleep(2)

    print l['love'].value
    l.sleep()
