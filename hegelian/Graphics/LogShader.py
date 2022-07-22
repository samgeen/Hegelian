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

from .ReductionShader import ReductionShader
from .Shader import Shader
    
class LogShader(object):
    '''
    Simple shader to project images in log space
    '''


    def __init__(self,shaderName="LogBuffer"):
        '''
        Constructor
        '''
        #self._incShader = 0
        self._logShader = 0
        self._shaderName = shaderName
        self._recalcMaxMin = 0 # Counter to recalculate max/min
        self._logmin = -16.5 # = ln(1e-7)
        self._invlogrng = 0.1 # arbitrary guess
        self._prepared = False # Has the shader been initialised?
        self._preloaded = False # Have we found the min/max value of the image?
        self._reduction = None # Reduction shader for calculating min/max
        self._frameBuffer = None 
        
    # Do this when the program is loaded
    def Init(self, frameBuffer):
        
        if not self._prepared:
            self._frameBuffer = frameBuffer
            # Set up shaders
            #self._incShader = Shader("IncrementBuffer")
            self._logShader = Shader(self._shaderName)
            size = max(self._frameBuffer.Width(), self._frameBuffer.Height())
            size = 2.0**int(np.log2(size)+1)
            self._reduction = ReductionShader(self._frameBuffer.Texture(), 
                                              size,
                                              ["ReduceMaxMin"])
            self._prepared = True
        
    # Do this before the objects are rendered
    def Begin(self):
        
        # Reduce the image
        # Get the max/min value in the texture to pass to the shader
        self._recalcMaxMin -= 1
        properScale = self._recalcMaxMin <= 0
        # HACK - turn off properscale counter; turn back on if it runs slowly
        properScale = True # HACK - always run
        if properScale:
            reduce = self._reduction.Run()
            maxval = reduce[0,0]
            minval = reduce[0,1]
            if minval == maxval:
                dmin = 0.0
                dmax = 0.0
                invrng = 1.0
            else:
                dmin = float(np.log(minval))
                dmax = float(np.log(maxval))
                if minval == 0.0:
                    dmin = dmax - 7
                try:
                    invrng = 1.0/(dmax-dmin)
                except:
                    invrng = 1.0
                self._logmin = dmin
                self._invlogrng = invrng
            self._recalcMaxMin = 10
        
        # Reset view
        x,y = self._frameBuffer.Pos()
        width = self._frameBuffer.Width()
        height = self._frameBuffer.Height()
        glViewport(x,y,width, height)
        
        self._logShader.Bind()
        self._logShader.AddFloat(self._logmin, "texmin")
        self._logShader.AddFloat(self._invlogrng, "texinvrng")
        
        
    # Do this after the objects are rendered
    def End(self):
        self._logShader.Unbind()
        
    def Reset(self):
        '''
        Reset the shader; make it run the pre-load operation again
        '''
        self._preloaded = False

