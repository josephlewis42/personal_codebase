#!/usr/bin/env python
'''Provides NumberList and FrequencyDistribution, classes for statistics.

NumberList holds a sequence of numbers, and defines several statistical
operations (mean, stdev, etc.) FrequencyDistribution holds a mapping from
items (not necessarily numbers) to counts, and defines operations such as
Shannon entropy and frequency normalization.

Copyright 2011 Joseph Lewis <joehms22@gmail.com>

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

import ConfigParser
import os

__author__ = "Joseph Lewis"
__copyright__ = "Copyright 2011, Joseph Lewis"
__license__ = "GPL"
__version__ = ""

CONFIG_FILE = 'config_file.ini'

config = ConfigParser.ConfigParser()
#Creates and parses an ini file for the 
if os.path.exists(CONFIG_FILE):
    config.read(CONFIG_FILE) 
    
else:
    config.add_section('SMTP')
    config.add_section('POP')
    config.set('SMTP', 'username', 'someone@gmail.com')
    config.set('SMTP', 'password', 'P@$$w0Rd')
    config.set('SMTP', 'hostname', 'smtp.gmail.com')
    config.set('SMTP', 'port', '587')

    config.set('POP', 'username', 'someone@gmail.com')
    config.set('POP', 'password', 'P@$$w0Rd')
    config.set('POP', 'hostname', 'pop.gmail.com')
    config.set('POP', 'port', '995')
    config.set('POP', 'ssl', 'True')

    # Writing our configuration file to 'example.cfg'
    with open(CONFIG_FILE, 'wb') as configfile:
        config.write(configfile)
        
        

def setup_fetcher(email_fetcher):
    '''sets up an email fetcher from the given information in the ini.
    '''
    email_fetcher.configure_pop(   
                        config.get('POP', 'username'),
                        config.get('POP', 'password'),
                        config.get('POP', 'hostname'),
                        config.getint('POP', 'port'),
                        config.getboolean('POP', 'ssl')
                    )
    email_fetcher.configure_smtp(  
                        config.get('SMTP', 'username'),
                        config.get('SMTP', 'password'),
                        config.get('SMTP', 'hostname'),
                        config.getint('SMTP', 'port'),
                        )
    