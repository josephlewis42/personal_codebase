#!/usr/bin/env python
''' The mapper module is used to maintain a map of places.

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
import random
import copy

__version__ = 1.0
__author__ = "Joseph Lewis <joehms22@gmail.com>"
__license__ = "Copyright (c) 2010 Joseph Lewis <joehms22@gmail.com> all rights reserved."

DEBUGGING = False


def make_maze(seed=None, xsize=10, ysize=10, zsize=1):
    '''Returns a randomized grid (a maze).  A seed can be supplied to
    get the same maze each time.

    Paramaters:
    seed -- An int to seed the random number generator with.
    xsize -- The width of the maze to generate. (int) Default: 10
    ysize -- The height of the maze to generate. (int) Default: 10
    zsize -- The z of the maze to generate. (int) Default: 1

    '''
    if not seed:
        seed = int(random.random() * 1000000)
    random.seed(seed)

    #Make a graph and populate it with cells
    g = Grid(xsize, ysize, zsize, True, name="Random Seed:%s"%(str(seed)))

    #Gets the non visited neighbors of the given cell.
    def non_visited_neighbors(cell):
        nonvisited = []
        for n in g.neighbors(cell):
            if n.parent == None:
                nonvisited.append(n)

        return nonvisited

    #Recursively remove walls, without recursive calls due to overflows.
    current = g.cell_at(0,0,0)
    last = []

    last.append(current)
    while last:
        #If there are neighbors remove a wall and add to the stack.
        nvn = non_visited_neighbors(current)
        if nvn:
            next = random.choice(nvn)
            g.set_accessible(current, next, True)
            next.parent = current
            last.append(current)
            current = next
        else:  #If there are no neighbors pop the stack and try from there.
            current = last.pop()

    return g


def make_from_mapfile(mapfile_location):
    '''Re-creates a maze from a mapfile at the given filesystem path.
    '''
    f = open(mapfile_location)
    name = ""
    size = None

    #Read first line, this should say MAP version.
    line = f.readline()
    if "MAP" not in line:
        raise Exception, "Not a valid mapfile!"
        if eval(line.split(" ")[1]) > __version__:
            raise Exception("Map file too new!")

    #Fetch the name and size of the map.
    while line.startswith("#"):
        line = f.readline()
        if "Name" in line:
            name = line[line.index(' '):-1]  #-1 = Don't include newline

        if "Size" in line:
            size = line[line.index(' '):-1]  #-1 = Don't include newline
            size = eval(size) #Change to tuple

    #Make new map instance that fits the size of the given file.
    x, y, z = size
    newgrid = Grid(x, y, z, True, name)

    #Get all of the cells and populate the map.
    #A line is in the format: (x,y,z) nesw []
    f.seek(0)
    for line in f:
        if line.startswith("#"):  #Skip comments.
            continue
        a = line.split('\t')
        x, y, z = eval(a[0])
        d = a[1]
        items = eval(a[2])

        c = Cell(x,y,z, 'n' in d, 's' in d, 'e' in d, 'w' in d, \
                    'u' in d, 'd' in d)
        c.items = items

        newgrid.append(c)

    return newgrid

def map2HTML(mapfile_location):
    '''Generates an HTML version of the mapfile at the same location
    as the original.'''
    g = make_from_mapfile(mapfile_location)
    g.gen_HTML(file_path=mapfile_location+".html")

class Cell:
    '''A representation of a square of the map, has an x y and z axis
    to allow better representaiton of the map.  Each square can have
    extra variables attached to it such as temperature, humidity, etc.
    Map squares can also have objects attached to them, usually things
    identified by the senses that the Actor can interact with.  These
    can be stored in a list in the map square.


    Variables:
    north -- Can this cell access the one to the north? (boolean)
    south -- Can this cell access the one to the south? (boolean)
    east -- Can this cell access the one to the east? (boolean)
    west -- Can this cell access the one to the west? (boolean)
    up -- Can this cell access the one above? (boolean)
    down -- Can this cell access the one below? (boolean)
    x -- The x (E/W) location of this cell in the world. (int)
    y -- The y (N/S) location of this cell in the world. (int)
    z -- The z (U/D) location of this cell in the world. (int)
    items -- A list of items this cell holds that Actors can interact
             with.  (List of Strings)
    css_id -- A unique id for representing this Cell when it is placed
              in an HTML file. Format: x00,y00,z00 Where the zeros
              are replaced by the x,y, and z of the Cell. (String)


    Note:
    Just because this cell can access another doesn't mean the reverse
    is true.

    '''
    last_visit = 0.0  #The last time this cell was seen live.

    #For a* algorithm
    score = 0
    parent = None

    def __init__(self, x, y, z, north, south, east, west, up=False, down=False):
        '''Creates a new map square, with the x y and z location, as well as
        the movement variables.

        Paramaters:
        x -- The x location of this square (int)
        y -- The y location of this square (int)
        z -- The z location of this square (int)

        north -- Can this square access the north? (bool)
        south -- Can this square access the south? (bool)
        east -- Can this square access the east? (bool)
        west -- Can this square access the west? (bool)
        up -- Can this square access above? (bool)  Default: False
        down -- Can this square access below? (bool) Default: False

        '''
        self.x = x
        self.y = y
        self.z = z

        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.up = up
        self.down = down

        self.items = []
        self.css_id = "x%iy%iz%i" % (x, y, z)


    def __str__(self):
        return "(%i,%i,%i)" % (self.x, self.y, self.z)


    def is_north(self, other):
        '''Is this cell North of the one given? Return bool.'''
        return self.y < other.y


    def is_south(self, other):
        '''Is this cell South of the one given? Return bool.'''
        return self.y > other.y


    def is_east(self, other):
        '''Is this cell East of the one given? Return bool.'''
        return self.x > other.x


    def is_west(self, other):
        '''Is this cell West of the one given? Return bool.'''
        return self.x < other.x


    def is_up(self, other):
        '''Is this cell above the one given? Return bool.'''
        return self.z < other.z


    def is_down(self, other):
        '''Is this cell below the one given? Return bool.'''
        return self.z > other.z

    def is_same_location(self, other):
        '''Is this cell in the same location as the one given? (bool)
        '''
        return other.x == self.x and other.y == self.y and other.z == self.z

    def update(self, newer):
        '''Updates this cell's directions and item list based off the
        values of another (newer) version.
        Also updates the last_visit variable to the current time.

        Paramaters:
        newer -- An instance of a Cell whose direction and items
                 values are to be copied to this cell's.  (Cell)
        '''
        self.north = newer.north
        self.east = newer.east
        self.south = newer.south
        self.west = newer.west
        self.up = newer.up
        self.down = newer.down

        self.items = copy.copy(newer.items)

        self.last_visit = time.time()


class Grid:
    '''A container of Cells.

    North/South is y    Furthest north is 0
    East/West is x      Furthest West is 0
    Up/Down is z        Furthest up is 0

    Variables:
    grid -- A 3D array of Cells.
    _x -- The x size for the grid. (int)
    _y -- The y size for the grid. (int)
    _z -- The z size for the grid. (int)
    name -- A name for this grid. (String)

    '''

    def __init__(self, x, y, z=1, fill=False, name=""):
        '''Creates a new grid with the number of elements.  To concerve
        memory with potentially large grids they are not filled unless specified
        with the fill variable.

        Paramaters:
        x -- The number of x columns.  (int)
        y -- The number of y rows.  (int)
        z -- The number of z levels. (int)  Default: 1
        fill -- Should the grid be populated with cells? (bool)
                Default: False
        name -- The name of this map. (string) Default: ""

        '''
        if not isinstance(x, int) or not isinstance(y, int) or not isinstance(z, int):
            raise TypeError("Can't create grid from non int indexes.")

        self._x = x
        self._y = y
        self._z = z
        self.name = name

        #Create a new grid filled with Nones.
        self.grid = [[[None]*z for i in xrange(y)] for j in xrange(x)]

        if fill:
            for j in range(x):
                for k in range(y):
                    for l in range(z):
                        c = Cell(j, k, l, False, False, False, False)
                        self.append(c)

    class Iterator():
        '''A simple dirty iterator for mapper.'''
        def __init__(self, parent):
            self.mylist = []

            for j in range(parent._x):
                for k in range(parent._y):
                    for l in range(parent._z):
                        self.mylist.append( parent.cell_at(j, k, l) )
            self.mylist.reverse()
        def next(self):
            #Check for stop:
            if not self.mylist:
                raise StopIteration
            return self.mylist.pop()

    def __iter__(self):
        '''Allows Grid to be used in for loops.

        Example:
        >>> for cell in Grid:
        >>>    print cell

        '''
        return self.Iterator(self)


    def add_cell(self, cell):
        '''Adds a cell to the Grid.'''
        import warnings
        warnings.warn("Use Grid.append() instead of Grid.add_cell()", DeprecationWarning, stacklevel=2)
        self.append(cell)

    def append(self, cell):
        '''Adds a cell to the Grid container.'''
        self.grid[cell.x][cell.y][cell.z] = cell


    def cell_at(self, x, y, z=0):
        '''Returns the cell at the given location.  Returns none if
        the cell has not been generated yet.

        Throws:
        IndexError -- If indexes are negative or out of bounds.
        '''
        if x < 0 or y < 0 or z < 0:
            raise IndexError("List index negative.")
        return self.grid[x][y][z]


    def safe_cell_at(self, x, y, z=0):
        '''Returns the cell at the given location.  Returns none if the cell
        has not been generated yet or is out of bounds.

        '''
        try:
            return self.cell_at(x, y, z)
        except IndexError:
            return None


    def clear_parents(self):
        '''Removes all parents settings from the cells.'''
        for c in self:
            try:
                c.parent = None
            except AttributeError:
                pass


    def get_all_items(self):
        '''Returns a list of all the unique items in the Grid's Cells.'''
        itemlist = []
        for c in self:
            try:
                for i in c.items:
                    itemlist.append(i)
            except AttributeError:
                pass  #The cell must be None
        return list( set(itemlist) )  #Uniquify


    def find_closest_list(self, items_list, othercell, quick=False):
        '''Returns the closest Cell to the one given that has the
        of the given items from items_list in its item list.

        Paramaters:
        items_list -- A list of names of items to search for. (string)
        othercell -- The cell to judge distances from. (Cell)
        quick -- True to judge the distance quickly based on the cells
                 relative position, False to actually find a route to
                 each cell before returning the fastest.  False is
                 much more accurate, but much slower.
                 Default: False (boolean)

        Returns a tuple (distance to closest cell, closest cell,
        item at that cell).
        Returns (None, None, None) if no cell has the given item.

        '''
        eachitem = []

        self.clear_parents()

        for i in items_list:
            dist, cell  = self.find_closest(i, othercell, quick)

            if dist and cell:
                cell.parent = i
                eachitem.append((dist, cell))

        for j in sorted(eachitem):
            return (j[0], j[1], j[1].parent)

        return (None, None, None)


    def find_closest(self, itemname, othercell, quick=False):
        '''Returns the closest Cell to the one given that has the
        given item in its item list.

        Paramaters:
        itemname -- The name of the desired item. (string)
        othercell -- The cell to judge distances from. (Cell)
        quick -- True to judge the distance quickly based on the cells
                 relative position, False to actually find a route to
                 each cell before returning the fastest.  False is
                 much more accurate, but much slower.
                 Default: False (boolean)

        Returns a tuple (distance to closest cell, closest cell).
        Returns (None, None) if no cell has the given item.

        '''
        closest = None
        dist = None    #The distance to the closest

        for c in self:
            if not c:
                continue

            if itemname in c.items:
                if DEBUGGING:
                    print "%s is in %s" % (itemname, c)
                #Get the first one.
                if not closest:
                    closest = c
                    dist = self.heuristic(othercell, c)

                #Less computation
                if quick:
                    mydist = self.heuristic(othercell, c)
                    if mydist < dist:
                        closest = c
                        dist = mydist
                #More computation, but more accuracy
                else:
                    mydist = self.heuristic(othercell, c)
                    if mydist <= dist:
                        mydist = len(self.path_to(othercell, c)) - 1 #Subtract the starting position.
                        if mydist < dist:
                            closest = c
                            dist = mydist
        return (dist, closest)


    def find_closest_unexplored(self, here):
        '''Finds the closest cell with unexplored neighbors, returns
        as a tuple (distance, closest_cell).

        '''
        for c in self:
            if c and self.unvisited_neighbors(c):
                c.items.append("has_unexplored_neighbors")
                print c

        output = self.find_closest("has_unexplored_neighbors", here, True)

        #Remove unvisited status
        for c in self:
            try:
                c.items.remove("has_unexplored_neighbors")
            except:
                pass

        return output


    def heuristic(self, here, there):
            '''A heuristic estimate of distance between two nodes.

            Paramaters:
            here -- A cell or a tuple with x,y,z coordinates for a location.
            there -- A cell or a tuple with x,y,z coordinates for a location.

            Example:
            heuristic(Cell c, (2,2,8))

            '''
            if hasattr(here, "__module__"):
                h_x, h_y, h_z = here.x, here.y, here.z
            else:
                h_x, h_y, h_z = here  #Unpack the tuple

            if hasattr(there, "__module__"):
                t_x, t_y, t_z = there.x, there.y, there.z
            else:
                t_x, t_y, t_z = there

            x = abs(h_x - t_x)
            y = abs(h_y - t_y)
            z = abs(h_z - t_z)

            return x + y + z


    def path_to(self, here, there):
        '''Returns the path from the first cell to the second using the A*
        search algorighm.

        TODO: add support for terrain difficulty.

        '''
        self.clear_parents()

        open_set = set()
        closed_set = set()
        path = []

        def retrace_path(c):
            path = [c]
            while c.parent is not None:
                c = c.parent
                path.append(c)
            path.reverse()
            return path


        open_set.add(here)

        while open_set:
            #Get the node in openset having the lowest f_score value (stored as score in ini)
            current = sorted(open_set, key=lambda i:i.score)[0]

            #end if we have reached the end.
            if current == there:
                return retrace_path(current)

            #Move x from openset to closedset
            open_set.remove(current)
            closed_set.add(current)

            for y in self.accessible_neighbors(current):
                if y not in closed_set:
                    y.score = self.heuristic(y, there)

                    if y not in open_set:
                        open_set.add(y)
                    y.parent = current
        return []  #Failed


    def is_touching(self, cellone, celltwo):
        '''Returns True if both cells are touching (regardless of if
        they can access one another or not).  Cells in the same
        location are always touching.

        '''
        for n in self.neighbors(cellone):
            if celltwo.is_same_location(n):
                return True

        if cellone.is_same_location(celltwo):
            return True

        return False


    def is_accessable(self, cellone, celltwo):
        '''Returns True if celltwo is accessable from cellone, note
        that the reverse isn't always True.  Cells in the same
        location are always accessable to each other.'''
        for n in self.accessible_neighbors(cellone):
            if celltwo.is_same_location(n):
                return True

        if cellone.is_same_location(celltwo):
            return True

        return False

        '''if cellone.is_north(celltwo):
            return cellone.south
        if cellone.is_south(celltwo):
            return cellone.north
        if cellone.is_east(celltwo):
            return cellone.west
        if cellone.is_west(celltwo):
            return cellone.east
        if cellone.is_up(celltwo):
            return cellone.down
        #Cellone must be below celltwo
        return cellone.up'''


    def neighbors(self, cell):
        '''Returns a list of the neighbors for the cell supplied.

        If the neighbors haven't been added to the grid (None)
        they are ignored.

        Paramaters:
        cell -- The cell to return neighbors for.

        '''
        x = cell.x
        y = cell.y
        z = cell.z
        return self.neighbors_by_location(x,y,z)


    def neighbors_by_location(self, x, y, z):
        '''Returns a list of the neighbors for the coordinates
        supplied.

        If the neighbors haven't been added to the grid (None)
        they are ignored.

        Paramaters:
        x,y,z -- The coordinates for the cell to get neighbors from.

        '''
        n = []

        n.append(self.safe_cell_at(x-1, y, z))
        n.append(self.safe_cell_at(x+1, y, z))
        n.append(self.safe_cell_at(x, y+1, z))
        n.append(self.safe_cell_at(x, y-1, z))
        n.append(self.safe_cell_at(x, y, z-1))
        n.append(self.safe_cell_at(x, y, z+1))

        #Remove Nones so as not to mess up program
        #ValueError is thrown when no more exist.
        try:
            while True:
                n.remove(None)
        except ValueError:
            pass

        return n

    def unvisited_neighbors(self, cell):
        '''Returns the number of neighbors that are accessible but unvisited
        for the given cell.

        '''
        x = cell.x
        y = cell.y
        z = cell.z
        c = cell

        unvisited = []

        if c.north:
            try:
                unvisited.append(self.cell_at(x, y-1, z))
            except IndexError:
                pass

        if c.south:
            try:
                unvisited.append(self.cell_at(x, y+1, z))
            except IndexError:
                pass

        if c.east:
            try:
                unvisited.append(self.cell_at(x+1, y, z))
            except IndexError:
                pass

        if c.west:
            try:
                unvisited.append(self.cell_at(x-1, y, z))
            except IndexError:
                pass

        if c.up:
            try:
                unvisited.append(self.cell_at(x, y, z-1))
            except IndexError:
                pass

        if c.down:
            try:
                unvisited.append(self.cell_at(x, y, z+1))
            except IndexError:
                pass

        count = 0
        for u in unvisited:
            if not u:
                count += 1

        return count

    def accessible_neighbors(self, cell):
        '''Returns a list of the neighbors accessible from the cell at
        the given point.

        If the neighbors haven't been added to the grid (unexplored)
        they are ignored.

        Paramaters:
        cell -- The cell to get neighbors from

        '''
        x = cell.x
        y = cell.y
        z = cell.z
        c = cell

        accessible = []

        if c.north:
            accessible.append(self.safe_cell_at(x, y-1, z))
        if c.south:
            accessible.append(self.safe_cell_at(x, y+1, z))
        if c.east:
            accessible.append(self.safe_cell_at(x+1, y, z))
        if c.west:
            accessible.append(self.safe_cell_at(x-1, y, z))
        if c.up:
            accessible.append(self.safe_cell_at(x, y, z-1))
        if c.down:
            accessible.append(self.safe_cell_at(x, y, z+1))

        #Remove Nones so as not to mess up program
        #ValueError is thrown when no more exist.
        try:
            while True:
                accessible.remove(None)
        except ValueError:
            pass

        return accessible


    def random_accessible_neighbor(self, cell, notin=None):
        '''Returns a random accessible neighbor for the cell given.'''
        myn = self.accessible_neighbors(cell)
        random.shuffle(myn)

        if notin and myn[0].is_same_location(notin):
            try:
                return myn[1]
            except:
                pass
        return myn[0]

    def random_neighbor(self, cell, notin=None):
        '''Returns a random neighbor for the cell given.  If supplied
        the cell given at notin will not be chosen.'''
        myn = self.neighbors(cell)
        random.shuffle(myn)
        if notin and myn[0].is_same_location(notin):
            try:
                return myn[1]
            except:
                return myn[0]
        return myn[0]


    def set_accessible(self, cellone, celltwo, value=True):
        '''Sets the walls between two cells to value.  If the cells
        aren't neighbors do nothing.  The default value removes the
        walls between the two cells.

        Paramaters:
        cellone -- A Cell to add or remove a wall between.
        celltwo -- A Cell to add or remove a wall between.
        value -- True = Remove "walls" False = Add "walls"


        '''
        if celltwo in self.neighbors(cellone):
            if cellone.is_north(celltwo):
                cellone.south = value
                celltwo.north = value

            elif cellone.is_south(celltwo):
                cellone.north = value
                celltwo.south = value

            elif cellone.is_east(celltwo):
                cellone.west = value
                celltwo.east = value

            elif cellone.is_west(celltwo):
                cellone.east = value
                celltwo.west = value

            elif cellone.is_up(celltwo):
                cellone.down = value
                celltwo.up = value

            elif cellone.is_down(celltwo):
                cellone.up = value
                celltwo.down = value

    def gen_inner_HTML(self, z=0):
        '''Generates the grid for the gen_HTML function.'''
        table = ""

        #Set up the css and divs for all cells
        for j in range(self._y):
            for k in range(self._x):
                c = self.safe_cell_at(k, j, z)

                css_id = "x%iy%iz%i"%(k, j, z)

                if c == None:  #Not explored
                    inner = "?"
                    nesw = "unknown"

                else:
                    inner = ""
                    if c.up:
                        inner += "&uarr;"
                    if c.down:
                        inner += "&darr;"

                    if c.items != []:
                        for item in c.items:
                            inner += str(item)+"<br />"

                    nesw = ""  #class ids to apply
                    if not c.north:
                        nesw += "n "
                    if not c.east:
                        nesw += "e "
                    if not c.south:
                        nesw += "s "
                    if not c.west:
                        nesw += "w"

                table += "<div id='%s' class='%s'>%s</div>\n" % (css_id, nesw, inner)
        return table

    def table_width(self, size_of_cell):
        return size_of_cell * self._x

    def gen_HTML(self, z=0, commands="", file_path=None):
        '''Generates an HTML representation of the NESW directions
        for the given level.

        Paramaters:
        z -- The level to generate from.
        commands -- The cell IDs to be placed in the javascript
                    function. These correspond with cells.

        file_path -- The file to write the map to, overwrites if
                     existing. (string)

        '''
        table = self.gen_inner_HTML(z)

        page = '''
        <html><head>
        <script type="text/javascript">
        var orig = "";
        var current = null;
        var list = [];
        var i = 0;

        function play()
        {
            clearInterval();
            var all = document.getElementById('commands').value;
            list = all.split("\\n");
            i = 0;
            setInterval(next, 200);
        }

        function next()
        {
            if( current != null)
            {
                document.getElementById(current).innerHTML = orig;
            }
            current = list[i];

            orig = document.getElementById(current).innerHTML;
            document.getElementById(current).innerHTML = "<:3)~";
            i++;
            if( i >= list.length - 1)
            {
                clearInterval();
            }
        }
        </script>
        <style>
        div { width:28px; height:28px; text-align:center;
        border:1px solid #FFF; float:left; font-size:8pt; }
        #entire { width:%ipx; text-align:left; margin:0px; padding:0px; }
        .unknown { background-color:#999; font-size:28px;}
        .n { border-top:1px solid #000; }
        .s { border-bottom:1px solid #000; }
        .e { border-right:1px solid #000; }
        .w { border-left:1px solid #000; }
        </style></head>
        <body><h1>%s</h1><div id="entire">%s</div>
        <div width="100%%">
        <textarea cols="50" rows="4" id="commands">%s</textarea>
        <button type="button" onClick="javascript:play();">Play</button>
        </div></body></html>
        '''%(self.table_width(30), self.name, table, commands)

        #Write file if desired.
        if file_path:
            f = open(file_path, 'w')
            f.write(page)
            f.close()

        return page

    def update_or_add(self, cell):
        '''Updates the cell at the same location as the current cell if it
        exists, adds it otherwise.'''
        if self.cell_at(cell.x, cell.y, cell.z) != None:
            self.cell_at(cell.x, cell.y, cell.z).update(cell)
        else:
            self.append( cell )

    def gen_mapfile(self, file_path = None):
        '''Generates a mapfile for this specific map.  Returns it as a string.
        Optionally writes it to a file.

        Paramaters:
        file_path = The file to write the map to, overwrites if existing. (string)

        '''
        output = "#MAP %s Used by AI mapper class, %s\n" % (str(__version__), __license__)
        output += "#Generation Time UTC: %s\n" % (time.strftime("%Y-%m-%d %H.%M.%S"))
        output += "#Name: %s\n" % (self.name)
        output += "#Size: (%i,%i,%i)\n" % (self._x, self._y, self._z)

        for c in self:
            if not c: #If null, just get next
                continue

            representation = str(c) + "\t"

            if c.north:
                representation += "n"
            if c.east:
                representation += "e"
            if c.south:
                representation += "s"
            if c.west:
                representation += "w"
            if c.up:
                representation += "u"
            if c.down:
                representation += "d"

            representation += "\t" + str(c.items) + "\n"
            output += representation

        #Write file if desired.
        if file_path:
            f = open(file_path, 'w')
            f.write(output)
            f.close()

        return output


