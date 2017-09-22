'''
Created on Nov 8, 2012

@author: samgeen
'''

from OpenGL.GL import *
from OpenGL.GL import shaders
from PointRenderer import PointRenderer
from GaussianImage import GaussianImage

from Graphics.Shader import Shader

import numpy as np

class PointRendererBillboard_Impl4(PointRenderer):
    '''
    Billboarding using geometry shaders
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._points = None
        self._pointSizes = None
        self._sizeRange = (0.0,1.0)
        self._displayList = 0
        self._name = "PointRenderBillboard"
        self._shader = None
        self._texture = None
        
    def Name(self):
        return self._name
    
        print "LIFAIRY"
    def Weight(self, weight):
        self._weight = weight
        
    def Build(self, points,pointSizes=None):
        
        self._pointSizes = pointSizes
        smin = np.min(self._pointSizes)
        smax = np.max(self._pointSizes)
        self._sizeRange = (smin,smax)
        self._pointSizes = (self._pointSizes - smin) / (smax - smin)
        
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
        #glEnable(GL_POINT_SMOOTH)
        #glEnable(GL_PROGRAM_POINT_SIZE)
        
        # Make billboarding shader
        self._shader = Shader("Billboard_Impl2") # TODO: Rename the shader to make this object's Impl no.
        
        # Make display list
        self._points = points
        self._displayList = glGenLists(1)
        glNewList(self._displayList,GL_COMPILE) 
        
        glBegin(GL_TRIANGLES)
        for point, psize in zip(self._points, self._pointSizes):
            glColor4f(psize,0.0,0.0,0.0)
            #glColor4f(1.0,1.0,1.0,1.0)
            glVertex3fv(point)
        glEnd()
        
        glEndList()
    
    def Draw(self):
        glColor4f(1.0,1.0,1.0,1.0)
        glBindTexture(GL_TEXTURE_2D, self._texture)
        # Start shader
        smin, smax = self._sizeRange
        # HACK
        #smin = 1.0
        #smax = 1.0
        # HACK END
        #glPointSize(20)
        densScale = 1.0
        shaders.glUseProgram(self._shader.Shader())
        psminLoc = glGetUniformLocation( self._shader.Shader(), 'pointSizeMin' )
        psmaxLoc = glGetUniformLocation( self._shader.Shader(), 'pointSizeMax' )
        densScaleLoc = glGetUniformLocation( self._shader.Shader(), 'densScale' )
        glUniform1f( psminLoc,smin)
        glUniform1f( psmaxLoc,smax)
        glUniform1f( densScaleLoc,densScale)
        glCallList(self._displayList)
        shaders.glUseProgram(0)
        glBindTexture(GL_TEXTURE_2D, 0)