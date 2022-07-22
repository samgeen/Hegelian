'''
Created on 24th April 2013

@author: samgeen
'''

import os, sys, pyglet
from pyglet.gl import * # it already has the gl prefix so OK whatevs

import random
import numpy as np

from Window import Window
import zsprite
import Frame

from Snapshot import Snapshot
from Renderer import Renderer
import Camera
from Graphics.ColourShader import ColourShader




# REMOVE EVERYTHING BELOW HERE

smallfont = pyglet.font.load("Courier New", 14)
white = color=(1.0,1.0,1.0,1.0)
red   = color=(1.0,0.0,0.0,1.0)
black = color=(0.0,0.0,0.0,1.0)

class AsVis(Frame.Frame):
    '''
    The top level object for visualising astrophysics 
    '''

    def __init__(self, window=None):
        '''
        Constructor
        '''
        Frame.Frame.__init__(self)
        self._renderer = None
        self._snapshot = Snapshot()
        self._camera = Camera()
        self._setup = False
        self._lmb = False
        # Make the game window
        title = "Astrophysics Visualisation"
        windowed = True
        
        screenSize = (1800,1024)
        if window == None:
            window = pyglet.window.Window(screenSize[0], screenSize[1],caption = title)
        self._window = window
        
    def Window(self):
        '''
        Return the pyglet window object used by the visualiser
        '''
        return self._window
        
    def Run(self):
        '''
        Start the draw loop
        '''
        pyglet.app.run()
        
    def Setup(self):
        '''
        Set up the main level - can usually be guaranteed to run before Run()
        '''
        glEnable(GL_DEPTH_TEST)
        if not self._setup:
            # This starts threads and stuff, so don't grunk up anything by 
            self._renderer = Renderer(self.Window(), self._camera)
            self._renderer.Setup()
            self._setup = True
    
    def LoadSnapshot(self, filename):
        '''
        Load a snapshot
        '''
        self._snapshot.Open(filename)
        self._renderer.LogText(self._snapshot.InfoText())
        self._renderer.Redraw()
            
    def Draw(self, dummy=None):
        if self._camera.ZoomActive():
            self._renderer.Redraw()
        self._renderer.Draw([self._snapshot])
        #if self._camera.ZoomActive():
        
    def Redraw(self):
        self._renderer.Redraw()
        
    def OnMouseMove(self, state):
        '''
        Parse mouse movement
        '''
        if self._lmb:
            self._renderer.Camera().OnMouseMove(state)
        self.Redraw()

    def OnKeyboard(self, state):
        '''
        Register the pressing or releasing of a keyboard key
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        # 113 = Q, 101 = e, YES I KNOW I'M IN A HURRY OK
        # Escape
        pressed = state["pressed"]
        button = state["button"]
        #if button == pyglet.window.key.ESCAPE:
            # Upon returning the window will now quit too
        # Q
        if button == pyglet.window.key.Q:
            self._renderer.Camera().ZoomIn(pressed)
        # E
        if button == pyglet.window.key.E:
            self._renderer.Camera().ZoomOut(pressed)
            
        # Switch render modes
        # TODO: Unbreak this
        #if button == pyglet.window.key.P and not pressed:
        #    self._renderer.ToggleBillboarding()
        
    def OnMouseButton(self, state):
        if state["button"] % 2 == pyglet.window.mouse.LEFT:
            self._lmb = state["pressed"] # True if pressed, False if not
        
if __name__ == '__main__':
    # NOTE - this will run the visualiser immediately
    asvis = AsVis()
    asvis.LoadSnapshot("spiral68_010")
    asvis.Run()