def interface_from_grid(grid, mynameclass):
    '''Generates an ItemEventInterface from the given Grid, grid.  All
    of the Grid's item names are sought after in the given class
    mynameclass.  For example if you had a Grid whose Cells had the
    following items: ['food', 'water', 'lever'] and passed an instance
    of the class c:

    class c:
        def food(self, actor):
            <--Insert code here-->
        def water(self, actor):
            <--Insert code here-->

    Then the items food and water would be mapped to the functions
    with the same name, the final item would throw an exception.

    Paramaters:
    grid -- An instance of Grid to take items from.
    mynameclass -- An instance of a class whose methods are the same
                   names as the items.
    '''
    func_names = set(dir(mynameclass))
    items = grid.get_all_items()

    iei = ItemEventInterface()

    for i in items:
        if i in func_names:
            func_i = eval('mnc.%s' % (i), {}, {'mnc':mynameclass})
            iei.register(i, func_i)
        else:
            raise KeyError("Can't map %s to a function!" % (i))

    return iei


class ItemEventInterface:
    '''Provides an interface for interacting with items on the map.
    Items get registered with their specific functions.'''

    _iei = {}
    news = []

    def name_to_action(self, string):
        '''Convert the name of an object to an interaction name.'''
        return string + "_interact"


    def register(self, item_name, event):
        '''Adds the item_name and event to the interface.

        Paramaters:
        item_name -- The name of the item as it is found in the items
                     list in Cells on a Grid. (string)
        event -- The function that is triggered when an Actor
                 interacts with the item.  Takes a single paramater,
                 the Actor that is interacting with the item.  Returns
                 a string about what happened (for logging/news
                 updates) or None. (function)
        '''
        #Change the name to action
        item_name = self.name_to_action(item_name)

        self._iei[item_name] = event


    def interact(self, actor, item_name):
        '''This function is called when an actor wishes to interact
        with an item on the map.  Also registers the action with the
        Actor's pavlov.ResponseNetwork, adding it if necessary.

        Paramaters:
        item_name -- The name of the item as it is found in the items
                     list in Cells on a Grid. (string)
        '''

        if DEBUGGING:
            print("Actor %s interacted with %s" % (actor.name, item_name))

        #Change the name to action
        item_name = self.name_to_action(item_name)

        #Register the action with the Actor's pavlov.
        actor.response_network.condition(item_name)

        #Run the event.
        self.news.append( self._iei[item_name](actor) )


    def fetch_news(self):
        '''Returns a list of strings of the news generated by the
        actor's interactions with their environment.

        '''
        n = self.news
        self.news = []
        return n


    def exists(self, i):
        '''Checks if an item actually exists. Return true/false.
        If i is a list, returns a list of the items that exist.

        '''
        #String
        if not hasattr(i, '__iter__'):
            #Change the name to action
            i = self.name_to_action(i)
            return i in self._iei.keys()

        #List
        new = []
        for j in i:
            if self.exists(j):
                new.append(j)
        return new

if __name__ == "__main__":
    g = make_maze(seed=617161, xsize=30, ysize=30)

    #g.gen_HTML(file_path="output_basic.html")

    g.grid[1][1][0].items = ['food']
    a,b = g.find_closest('food',g.cell_at(1,1))
    #print b
    #print g.heuristic(g.cell_at(1,1), g.cell_at(2,2))
    #x = g.find_closest_unexplored(g.cell_at(9,9))
    #print x[1]
    #cmds = ""
    #for x in g.path_to(g.cell_at(9,9), x[1]):
    #    cmds += ("%s\n"%(x.css_id))

    #g.gen_HTML(commands=cmds, file_path="output.html")

    #g.gen_mapfile('output.map')
