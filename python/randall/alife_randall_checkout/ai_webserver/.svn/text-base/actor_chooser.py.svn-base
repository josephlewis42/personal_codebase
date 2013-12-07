#       actor_chooser.py
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
    if 'actor' not in SESSION.keys():
        try:
            SESSION['actor'] = SESSION['world'].actors[0].name
        except IndexError:
            import warnings
            warnings.warn("Can't find the world OR an actor in it.")

    if POST_DICT and 'actor' in POST_DICT.keys():
        #Change actor on successful post.
        SESSION['actor'] = POST_DICT['actor']

    #Handle AJAX refresh query.
    if 'load' in QUERY_DICT.keys():
        page = '''
        <script type="text/javascript" src="assets/jquery.js"></script>
        <h3>Actor Panel:</h3> <div id="progresscontainer">
        <h4>Choose Actor:</h4>
        <form id="actorselect">
        <select name="actor" onchange="$.post('actor_chooser.py', $('#actorselect').serialize());">
        '''
        try:
            for item in SESSION['world'].actors:
                page += "<option>%s</option>"%(item.name)
        except KeyError:
            pass

        page += '''</select></form>'''
        #Generate the normal links for the actor.
        page += '''<hr>
                    <a href="actor_map.py" target="_blank">Map</a>
                    <a href="pavlov.py" target="_blank">Association</a>'''
        page += "</div>"

        self.wfile.write(page)

    #Handle page query.
    else:
        self.wfile.write('''
        <html>
        <head>
            <script type="text/javascript" src="assets/jquery.js"></script>
            <link rel="StyleSheet" href="assets/login.css" type="text/css" />
        </head>
        <body class="widget">
        </body>
        </html>
        ''')
