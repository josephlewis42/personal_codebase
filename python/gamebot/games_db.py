#!/usr/bin/env python
''' Provides a database for games

Copyright (c) 2011 Joseph Lewis <joehms22@gmail.com>

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

import sqlite3
import time
import re

conn = None  # Connection to the games db.
cursor = None  #The cursor for games

def setup():
    '''Sets up the games database (connects, etc.)'''
    global conn 
    global cursor
    conn = sqlite3.connect('games_db.sqlite')
    conn.row_factory = sqlite3.Row  #Produce dicts of data rather than tuples
    cursor = conn.cursor()

    #If the database isn't set up, create the new tables.
    try:
        #Is this database set up?
        cursor.execute("select * from Games")
    except sqlite3.OperationalError:
        '''
        ==Database Layout==
        TABLE: Games
                name        (name of the game)
                date        (date last accessed)
                file        (blob of this file)
        '''
        cursor.execute('''create table Games (name text, date numeric, file blob)''')

setup()

def cleanup(t):
    '''Removes games older than the given time (UNIX time).'''
    #Remove all deleted nodes
    cursor.execute("DELETE FROM Games WHERE date<?",(t,))
    # Clean up the database.
    cursor.execute("VACUUM")
    conn.commit()

def empty():
    '''Completely cleans the database.'''
    cleanup(time.time())

def __clean_name(name):
    return re.sub('[^a-z1-9]', '', name.lower().strip())
    
def add(name, blob):
    '''Adds a game to the database.'''
    b = sqlite3.Binary(blob) #Convert the input to a blob.
    
    #Clean up the name to be very simple (for easier searching)
    name = __clean_name(name)    
    
    cursor.execute("INSERT INTO Games (name, date, file) VALUES (?, ?, ?)", (name, int(time.time()), b))
    conn.commit()
    
    
def find(name):
    '''Finds the game with the given name, returns the binary if 
    possible, if not returns None.
    
    ''' 
    name = __clean_name(name)    
    
    cursor.execute("SELECT * FROM Games WHERE Name=?",(name,))
    
    row = cursor.fetchone()
    
    if row != None:
        return row['file']
    return None


def random_names():
    '''Returns a list of the names of 10 random games.'''
    
    cursor.execute("SELECT name FROM Games ORDER BY RANDOM() LIMIT 10")
    
    names = []
    
    for n in cursor.fetchall():
        names.append(n['name'])
    
    return names
