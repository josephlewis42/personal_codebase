#!/usr/bin/python
import wx.html as html
import Parser
import wx
import Graph

class events():
    '''
    This class holds all of the events for the main gui and their helper methods.
    '''
    
    def submit_function(self, event):
        index = self.functions_list_box.GetSelection()
        fx = Graph.function(self.function_text_ctrl.GetValue(),
                             self.function_name_text_ctrl.GetValue())
        fx.will_graph = self.function_show_checkbox.GetValue()
        fx.line_color = self.function_color_combo_box.GetValue()
        fx.line_style = self.function_style_combo_box.GetValue()
                
        #Set the function
        Graph.function_list[index] = fx
        #Update the box
        self.setup_functions_list()
        event.Skip()

    def update_function_editor(self, event):
        #Get selected f(x) location
        index = event.GetSelection()
        #Get the correct function from the tupple
        fx = Graph.function_list[index]
        #Set all values
        self.function_text_ctrl.SetValue(fx.function_value)
        self.function_color_combo_box.SetValue(fx.line_color)
        self.function_style_combo_box.SetValue(fx.line_style)
        self.function_name_text_ctrl.SetValue(fx.function_name)
        self.function_show_checkbox.SetValue(fx.will_graph)
        event.Skip()

    def LoadPage(self, event): # wxGlade: CalcWidget.<event_handler>
        print "Event handler `LoadPage' not implemented"
        event.Skip()

    def input_key_press(self, event):
        '''
        Checks for the enter key, if it has been pressed then the program will
        submit the value that is in the pad input box
        '''
        keycode = event.GetKeyCode()
        #If user pressed enter or return spawn the submit input event
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            self.Submit_Input(event)
        event.Skip()

    def show_tab(self, event): # wxGlade: CalcWidget.<event_handler>
        print "Event handler `show_tab' not implemented!"
        event.Skip()
        

    def clear_pad(self, event): # wxGlade: CalcWidget.<event_handler>
        self.output_text_ctrl.Clear()
        event.Skip()
        

    def save_graph_as(self, event): # wxGlade: CalcWidget.<event_handler>
        print "Event handler `save_graph_as' not implemented!"
        event.Skip()

    def Submit_Input(self, event):
        '''
        Parse the input for the pads
        '''
        if self.input_text_ctrl.GetValue() != "":
            #Parse the data
            self.output_text_ctrl.AppendText("==" + self.input_text_ctrl.GetValue() + "\n")
            self.output_text_ctrl.AppendText(str(Parser.parse(self.input_text_ctrl.GetValue()))+"\n")
            #If an error happens above the text will NOT be cleared, allowing the
            #user to correct their mistake easily.
            self.input_text_ctrl.Clear()
        event.Skip()

    def LoadPage(self, event):
        '''
        Load the main html page.
        '''
        self.html_window.LoadPage("./Lib/Function Lookup/index.html")

    def switch_to_pad(self, event):
        '''
        Switch to the pad tab
        '''
        self.notebook_manager.SetSelection(0)
        event.Skip()
    
    def write(self,text):
        #Used to print stdout to output control
        self.output_text_ctrl.AppendText(text+"\n")
    
    def switch_to_functions(self, event):
        '''
        Switch to the functions tab
        '''
        self.notebook_manager.SetSelection(1)
        event.Skip()

    def switch_to_graphs(self, event):
        '''
        Switch to the graphs tab
        '''
        self.notebook_manager.SetSelection(2)
        event.Skip()

    def toggle_fullscreen(self, event):
        '''
        Toggles the window being fullscreen.
        
        TODO : Test this function
        '''
        self.main_window.ShowFullScreen(True, style=wx.FULLSCREEN_ALL)
        
    
    def setup_functions_list(self):
        '''
        Add all of the functions as well as their text to the listbox
        '''
        #Clear Box
        self.functions_list_box.Clear()
        #Get all function titles
        titles = Graph.get_function_titles()
        #Add title to list
        for title in titles:
            self.functions_list_box.Append(title)

    def graph(self):
        '''
        Graphs the current functions and plots the user has entered.
        '''
        #Get x range for y to be calculated off of
        x = Graph.get_x_range(Graph.xmin,Graph.xmax,Graph.x_increment)
        
        #Get all functions to plot
        functions_to_plot = Graph.get_on_functions()
        
        for fx in functions_to_plot:
            fx.update_function(x)

        #Now set up and plot the functions
        fig = self.graph_2d_plot_panel.get_figure()
        axes = fig.gca()
                
        # clear the axes and replot everything
        axes.cla()
        
        for fx in functions_to_plot:
            axes.plot(fx.x_values, fx.y_values,fx.get_color()+fx.get_line_style(), linewidth=1.0, label=fx.function_name)
        #Set the limits for the graph TODO get this working
        #axes.set_xlim((-100,100))
        axes.set_ylim(-1,1)
    
    def on_resize_window(self, event):
        '''
        Changes the position of the window divider (help frame, and tabs) when
        the window is resized, being that the help window will take all the 
        space otherwise.
        '''
        frame_size = event.GetSize()
        self.main_window.SetSize(frame_size)
        width      = frame_size.GetWidth()
        self.main_window.SetSashPosition(width - 300, redraw=True)
        event.Skip()

    def notebook_page_changed(self, event): # wxGlade: CalcWidget.<event_handler>
        '''
        Called when the tabs change, if graphing tab, update graph
        '''        
        if self.notebook_manager.GetSelection() == 2:
            self.graph() #TODO try to speed this up
            
        event.Skip()
        
    def _do_bindings(self):
        '''
        Does all of the custom bindings left out by wxGlade when the project is 
        generated.
        '''
        #Bind the pad input control with the enter key
        self.input_text_ctrl.Bind(wx.EVT_KEY_DOWN, self.input_key_press)
        
        #Bind window resize with a recalculation of the divider placement
        wx.EVT_SIZE(self, self.on_resize_window)
        
    def setup(self):
        '''
        This function sets up the program in the proper way, and 
        inits all components.
        '''
        #Bind all of the extras
        self._do_bindings()
        #Load the main web page
        self.LoadPage("")
        
        #Disallow any of the panels from disappearing
        self.main_window.SetMinimumPaneSize(1)
        #Add functions to the listbox
        self.setup_functions_list()
        #self.graph()
