#       emotions.py
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
    #Handle AJAX query.
    if 'reload' in QUERY_DICT.keys():
        zero_emotions = ""

        page = '''<h3>Emotions:</h3> <div id="progresscontainer">'''
        try:
            w = SESSION['world']
            a = SESSION['actor']

            #Make bars for used emotions
            for item in w[a].emotions:

                iv = int(item.value)
                if iv > 0:
                    page += item.name + ":<br />"
                    page += '''<div class='progressbar'>
                                  <div class='progressbartext'>%i%%</div>
                                  <div class='progressbarinner' style='width:%i%%;'></div>
                               </div>'''%(iv, iv)

                else:
                    zero_emotions += "<li>%s</li>"%(item.name)

            #Alert the user for emotions not used.
            if zero_emotions != "":
                page += "<h4>Emotions Not Currently Felt:</h4><ul class='sidebyside'>%s</ul>"%(zero_emotions)
            page += "</div>"

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
        <body onLoad="javascript:Update(2000, 'emotions', 'emotions.py?reload=true');" class="widget">
        Loading...
        </body>
        </html>
        '''
        self.wfile.write(page)
