#!/usr/bin/env python

#Monty Hall Problem
#
# switch = True : change doors
# switch = False: don't change doors

import random
import time
starttime = time.time()

def choose_door_to_open(one, two):
    #If either of the doors is the one with the prize
    if one or two:
        if one:
            return 2
        else:
            return 1
    #If neither of the doors has a prize, return a random number
    else:
        return random.randint(1,2)


wins = 0
losses = 0
rounds = 1000000
switch = True

for i in range(1,rounds+1):
    #Set up doors

    door_one = False
    door_two = False
    door_three = False

    #Choose door that is to have

    door_with_prize = random.randint(1,3)

    if door_with_prize == 1:
        door_one = True
    if door_with_prize == 2:
        door_two = True
    if door_with_prize == 3:
        door_three = True

    #print "Doors:"
    #print "One: "+str(door_one)
    #print "Two: "+str(door_two)
    #print "Three: "+str(door_three)

    #Have the program randomly choose a start door
    chosen_door = random.randint(1,3)
    #print "Chosen door: "+str(chosen_door)

    #Have the program choose which door to open.
    if chosen_door == 1:
        opens = choose_door_to_open(door_two, door_three)
        if opens == 1:
            opens = 2
        else:
            opens = 3
    elif chosen_door == 2:
        opens = choose_door_to_open(door_one, door_three)
        if opens == 1:
            opens = 1
        else:
            opens = 3
    else:
        opens = choose_door_to_open(door_one, door_two)
        if opens == 1:
            opens = 1
        else:
            opens = 2

    #print "Door Opened: "+str(opens)

    #Have the program choose to switch or stay and report result.
    if switch:
        if opens == 1 and chosen_door == 2:
            chosen_door = 3
        elif opens == 1 and chosen_door == 3:
            chosen_door = 2
        elif opens == 2 and chosen_door == 1:
            chosen_door = 3
        elif opens == 2 and chosen_door == 3:
            chosen_door = 1
        elif opens == 3 and chosen_door == 1:
            chosen_door = 2
        elif opens == 3 and chosen_door == 2:
            chosen_door = 1
        #print "Change door to: "+str(chosen_door)
    #else:
        #print "Chosen door is same."

    if chosen_door == door_with_prize:
        #print "Win"
        wins = wins + 1
    else:
        #print "Lose"
        losses = losses + 1

    #print "===End of round: "+str(i)+" ==="

print "===RESULTS==="
print "Wins: "+str(wins)
print str((wins / (rounds * 1.0))*100)+"%"
print "Losses: "+str(losses)
print str((losses / (rounds * 1.0))*100)+"%"
print
#print time.time() - starttime

#raw_input("Press enter to exit...")
