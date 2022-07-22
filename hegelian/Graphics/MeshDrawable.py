'''
Created on 1 Oct 2013

@author: samgeen
'''

import ctypes, collections
from .. import Events

from pyglet.gl import *
import numpy as np

import scipy.special

import os, glob, array

from .SimplePhysShader import SimplePhysShader

def MakeTextureFiles(folder,vars,ltex):
    '''
    Make intermediary texture files to load more quickly
    '''
    
    # Set up colour mode
    lvars = len(vars)
        
    def ReadCube(file):
        return np.load(file).astype("float32")
    
    files = {}
    # Find all the output files
    for var in vars:
        search = folder+os.sep+var+os.sep+"cube_"+var+"_*.npy"
        print("Searching for", search)
        files[var] = glob.glob(search)
        files[var].sort()
    print("Found files", files)
    # Set up output array
    cube = ReadCube(files[var][0])
    length = int(cube.shape[0]**(1.0/3.0)+0.5)
    lcube = length*length*length
    itex = np.arange(0,lcube,dtype="int")*ltex
    texdata = np.zeros((lcube*ltex),dtype="float32")+1.0
    # Run through them all
    numouts = len(files[vars[0]])
    outfiles = []
    for iout in range(0,numouts):
        outfile = files[vars[0]][iout]
        outfile = outfile.replace(vars[0],"TEX")
        outfile = outfile.replace(".npy",".tex")
        if not os.path.exists(outfile):
            print("Writing to file", outfile)
            # Load the cubes
            for ivar in range(0,lvars):
                texdata[itex+ivar] = ReadCube(files[vars[ivar]][iout])
            print(outfile)
            texdata.tofile(outfile)
        outfiles.append(outfile)
    return outfiles, length

