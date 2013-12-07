#!/usr/bin/env python


import os
import random


def write_pgm(filename, content, width):
    '''Writes a pgm image file from the given content, with width being
    given.  The contnet written is the value at the content at the position,
    if contnet was [1,0,1,0] and width was 2 the pixels would end up being
        10
        10
    1 being on and 0 being off (black and white).

    content can be any iteratable object.
    '''
    #Create folders if necessary
    if os.sep in filename:
        filepath = filename[:filename.rfind("/")]
        if not os.path.exists(filepath):
            os.makedirs(filepath)

    #Set up variables
    height = int(len(content) / width)
    j = 0
    line = ""

    #Open up the new file.
    with open(filename, 'w') as f:
        #File header based on pgm standard:
        f.write("P1\n%i %i\n" % (width, height))

        for i in content:
            if j < width:
                line += str(i) + " "
                j += 1
            else:
                f.write(line + "\n")
                line = ""
                j = 0

        #Append the last line.
        f.write(line)

def add_one(array):
    add = True
    for i in range(len(array)):
        if add:
            if array[i] == 1:
                array[i] = 0
            else:
                array[i] = 1
                add = False

def main_straight_through():
    a = [0]*100

    i = 0

    while a[99] != 1:
        add_one(a)
        i += 1
        print i
        write_pgm("%i/%i/%i.pgm"%(i/1000, i/100, i), a, 10)

def main_random(height=10, width=10, num_to_gen=10000):
    length = height * width
    num_so_far = 0

    try:
        while num_so_far < num_to_gen:
            my_rand = random.randint(0, 2**length)
            a = bin(my_rand)[2:]
            to_add = "0" * (length - len(a))  #Padding front with zeros.
            a = to_add + a
            write_pgm("randout_%s.pgm" % (hex(my_rand)[2:-1]), a, width)
            num_so_far += 1

    except KeyboardInterrupt:
        print("Control + C pressed.")
        print("Generated %i random images." % (i))

if __name__ == "__main__":
    a = raw_input("[R]andom or [S]equential Image Generation?")
    if a.lower() == 'r':
        h = input("Height in pixels? ")
        w = input("Width in pixels? ")
        n = input("How many random images do you want to generate? ")

        print("The images will be generated in the present working directory")
        print("Their respective ids will be the hex value of their binary represenation.")
        main_random(h,w,n)
    else:
        print("Generating sequential images, warning, this happens very fast.")
        print("Press Control + C to stop generation...")
        main_straight_through()