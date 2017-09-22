'''
Created on 14 Sep 2011

@author: samgeen
'''

from OpenGL.GLUT import *
import EventHandler as Events

# Key press input data structure
class Key(object):
    def __init__(self, name, toggle=False):
        # Key name
        self.name = name
        # Is the key pressed?
        self.pressed = False
        # Is the action a toggle action that turns off after the first press?
        self.toggle = False

class KeyHandler(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Set up key map
        map = dict()
        map["CAMERA_ZOOM_IN"] = Key("q")
        map["CAMERA_ZOOM_OUT"] = Key("e")
        self.__keyMap = map
        
    def RegisterEvents(self):
        Events.RegisterEvent("KEYPRESS", self.ReceiveKeyPress)
        
    def ReceiveKeyPress(self, keyData):
        '''
        Receive a key press and fire all the key events in the key map
        '''
        for action,key in self.__keyMap.items():
            if key.name == keyData.button:
                key.pressed = keyData.state
        self.FireAllKeys()
        
    def FireAllKeys(self):
        '''
        Fire all keys in the keymap
        '''
        # Run through each action in the key map
        for action,key in self.__keyMap.items():
            if key.pressed:
                Events.FireEvent(action,0)
                # If this is a toggle action, reset once action is fired once
                if key.toggle:
                    key.pressed = False
            
        # Now fire a redraw event
        Events.FireEvent("REDRAW",0)
        