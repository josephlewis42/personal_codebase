#!/usr/bin/python
'''
Graph provides an interface to matplotlib, as well as classes defining graph
objects, and function objects

@Author = Joseph Lewis
@Date = 2010-03-12
@License = GPL
==Changelog==
2010-03-12 - Original Built by Joseph Lewis <joehms22@gmail.com>
2010-03-17 - Added functions to get the graph colors and style - JL
'''

#from pylib import *
import numpy
import Parser
import matplotlib.numerix as nx #Depreciated TODO fix
import matplotlib.patches #Fixes momentarily the Depreciation?

xmin = -10
xmax = 10
x_increment = 0.01
ymin = -10
ymax = 10
zmin = -10
zmax = 10

def get_x_range(lower,upper,by):
    '''
    Returns a range from lower, to upper, by incriment.
    '''
    return nx.arange(lower,upper,by)

class function():
    '''
    Defines a function object, this object holds a function to be plotted
    '''
    function_name = ""
    function_value = ""
    previous_fx_value = ""
    will_graph = False
    line_color = "Blue"
    line_style = "Solid Line"
    x_values = ()
    y_values = []
    
    def __init__(self, value, name):
        self.function_value = value
        self.function_name  = name
    
    def get_descriptor(self):
        '''
        Returns a string description of the plot
        '''
        desc = self.function_name + "    " +self.function_value
        
        if self.will_graph:
            desc = desc + "    " + "ON"
        else:
            desc = desc + "    " + "OFF"
        
        return desc
    
    def update_function(self, arr):
        '''
        Creates a set of Y values from the x values in the array only if the
        current set will not work for some reason
        '''
        if tuple(arr) != self.x_values or self.previous_fx_value != self.function_value:
            #Update the conditions that made this switch work so it wont again
            #if next time the f(x) is the same.
            self.x_values = tuple(arr)
            self.previous_fx_value = self.function_value
            self.y_values = []
            for x in arr:
                self.y_values.append(Parser.clean_parse(self.function_value, x))

    def get_color(self):
        '''
        Get the matplotlib equivilent of a color word that is input.
        '''
        color_values = { 
            
            "Blue": "b", 
            "Cyan": "c",
            "Green":"g",
            "Black":"k",
            "Magenta":"m",
            "Yellow": "y",
            "Red": "r",
            "White": "w",
         }
        return color_values.get(self.line_color, 'b') #Default = blue

    def get_line_style(self):
        '''
        Get the matplotlib equivilent of a style word that is input.
        '''
        line_values = {
            "Solid Line":'-',
            "Dashed Line":'--',
            "Dashed - Dot Line":"-.",
            "Dotted Line":":",
        }
        return line_values.get(self.line_style, '-') #Default = solid

def get_function_titles():
    '''
    Returns a list of function descriptors
    '''
    global function_list
    titles = []
    for fx in function_list:
        titles.append(fx.get_descriptor())
    return titles

def get_on_functions():
    '''
    Returns a list of lists, the first value is x, the next is y, the third is
    the title of the plot.
    '''
    on_functions = []
    for fx in function_list:
        if fx.will_graph:
            on_functions.append(fx)
    return on_functions

function_list = [function('sin(x)', 'Y1'), function('', 'Y2'), function('', 'Y3'),
            function('', 'Y4'),function('', 'Y5'),function('', 'Y6'),
            function('', 'Y7'),function('', 'Y8'),function('', 'Y9'),
            function('', 'Y0')] #The default functions

#Test
xmin = -180
xmax = 180
function_list[0].will_graph = True
