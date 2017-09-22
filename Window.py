'''
Created on 17 Feb 2014

@author: samgeen
'''

import os, sys, pyglet
from pyglet.window import key, event
from pyglet.gl import * # it already has the gl prefix so OK whatevs

import Frame as Level
import Events as Events
import Renderer as Renderer

class Window(pyglet.window.Window):
    # TODO: Use @ decorators and make this by composition instead!
    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
    
        # Stop pyglet burning a hole through the Earth's core with your cpu
        pyglet.clock.set_fps_limit(60)
        
    def on_key_press(self, symbol, modifiers):  
        '''
        Overload on_key_press to allow the level to clean up first
        '''      
        if symbol == key.ESCAPE and not (modifiers & ~(key.MOD_NUMLOCK | key.MOD_CAPSLOCK | key.MOD_SCROLLLOCK)):
            press = {"button":symbol, "mod": modifiers, "pressed":True}
            self._level.OnKeyboard(press)
            # Give the window a chance to tidy up
            self.dispatch_event('on_close')