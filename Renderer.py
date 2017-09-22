'''
Created on 1 Oct 2013

@author: samgeen
'''

'''
Created on 15 Aug 2011

@author: samgeen
'''

import pyglet
# We do this as OpenGL/GLUT has prefixes on all its functions (e.g. glutInit)
from pyglet.gl import *
from pyglet.gl.glu import *

import Events
            
from asvis.Graphics.FrameBuffer import FrameBuffer
from asvis.Graphics.LogShader import LogShader
from asvis.Graphics.SimplePhysShader import SimplePhysShader

#from Graphics.ColourShader import ColourShader

#import EventHandler as Events

SIZE = 1024
WINSIZE = (SIZE,SIZE)
WINX, WINY = WINSIZE

import Camera

class TextSprite(object):
    '''
    Mainly exists to set my own defaults
    '''
    def __init__(self, textstring, x, y, font='Lato', colour=(255,255,255,255), size=30, anx='left', any='right'):
        # This is part of the interface why not
        self.text = pyglet.text.Label(textstring,
                          font_name=font,
                          font_size=size,
                          color=colour,
                          x=x, y=y,
                          anchor_x=anx, anchor_y=any)
        
    def Draw(self):
        self._text.draw()

class Renderer(object):
    '''
    3D renderer for projecting onto the pyglet.Window
    '''


    def __init__(self, window, camera, frame):
        '''
        Constructor
        '''
        # TODO: Replace redraw with an event? Better parallelism?
        self._redraw = True
        self._modifiers = []#[ColourShader()]
        
        Events.dispatcher.push_handlers(redraw=self.Redraw)
       
        pyglet.resource.path = ['data']
        pyglet.resource.reindex()
        #insimage = pyglet.resource.image("placeholderinstructions.png")
        #self._instructions = pyglet.sprite.Sprite(insimage,subpixel="False")
        #bgimage = pyglet.resource.image("star_crop.jpg")
        #self._background = pyglet.sprite.Sprite(bgimage,subpixel="False")
        
        self._loglabel = pyglet.text.Label('Log',
                          font_name='Lato',
                          font_size=36,
                          color=(255,255,255,200),
                          x=0, y=window.height,
                          anchor_x='left', anchor_y='top',multiline=True,width=1024)
        
        self._frame = frame
        logShader = LogShader()
        #simplePhysShader = SimplePhysShader()
        self._buffer = FrameBuffer(frame.x,frame.y,
                                   frame.width, frame.height,
                                   logShader)#,simplePhysShader)
        
        
    def __del__(self):
        '''
        Destructor (Clean up OpenGL)
        '''
        print "Stopping display"
        
    def Setup(self):
        '''
        Initialise settings for the display
        '''
        # Set up the display mode
        #glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

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
        # Initialise the display settings
        self.Setup()
            
        # Ready?
        # Reeeeady?
        # Okay.
        # Hit it.
        print "Starting display"
    
    def Draw(self, objects=[]):
        '''
        Main display function
        '''
        
        #print "REDRAW:", self._redraw
        if self._redraw:
            self._buffer.Begin()
            # Clear background
            
            #HACK - Clear disabled to test frame buffer
            
         
            #self.DrawScene(objects, "R") 
            self.DrawScene(objects)
                
            self._redraw = False
            self._buffer.End()
        
        self._buffer.DrawTexture()
            
    def DrawScene(self, objects):
        '''
        Draw the 3D scene
        '''
        
        #self._SetupView("3D"+side)
        
        # Set up face culling
        glDisable(GL_CULL_FACE)
    
        # Set up the depth buffer
        glDisable(GL_DEPTH_TEST)
        
        # Set up blend functions for this run
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
                
        # Draw each object, passing them self in case they need it
        # TODO: Add scene graph object to deal with this?
        glDisable(GL_DEPTH_TEST)
        for it in objects:
            if not it is None:
                it.Draw(self)
        
        
    def _SetupView(self, type="2D"):
        wx,wy = self._window.get_size()
        cx = wx//2
        cy = wy//2
        if type == "2D":
            # Set up projection matrix
            glDisable(GL_DEPTH_TEST)
            glLoadIdentity()
            glViewport(0, 0, wx, wy)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(0,wx,0,wy,-1,1)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
        if type == "3DL":
            ox = 0
            oy = 0
            # Set up viewport to position view in centre of screen
            glViewport(ox, oy, WINX, WINY)
            self._camera.Draw()
            if len(self._modifiers) > 0:
                self._modifiers[0].ViewPos(ox, oy)
        if type == "3DR":
            ox = wx - WINX
            oy = 0
            # HACK HACK HACK!!!
            # Set up viewport to position view in centre of screen
            glViewport(0, oy, WINX, WINY)
            self._camera.Draw()
            if len(self._modifiers) > 0:
                self._modifiers[0].ViewPos(ox, oy)
        
    def Redraw(self):
        '''
        Tell the display to redraw its contents the next time it gets a chance
        Dummy required to allow use as an event-driven function
        '''
        self._redraw = True
        
    def ToRedraw(self):
        '''
        Do we have to redraw?
        TODO: Rethink the wording of this interface
        '''
        return self._redraw
        
    def Window(self):
        '''
        Return the display's window object
        '''
        return self._window
    
    def FrameBuffer(self):
        '''
        Return the current frame buffer
        '''
        return self._buffer
        
    def AddModifier(self, newModifier):
        '''
        Add modifier to display
        '''
        self._modifiers.append(newModifier)
        newModifier.Init(self)