class Cubes(object):
    def __init__(self, cubeLocation,hydrovars=["*"]):
        # cubelocation - string containing the location of the cube
        # hydrovar - string containing hydro variable to import (default: "*" = any)
        self._folder = cubeLocation
        self._hydrovars = hydrovars
        self._cols = [GL_RED, GL_GREEN, GL_BLUE]
        self._mode = None
        self._texdata = None
        self._outfiles = []
        self._outcurr = 0
        self._icurr = 0
        self._length = 0
        self._texture = ctypes.c_uint(0)
        self._first = True
        self._toload = True
        self._shader = SimplePhysShader()
    
    def Setup(self):
        # Set up the temporary files
        lvars = len(self._hydrovars)
        if lvars == 1:
            self._mode = GL_RED
            ltex = 1
        elif lvars == 3:
            self._mode = GL_RGBA
            ltex = 4
        else:
            print("Number of variables not supported! Use 1 or 3")
            raise ValueError
        print("Setting up temporary files...")
        self._outfiles, self._length = MakeTextureFiles(self._folder,self._hydrovars,ltex)
        # Put the cube texture into memory
        self.UpdateTexture()
        self._shader.Init()
        print("Cube setup done")
        
    def Texture(self):
        return self._texture
        
    def UpdateTexture(self):
        # Set up cubes to use
        if self._toload:
            currfile = self._outfiles[self._icurr]
            print("Loading file", currfile)
            self._texdata = np.fromfile(currfile,dtype='float32')
            print("TEXDATA MINMAX", self._texdata.min(),self._texdata.max())
            # Update the texture in graphics memory
            texsize = self._length
            c_float_p = ctypes.POINTER(ctypes.c_float)
            data_p = self._texdata.ctypes.data_as(c_float_p)
            glEnable(GL_TEXTURE_3D)
            glActiveTexture(GL_TEXTURE0)
            if self._first:
                print("Making texture...", )
                # Set up texture in graphics memory for the first time
                gl.glGenTextures(1,self._texture)
                glBindTexture( GL_TEXTURE_3D, self._texture )
                glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
                glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
                glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
                glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_BORDER)
                glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexImage3D(GL_TEXTURE_3D, 0, GL_RGBA32F_ARB, 
                    texsize, texsize, texsize, 0,
                    self._mode, GL_FLOAT,data_p)
                self._first = False
            else:
                print("Updating texture data...",)
                # Update the existing texture (subimages are faster than remaking the texture array each time)
                glBindTexture( GL_TEXTURE_3D, self._texture )
                glTexSubImage3D(GL_TEXTURE_3D, 0, 
                    0,0,0, 
                    texsize, texsize, texsize,
                    self._mode, GL_FLOAT,data_p)
            # Tidy up
            print("Done")
            glBindTexture( GL_TEXTURE_3D, 0 )
            self._toload = False
    
    def NextCube(self):
        self._icurr += 1
        self._toload = True
        self.UpdateTexture()
            
    def PrevCube(self):
        self._icurr -= 1
        self._toload = True
        self.UpdateTexture()
        
    def _PlotSlice(self, slice):
        off = -0.707#-0.5
        ext = 1.414
        toff = -0.707
        text = 1.414
        glTexCoord3f(toff, toff, slice)
        glVertex3f(off,off,slice)
        glTexCoord3f(toff+text, toff, slice)
        glVertex3f(off+ext,off,slice)
        glTexCoord3f(toff+text, toff+text, slice)
        glVertex3f(off+ext,off+ext,slice)
        glTexCoord3f(toff, toff+text, slice)
        glVertex3f(off,off+ext,slice)
        
        
    # Draw the points to screen
    def Draw(self):
        '''
        Draw object
        '''
        
        # First time through?
        # NOTE: I have no idea how reliable this code is at determining whether we set these things
        if self._first:
            self.Setup()
            self._first = False
        
        glEnable(GL_TEXTURE_3D)
        #glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_3D, self.Texture())
        
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE,GL_ONE)
        
        glColor4f(1.0,1.0,1.0,1.0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glMatrixMode(GL_TEXTURE)
        glPushMatrix()
        #glTranslatef(-0.5,-0.5,-0.5)
        #glRotatef(90,0,0,1)
        glMatrixMode(GL_MODELVIEW)
        
        # Draw the mesh
        # Billboard the quads
        modelview = (GLfloat * 16)()
        textureview = (GLfloat * 16)()
        # Get the existing matrices
        glGetFloatv(GL_MODELVIEW_MATRIX, modelview)    
        glGetFloatv(GL_TEXTURE_MATRIX, textureview)
        glMatrixMode(GL_MODELVIEW)
        # Undo rotation (and scaling)
        model = np.ctypeslib.as_array(modelview).reshape(4,4)
        rotate = model[0:3,0:3]
        invrot = np.linalg.inv(rotate)
        for i in range(0,3):
            for j in range(0,3):
                textureview[i*4+j] = invrot[i,j]#modelview[i*4+j]
                if i == j:
                    modelview[i*4+j] = 1.0
                else:
                    modelview[i*4+j] = 0.0
        textureview[12] = textureview[13] = textureview[14] = 0.5
        # Set the new modelview matrix
        glLoadMatrixf(modelview)
        #glTranslatef(0.5,0.5,0.5)
        glMatrixMode(GL_TEXTURE)
        glLoadMatrixf(textureview)
        #glTranslatef(-0.5,-0.5,-0.5)
        #glTranslatef(0.5,0.5,0.5)
        #glTranslatef(-1,-1,-1)
        #glScalef(0.5,0.5,0.5)
        
        # Draw the quads
        self._shader.Begin()
        glBegin(GL_QUADS)
        self._PlotSlice(0.707)
        glEnd()
        self._shader.End()
        glMatrixMode(GL_TEXTURE)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_3D, 0)
        glDisable(GL_TEXTURE_3D)
        
        # Draw bounding line
        glBegin(GL_LINE_STRIP)
        glVertex3f(0.5,0.5,0.0)
        glVertex3f(-0.5,0.5,0.0)
        glVertex3f(-0.5,-0.5,0.0)
        glVertex3f(0.5,-0.5,0.0)
        glVertex3f(0.5,0.5,0.0)
        glEnd()
        # Draw star
        glPointSize(3.0)
        glDisable(GL_BLEND)
        glColor4f(1.0,0.5,0.0,0.7)
        glBegin(GL_POINTS)
        glVertex3f(0.0,0.0,0.0)
        glEnd()

class MeshDrawable(object):
    '''
    A uniform cubic mesh drawable object
    '''
    def __init__(self, cubeLocation, window,hydrovars=["*"]):
        '''
        Constructor
        cubeLocation - place where cubes are found
        density - a NxNxN cube of density
        hydrovars - hydro variables for the cubes to use
                    If a string, only show one variable
                    If an array, show three variables
        '''
        self._hydrovars = hydrovars
        self._cubes = Cubes(cubeLocation,hydrovars=hydrovars)
            
        self._window = window
        self._redraw = True
        # Switch cubes?
        self._userInput = Events.UserInputHandler(self)
        self._window.push_handlers(self._userInput)
        
    def ToRedraw(self):
        return self._redraw
    
    def Redraw(self, redraw):
        self._redraw = redraw
    
    def Draw(self, frame):
        '''
        Draw object
        '''
        self._cubes.Draw()

    def OnKeyboard(self, state):
        '''
        Register the pressing or releasing of a keyboard key
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        # Escape
        pressed = state["pressed"]
        button = state["button"]
        
        # Z - previous cube
        if button == pyglet.window.key.Z and not pressed:
            self._cubes.PrevCube()
        # X - next cube
        if button == pyglet.window.key.X and not pressed:
            self._cubes.NextCube()
        # Redraw
        self.Redraw(True)
        Events.Redraw()
            
    def OnMouseMove(self, state):
        # Necessary for handler interface
        pass
        
    def OnMouseButton(self, state):
        # Necessary for handler interface
        pass
            
