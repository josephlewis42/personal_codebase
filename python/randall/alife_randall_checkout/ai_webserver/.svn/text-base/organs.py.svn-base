#       organs.py
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
else:
    if 'reload' in QUERY_DICT.keys():
        #Handle AJAX query.
        page = '''<h3>Organs:</h3><div id="progresscontainer">'''
        try:
            w = SESSION['world']
            a = SESSION['actor']
            for item in w[a].my_body:
                page += item.name + ":<br />"

                #Set colors for different values (so the humans can easily see)
                color = "#0D5995"
                if item.value >= 25 and item.value < 50:
                    color = "#00FF00"
                if item.value >= 50 and item.value < 75:
                    color = "#FFA500"
                if item.value >= 75:
                    color = "#A52A2A"

                page += '''<div class='progressbar'>
                               <div class='progressbartext'>%i%%</div>
                               <div class='progressbarinner' style='width:%i%%; background-color:%s;'></div>
                           </div>
                        ''' % (int(item.value), int(item.value),color)
            page += "<br /></div>"

            self.wfile.write(page)

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
        <body onLoad="javascript:Update(2000, 'body', 'organs.py?reload=true');" class="widget">
        Loading...
        </body>
        </html>
        '''
        self.wfile.write(page)
