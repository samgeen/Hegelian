'''
Created on 15 Aug 2011

@author: samgeen
'''

# TODO: TURN INTO INTERFACE RATHER THAN CONCRETE CLASS
# TODO: ALLOW DIFFERENT RENDER MODELS (e.g. OPENGL/SOFTWARE)
# We do this as OpenGL/GLUT has name identifiers on all its funcions (e.g. glutInit)
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import OpenGLStatics
from Window import Window
from Viewport import Viewport
from Stopwatch import Stopwatch

import EventHandler as Events

SIZE = 512
WINSIZE = (SIZE,SIZE)
WINX, WINY = WINSIZE

class Display():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        # TODO: Replace redraw with an event? Better parallelism?
        self.__redraw = True
        # TODO: REMOVE HARD-CODED DIMENSIONS?
        self.__window = Window(WINX, WINY)
        self.__viewport = Viewport(WINX, WINY)
        self.__objects = list()
        self.__timer = Stopwatch()
        self.__lastFrameTime = 0.0
        self._modifiers = list()
        Events.RegisterEvent("REDRAW", self.Redraw)
        
    def __del__(self):
        '''
        Destructor (Clean up OpenGL)
        '''
        print "Stopping display"
        
    def Initialise(self):
        '''
        Initialise settings for the display
        '''
        # Set up the display mode
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

        # Set up a default clear colour
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        # Set up a default point size
        glPointSize(5.0)

        # Set up Blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
    
        # Set up face culling
        glDisable(GL_CULL_FACE)
    
        # Set up the depth buffer
        glEnable(GL_DEPTH_TEST)

        # Setup menu - TODO: THIS
        # GetMain()->m_input->m_popup->CreateMenu();

    def Start(self):
        '''
        Start the main display loop
        '''
        glutInit()
        # Initialise the display settings
        self.Initialise()
        
        # Set up the OpenGL.GLUT window
        self.__window.Init()

        # Give OpenGL functions to call for display, input, etc
        OpenGLStatics.SetupOpenGLStatics()
            
        # Ready?
        # Reeeeady?
        # Okay.
        # Hit it.
        print "Starting display"
        glutMainLoop()
    
    def Draw(self):
        '''
        Main display function
        '''
        # Start timer
        self.__timer.Reset()
        
        # Clear background
        #HACK - Clear disabled to test frame buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Start up viewports
        # TODO: ALLOW MORE THAN ONE
        self.__viewport.Begin()
        
        # Set up blend functions for this run (TODO: Pass to object draw code / shaders)
        #glEnable(GL_BLEND)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # TODO: REMOVE THIS HACK AND REPLACE WITH PROPER SHADERS
        glColor4f(1.0,0.0,0.0,0.2)
        glPointSize(3.0)
        
        # Set up modifier
        for mod in self._modifiers:
            mod.Init(self)
        
        # Begin modifier
        for mod in self._modifiers:
            mod.Begin(self)
                
        # Draw each object, passing them the camera in case they need it
        # TODO: Add scene graph object to deal with this?
        for it in self.__objects:
            it.Draw(self.__viewport)
        
        # Run modifier end actions
        for mod in self._modifiers:
            mod.End(self)
        
        # Finish up drawing
        self.__viewport.End()
        glFlush()        
        glutSwapBuffers()

        # Don't need to redraw no more
        self.__redraw = False
        
        # Read off draw time
        self.__lastFrameTime = self.__timer.Time()
        #print "Frame time: ", self.__lastFrameTime
        
    def Idle(self):
        '''
        Is GLUT not doing anything? Do these things!
        '''
        # Check for redraw request and if there's one, do that
        if self.__redraw:
            self.Draw()
            
    def Redraw(self, dummy=0):
        '''
        Tell the display to redraw its contents the next time it gets a chance
        Dummy required to allow use as an event-driven function
        '''
        self.__redraw = True
        
    def Window(self):
        '''
        Return the display's window object
        '''
        return self.__window
    
    def Viewport(self):
        '''
        Return the viewport
        '''
        return self.__viewport
    
    def AddObject(self, newObject):
        '''
        Preload and add object to display list
        '''
        # Preload removed as this must happen in an OpenGL context
        #newObject.Preload()
        self.__objects.append(newObject)
        
    def AddModifier(self, newModifier):
        '''
        Add modifier to display
        '''
        self._modifiers.append(newModifier)
    
    def FramesPerSecond(self):
        '''
        Return the current FPS (based on last frame draw time)
        '''
        return 1.0/self.__lastFrameTime
