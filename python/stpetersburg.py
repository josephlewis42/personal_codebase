#!/usr/bin/python
'''stpetersburg.py -- A saint petersburg simulator.

2011/02/25 15:36:28

Copyright 2011 Joseph Lewis <joehms22@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


'''
import random

def play():
    total_won = 0
    payoff_matrix = {}

    print("Iter:\tFlips:\tWinnings:\tWon?")

    for i in range(iterations):
        winnings = 0
        flips = flip(max_game)  #Flip the coin until tails.

        #Determine winnings based upon the wager multiplier and flips.
        if flips:
            winnings = multiplier**(flips)

        #Stats
        total_won += winnings
        if flips in payoff_matrix.keys():
            payoff_matrix[flips] = payoff_matrix[flips] + 1
        else:
            payoff_matrix[flips] = 1

        print("%i\t%i\t%i\t\t%s" % (i, flips, winnings, winnings >= initial_wager))

    #Do some basic stats.
    avg_won = float(total_won) / iterations
    print ("Avg. Winnings:\t%d" % (avg_won))
    print ("Flips x Frequency")
    for k in payoff_matrix.keys():
        print("%s x %s" % (k, payoff_matrix[k]))
    print ("Money Won:   %s" % (total_won))
    print ("Money Waged: %s" % (iterations * initial_wager))


def flip(max_flip):
    '''Flips a coin until max_flip is reached or the coin turns up
    tails.  Returns the number of flips that came up heads.

    If max_flip is -1 flipping will continue until a tails is reached.
    '''
    numflips = 0

    while numflips != max_flip:
        numflips += 1
        if random.randint(0,1): #0 = heads 1 = Tails:
            return numflips


    return numflips


def ask_int(question, default):
    '''Asks the user for an int printing out the default and question.
    '''
    num = raw_input(question + " (Default: %s)\n" % (str(default)))
    if num == '':
        return default
    return int(num)


if __name__ == "__main__":
    print __doc__ #Notify the user of the license (top of file)

    #Set up simulation
    iterations = ask_int("How many iterations?", 100000)
    initial_wager = ask_int("What is the initial wager?", 2)
    multiplier = ask_int("What is the multiplier per win?", 2)
    max_game = ask_int("What is the bound on the number of games -1 for infinity?", -1)

    #Start simulation
    play()
