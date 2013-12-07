"""
This application starts the webserver.
@Author  : Joseph Lewis <joehms22@gmail.com>
@Licence : Apache License
@Date    : Fri 12 Feb 2010 05:00:22 PM MST 
"""
#WX Stuff
import wx
from wx import xrc
#Config Parser, not needed in normal wx applications.
import ConfigParser
config = ConfigParser.RawConfigParser()

class ServerApp(wx.App):
    '''
    The server app creates a class that wx can use to interact with the items
    in the application.
    '''
    def OnInit(self):
        '''
        Called by wx to start the applet.
        '''
        #The location of the configuration file
        self.res = xrc.XmlResource("./Lib/configure_gui.xrc")
        #Init the frame and the items within
        self.InitFrame()
        #Init the buttons and bind them
        self.InitButtons()
        #Start up the sizer, and show the frame
        self.InitEverythingElse()
        return True
    
    def InitFrame(self):
        '''
        Sets the variables of the main frame, and the controls
        '''
        #Init frame
        self.frame = self.res.LoadFrame(None, "MainFrame")
        #Init the main panel
        self.panel = xrc.XRCCTRL(self.frame, "MainPanel")
        #Init Input Boxes
        self.portControl = xrc.XRCCTRL(self.panel, "port_ctrl")
        self.hostControl = xrc.XRCCTRL(self.panel, "host_ctrl")
        self.rootControl = xrc.XRCCTRL(self.panel, "root_ctrl")
        self.errorsControl = xrc.XRCCTRL(self.panel, "errors_ctrl")
        self.indexControl = xrc.XRCCTRL(self.panel, "index_ctrl")
        self._404Control = xrc.XRCCTRL(self.panel, "_404_ctrl")
        
    def InitButtons(self):
        '''
        Bind the user controllable items.
        '''
        self.frame.Bind(wx.EVT_BUTTON, self.StartServer, id=xrc.XRCID("StartServerButton"))

    def InitEverythingElse(self):
        '''
        Adds a sizer, and shows the panel
        '''
        sizer = self.panel.GetSizer()
        sizer.Fit(self.frame)
        sizer.SetSizeHints(self.frame)
        self.frame.Show()
    
    def StartServer(self, evt):
        '''
        Write the config file, then start the server.
        '''
        #Set Variables
        config.add_section('Pages')
        config.set('Pages', 'error_dir', self.errorsControl.GetValue())
        config.set('Pages', '_404', self._404Control.GetValue())
        config.set('Pages', 'siteroot', self.rootControl.GetValue())
        config.set('Pages', 'index', self.indexControl.GetValue())
        config.add_section('Server')
        config.set('Server', 'port', self.portControl.GetValue())
        config.set('Server', 'host_name', self.hostControl.GetValue())

        # Write the configuration file to 'configure.cfg'
        with open('./Configuration/configure.cfg', 'wb') as configfile:
            config.write(configfile)
        #Start the webserver in a new process (fork)
        import os
        pid = os.fork()
        if pid:
            import webserver
            webserver.main()
        else:
            #Start a browser for the user to see their work.
            import webbrowser
            webbrowser.open("http://"+ str(self.hostControl.GetValue())+":"+str(self.portControl.GetValue()))

def main():
    app = ServerApp(0)
    app.MainLoop()
if __name__ == '__main__':
    main()
