'''
Created on 29 May 2012

@author: samgeen
'''

import pyglet
# Import straight into the global namespace because the "gl" prefix counts enough as a namespace-equivalent for us
from pyglet.gl import *
from pyglet.gl.glu import *
import ctypes, array
import numpy as np

from Shader import Shader
    
class SimplePhysShader(object):
    '''
    Simple shader to project images in log space
    '''


    def __init__(self,shaderName="SimplePhysBuffer"):
        '''
        Constructor
        '''
        #self._incShader = 0
        self._shaderName = shaderName
        self._prepared = False # Has the shader been initialised?
        self._frameBuffer = None 
        
    # Do this when the program is loaded
    def Init(self):
        
        if not self._prepared:
            # Set up shaders
            self._shader = Shader(self._shaderName)
            self._prepared = True
        
    # Do this before the objects are rendered
    def Begin(self):
        self._shader.Bind()
        
    # Do this after the objects are rendered
    def End(self):
        self._shader.Unbind()
        
    def Reset(self):
        '''
        Reset the shader; make it run the pre-load operation again
        NOTE: THIS IS PROBABLY UNNEEDED, DELETE TO CLEAN UP INTERFACE
        '''
        self._preloaded = False

