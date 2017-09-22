'''
Created on 17 Aug 2011

@author: samgeen
'''

import EventHandler as Events
from KeyHandler import KeyHandler
from MouseHandler import MouseHandler

# Mouse data structure (all data public, no methods)
class MouseData(object):
    def __init__(self, button, state, scrx, scry):
        self.button = button
        self.state = state
        self.scrx = scrx
        self.scry = scry

# Main input class
class Input(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__mouseHandler = MouseHandler()
        self.__keyHandler = KeyHandler()
        # TODO: CONSIDER IGNORING EVENTS AND PASSING STRAIGHT TO KEYHANDLER/MOUSEHANDLER
        # TODO: MERGE KEY/MOUSE HANDLER INTO INPUTHANDLER?? BETTER CLASS NAME??
        self.__mouseHandler.RegisterEvents()
        self.__keyHandler.RegisterEvents()
    
    # Triggers when a key is depressed
    def OnKeyDown(self, key, x, y):
        data = MouseData(key, True, x, y)
        Events.FireEvent("KEYPRESS",data)
        
    # Triggers when a key is happy
    def OnKeyUp(self, key, x, y):
        data = MouseData(key, False, x, y)
        Events.FireEvent("KEYPRESS",data)
        
    def OnMousePress(self, button, state, scrx, scry):
        data = MouseData(button, state == 0, scrx, scry)
        Events.FireEvent("MOUSEPRESS", data)
        
    def OnMouseMove(self, scrx, scry):
        data = MouseData(0,0,scrx,scry)
        Events.FireEvent("MOUSEMOVE", data)