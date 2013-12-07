#       map.py
#
#       Copyright 2011 Joseph Lewis <joehms22@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

self.send_200()

if not SESSION or 'login' not in SESSION.keys() or not SESSION['login']:
    self.wfile.write("You are not logged in...<script type='text/javascript'>window.location = 'login.py'</script>")

elif 'load' in QUERY_DICT.keys():
    #Handle AJAX queries.
    try:
        wor = SESSION['world']
        name = wor.map_grid.name.strip()
        width = wor.map_grid.table_width(30)
        content = wor.map_grid.gen_inner_HTML()

        page = '''<h3>World Map "%s"</h3>
                  <div class='mapcontainer' style='width:100%%; height:400px; overflow:scroll;'>
                      <div class='map' style='width:%ipx;'>
                      %s
                      </div>
                  </div>
               ''' % (name, width, content)

        self.wfile.write(page)

    except KeyError, e:
        self.wfile.write("Error: Couldn't find the key specified: %s" %(e))

    except Exception, e:
        self.wfile.write("Error: %s" %(e))

elif 'update' in QUERY_DICT.keys():
    #Give most recent location.
    try:
        w = SESSION['world']
        a = SESSION['actor']
        page = "#" + w[a]._css_move_history[-1]
        self.wfile.write(page)

    except IndexError:
        self.wfile.write("")

    except KeyError, e:
        self.wfile.write("Error: Couldn't find the key specified: %s" %(e))

    except Exception, e:
        self.wfile.write("Error: %s" %(e))

#Handle page query.
else:
    page = '''
    <html>
    <head>
        <script type="text/javascript" src="assets/jquery.js"></script>
        <script type="text/javascript" src="assets/reloader.js"></script>
        <link rel="StyleSheet" href="assets/login.css" type="text/css" />
    </head>
    <body onLoad="javascript:Update(2000, 'body', 'map.py?reload=true');" class="widget">
    Loading...
    </body>
    </html>
    '''
    self.wfile.write(page)