'''
Created on Nov 8, 2012

@author: samgeen
'''

from pyglet.gl import *
from PointRenderer import PointRenderer
from GaussianImage import GaussianImage

from Graphics.Shader import Shader

import numpy as np

class PointRendererBillboard_Impl3(PointRenderer):
    '''
    Uses point sprites
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._points = None
        self._pointSizes = None
        self._weight = 1.0
        self._sizeRange = (0.0,1.0)
        self._displayList = 0
        self._name = "PointRenderBillboard"
        self._shader = None
        self._texture = None
        
    def Name(self):
        return self._name
    
    def Weight(self, weight):
        self._weight = weight
        
    def Build(self, points, pointSizes):
        
        # Set internal arrays
        self._points = points
        self._pointSizes = pointSizes
        
        # Refactor the point size list
        smin = np.min(self._pointSizes)
        smax = np.max(self._pointSizes)
        self._sizeRange = (smin,smax)
        self._pointSizes = (self._pointSizes - smin) / (smax - smin)
        
        # Make billboarding shader
        self._shader = Shader("PointSpriteScalerImpl3")
        
        # Make the billboarding texture
        texSize = 16
        im = GaussianImage(texSize)
        self._texture = glGenTextures(1)
        glEnable( GL_TEXTURE_2D )
        glBindTexture( GL_TEXTURE_2D, self._texture )
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, texSize, texSize, 0, GL_RGBA, GL_FLOAT, im)
        glBindTexture(GL_TEXTURE_2D, 0)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_PROGRAM_POINT_SIZE)
        
        # Make display list
        self._displayList = glGenLists(1)
        glNewList(self._displayList,GL_COMPILE)
        
        glBegin(GL_POINTS)
        for point, psize in zip(self._points, self._pointSizes):
            glColor4f(psize,0.0,0.0,0.0)
            glVertex3fv(point)
        glEnd() # GL_POINTS
        
        glEndList()
    
    
    def Draw(self):
        # Set up point sprites
        glPointSize(20.0)
        glBindTexture(GL_TEXTURE_2D, self._texture)
        glEnable(GL_POINT_SPRITE)
        glTexEnvi(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE)
        #glColor4f(1.0,0.0,1.0,0.4)
        # Start shader
        smin, smax = self._sizeRange
        #shaders.glUseProgram(self._shader.Shader())
        #psminLoc = glGetUniformLocation( self._shader.Shader(), 'pointSizeMin' )
        #psmaxLoc = glGetUniformLocation( self._shader.Shader(), 'pointSizeMax' )
        #glUniform1f( psminLoc,smin)
        #glUniform1f( psmaxLoc,smax)
        self._shader.Bind()
        self._shader.AddVariable(smin, "pointSizeMin","1f")
        self._shader.AddVariable(smax, "pointSizeMax","1f")
        # Call the display list
        glCallList(self._displayList)
        # Clear the shader and texture
        #shaders.glUseProgram(0)
        self._shader.Unbind()
        glBindTexture(GL_TEXTURE_2D, 0)