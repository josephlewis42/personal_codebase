#       index.py
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

if not SESSION or 'login' not in SESSION.keys() or not SESSION['login']:
    self.redirect("login.py")
else:
    self.send_200()

    #Create a new world if needed.
    global world
    global shutdown_hook

    if not world:
        from randallai import Randall
        world = Randall.newrandall()

        #kill the world when the server is closing.
        def killworld():
            world.kill()
        shutdown_hook.append(killworld)

    SESSION['world'] = world

    page = '''
<!--
        index.py

        Copyright 2010 Joseph Lewis <joehms22@gmail.com>

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
-->

<html lang="en">
<head>
    <title>AI Webserver</title>
    <meta http-equiv="content-type" content="text/html;charset=utf-8" />
    <LINK REL=StyleSheet HREF="assets/login.css" TYPE="text/css"> </LINK>
    <script type="text/javascript" src="assets/jquery.js"></script>
    <script type="text/javascript" src="assets/md5.js"></script>
    <script type="text/javascript" src="assets/reloader.js"></script>
    <script type="text/javascript">
        function start()
        {
            $('#fg').show();
            $('.widget_container').hide();
            $('#fg').fadeOut(2000, function() {});
            $('.widget_container').fadeIn(2000, function() {});

            //Updates for the widgets.
            Update(10000, '#newswidget', 'stats.py?reload=true');
            Update(2000, '#emotionswidget', 'emotions.py?reload=true');
            Update(2000, '#needswidget', 'needs.py?reload=true');
            Update(2000, '#organswidget', 'organs.py?reload=true');
            Update(500, '#chatwidget', 'chat.py?reload=true');
            //Load the map once.
            $('#mapswidget').load('map.py?load=true');
            setInterval("$(\\"#commands\\").load(\\"map.py?update=true\\");show_mouse()", 1100);

            //Load the actor chooser widget once.
            $('#actorchooserwidget').load('actor_chooser.py?load=true');

        }

        var orig = "";
        var current = null;

        function show_mouse()
        {
            if(current != null)
            {
                $(current).html(orig);
            }

            current = $('#commands').html();

            orig = $(current).html();
            $(current).html("<span style='color:#640F9A'>&lt;:3)~</span>");
        }
      </script>
</head>

<body onLoad="start()" id="main_panel">
    <div id="fg"></div>
    <div class="large_widget_container">
        <div id="mapswidget" class="widget"></div>
        <br />
        <div id="newswidget" class="widget"></div>
        <div id='commands' style="display:none;"></div>
        <!--<div id="chatwidget" class="widget"></div>-->
        <iframe src="chat.py" width="100%"></iframe>
        <br />
    </div>
    <div class="small_widget_container">
        <div id="actorchooserwidget" class="widget"></div>
        <br />
        <div id="needswidget" class="widget"></div>
        <br />
        <div id="organswidget" class="widget"></div>
        <br />
        <div id="emotionswidget" class="widget"></div>
        <br />


    </div>
</body>
</html>
'''

    #Send body
    self.wfile.write(page)