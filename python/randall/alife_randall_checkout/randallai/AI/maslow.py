#!/usr/bin/env python
'''
The maslow module provides a basic list of needs and the ability to
judge how well those needs are doing based off organs.

More Info: http://en.wikipedia.org/wiki/Maslow's_hierarchy_of_needs

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

__version__ = 1.0
__author__ = "Joseph Lewis <joehms22@gmail.com>"

DEBUGGING = False

PHYSIOLOGICAL = 0
SAFETY = 1
LOVE = 2
ESTEEM = 3
SELF_ACTUALIZATION = 4
OTHER = 5

PHYSIOLOGICAL_NEEDS = ['breathing', 'food', 'water', 'sex', 'sleep', \
                       'homeostasis', 'excretion']
SAFETY_NEEDS = ['body', 'employment', 'family', 'health', 'resources', \
                'morality', 'property']
LOVE_NEEDS = ['friendship', 'family', 'intimacy']
ESTEEM_NEEDS = ['self_esteem', 'confidence', 'achivement', \
                'respect_of_others', 'respect_by_others']
SELF_ACTUALIZATION_NEEDS = ['creativity', 'morality', 'spontaneity', \
                            'problem_solving', 'lack_prejudice', \
                            'fact_acceptance']

#The number of items to keep in a needs history used for extrapolating future needs.
NEED_HISTORY_LENGTH = 5


class Need:
    '''The need class represents a particular need for a creature.

    The higher the Need.value the more pressing it is.'''

    importance = None
    update_function = None
    name = None
    need_history = []  #The last NEED_HISTORY_LENGTH values for need, determines change
    value = 0

    def __init__(self, name, importance, update_function=None, updown=None):
        '''Initializes a Need.

        Paramaters:
        name -- The key used to represent this need in the Heirarchy.
                Usually a string.
        importance -- The importance of this need in the heirarchy,
                      0 being the lowest (PHYSIOLOGICAL variable) and
                      4 being the highest (SELF_ACTUALIZATION). (int)
        update_function -- The function called to update this need,
                           if none is provided the need will be ignored!
                           The function will be passed one variable, the
                           current value, if the function does not
                           accept this variable it will be called with
                           none.
                           The function should return a number between
                           0 and 100 anything higher or lower will be
                           changed to it's respective min/max (function)
                           Default: None

        updown -- An instance of pavlov.Response_Network, if not None
                  the conditions <needname>_up and <needname>_down
                  will be created, when the need value is raised
                  <needname>_up will be fired and the opposite for
                  lowering. (pavlov.ResponseNetwork) Default: None
        '''
        self.name = name
        self.importance = importance
        self.update_function = update_function

        #Do the updown setup.
        if updown != None:
            self.response_network = updown
            self.updown = True
            updown.register_con_res("%s_up"%(name))
            updown.register_con_res("%s_down"%(name))
        else:
            self.updown = False

    def __str__(self):
        '''Returns the name and value of this need as a string.'''
        return "%s:%i" % (self.name, self.value)

    def sortvalue(self):
        '''Creates a value to be used in sorting for importance.
        The lower the value the more pressing this need.  Needs with
        a lower importance will always come in before needs with
        a higher one, even if the need with the higher importance has
        a higher value.

        '''
        return (100 - self.value) + (self.importance * 100)

    def update(self):
        '''Updates the Need's value by calling the need's
        update_function.

        Returns the new value.

        '''
        if hasattr(self.update_function, '__call__'):
            #Try providing the current value.
            try:
                self.value = self.update_function(self.value)
            except TypeError:
                self.value = self.update_function()

            #Set the need history, but don't let it get too long.
            self.need_history.append(self.value)
            if len(self.need_history) > NEED_HISTORY_LENGTH:
                self.need_history = self.need_history[-NEED_HISTORY_LENGTH:]

            #Fix values
            if self.value > 100:
                self.value = 100
            elif self.value < 0:
                self.value = 0

            #Register raise and lowering of emotions.
            if self.updown and len(self.need_history) > 2:
                if self.need_history[-1] > self.need_history[-2]:
                    self.response_network.condition("%s_up"%self.name)
                elif self.need_history[-1] < self.need_history[-2]:
                    self.response_network.condition("%s_down"%self.name)

        if DEBUGGING:
            print(str(self))

        return self.value

    def _average_need_history(self):
        '''Returns the average slope of the need history.'''
        myslopes = []

        for i in range(len(self.need_history)-1):
            tmp = self.need_history[i+1] - self.need_history[i]  #Change in x, change in y is always 1
            myslopes.append(tmp)

        return sum(myslopes) / float(len(myslopes))

    def calls_to_max(self):
        '''Returns the (guessed) number of update calls until this
        Need hits 100.  Uses past data, the number of past points is
        defined by the NEED_HISTORY_LENGTH variable.

        Note: If need is going down the number of calls will be negative

        '''
        return (100 - self.value) / self._average_need_history()

    def calls_to_min(self):
        '''Returns the (guessed) number of update calls until this
        Need hits 0.  Uses past data, the number of past points is
        defined by the NEED_HISTORY_LENGTH varaible.

        Note: If need is rising the number of calls will be negative.

        '''
        return -self.value / self._average_need_history()

class Heirarchy:
    '''The Heirarchy class is used in determining needs.  Each need has
    a priority and an update function, when the Heirarchy class is
    polled for the highest need it updates itself, this can add time
    but reduces latency between need changes and resolution.  It also
    removes the overhead of having an extra thread running constantly.

    '''
    needs = []

    def __init__(self, level, updown_response_network=None):
        '''Creates a heirarchy with the level of needs corresponding to
        the given level.  The update functions for these needs must
        be set so they are considered when getting the most pressing
        need.

        If the level provided does not correspond to any need list then
        no default needs will be added.

        If updown_response_network is an instance of
        pavlov.ResponseNetwork then conditions will be registered on
        the raising and lowering of needs. DEFAULT: None

        Paramaters:
        level -- The level of needs to autogenerate (adds these needs
                 and all on lower levels). (int) Default: 1

        updown -- An instance of pavlov.Response_Network, if not None
                  the conditions <needname>_up and <needname>_down
                  will be created for each autogenerated need. When
                  the need value is raised <needname>_up will be fired
                  and the opposite for lowering.
                  (pavlov.ResponseNetwork) Default: None

        Example:
            >>> h = Heirarchy(maslow.PHYSIOLOGICAL)
            >>> h.needs
            ['breathing', 'food', 'water', 'sex' ... 'sleep']


        '''
        needs_list_list = []

        if level >= SELF_ACTUALIZATION:
            for n in SELF_ACTUALIZATION_NEEDS:
                self.needs.append( Need(n, SELF_ACTUALIZATION, updown=updown_response_network) )

        if level >= ESTEEM:
            for n in ESTEEM_NEEDS:
                self.needs.append( Need(n, ESTEEM, updown=updown_response_network) )

        if level >= LOVE:
            for n in LOVE_NEEDS:
                self.needs.append( Need(n, LOVE, updown=updown_response_network) )

        if level >= SAFETY:
            for n in SAFETY_NEEDS:
                self.needs.append( Need(n, SAFETY, updown=updown_response_network) )

        if level >= PHYSIOLOGICAL:
            for n in PHYSIOLOGICAL_NEEDS:
                self.needs.append( Need(n, PHYSIOLOGICAL, updown=updown_response_network) )

    def __getitem__(self, key):
        '''Emulates a list or dictionary, called with the name of the
        need, or an index.  Raises IndexError if not found.

        Example:
            >>> <Heirarchy>['food']
            <class Need at 0x0000007b>

            >>> <Heirarchy>[0]
            <class Need at 0x0000002a>

            >>> <Heirarchy>[None]
            IndexError

        '''
        #Check for strings
        try:
            for n in self.needs:
                if n.name == key:
                    return n
        except TypeError:
            pass

        #Check for indexes
        try:
            return self.needs[key]
        except TypeError:
            pass

        #else raise error
        raise IndexError


    def __len__(self):
        '''Returns the number of needs registered.'''
        return len(self.needs)

    def clean_needs(self):
        '''Removes needs from the need list that have no update_function
        This speeds up searches, updates, and clears memory.  Needs such
        as this may enter the needs list upon initialization.

        '''
        new_needs = []

        for n in self.needs:
            if hasattr(n.update_function, '__call__'):
                new_needs.append(n)

        self.needs = new_needs

    def update_needs(self):
        '''Updates the value of all needs by having each call its
        update_function.'''

        for n in self.needs:
            n.update()

    def most_urgent(self, threshold=80, update=True):
        '''Gets the most urgent need from the lowest possible need
        level that breaches the threshold.  Return None if there are
        no breaches.

        If the threshold is None, just return the Need with the highest
        value.

        Paramaters:
        threshold -- The number the need's value must be over to consider
                     returning the need. (int/None)
                     Default: 80
        update -- Should the needs be updated before calling? (boolean)
                  Default: True

        '''
        #Update needs if desired
        if update:
            self.update_needs()

        #If threshhold is none return need with highest value (last).
        if not threshold:
            return sorted(self.needs, key=lambda i:i.value)[-1]

        #Get all needs over threshold.
        over = []
        for n in self.needs:
            if n.value > threshold:
                over.append(n)

        #Sort so the most important is first
        try:
            return sorted(over, key=lambda i:i.sortvalue())[0]
        except IndexError:
            return None

if __name__ == "__main__":
    h = Heirarchy(LOVE)
    for n in h.needs:
        print n
    print h.most_urgent()

    #Test needs cleaning
    def friend():
        return 81
    def food():
        return 81
    h['friendship'].update_function = friend
    h['food'].update_function = food
    h.clean_needs()

    #Test urgency rating
    print h.most_urgent()
