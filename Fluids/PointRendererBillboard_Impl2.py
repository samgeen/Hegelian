'''
Created on Nov 8, 2012

@author: samgeen
'''

from OpenGL.GL import *
from OpenGL.GL import shaders
from PointRenderer import PointRenderer
from GaussianImage import GaussianImage

from Shader import Shader

import numpy as np

class PointRendererBillboard_Impl2(PointRenderer):
    '''
    Uses point sprites
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._points = None
        self._pointSize = 1.0
        self._displayList = 0
        self._name = "PointRenderBillboard"
        self._shader = None
        self._texture = None
        
    def Name(self):
        return self._name
        
    def PointSize(self, pointSize=-1.0):
        '''
        Sets the point size and returns it
        '''
        if pointSize >= 0.0:
            self._pointSize = pointSize
        return self._pointSize
        
    def Build(self, points):
        
        # Make billboarding shader
        self._shader = Shader("PointSpriteScaler")
        
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
        self._points = points
        self._displayList = glGenLists(1)
        glNewList(self._displayList,GL_COMPILE)
        
        glBegin(GL_POINTS)
        for it in self._points:
            glVertex3fv(it)
        glEnd()
        
        glEndList()
    
    
    def Draw(self):
        # Set up point sprites
        glPointSize(20.0)
        glBindTexture(GL_TEXTURE_2D, self._texture)
        glEnable(GL_POINT_SPRITE)
        glTexEnvi(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE)
        glColor4f(1.0,0.0,1.0,0.4)
        # Start shader
        shaders.glUseProgram(self._shader.Shader())
        psLoc = glGetUniformLocation( self._shader.Shader(), 'pointSize' )
        glUniform1f( psLoc,self._pointSize)
        # Call the display list
        glCallList(self._displayList)
        # Clear the shader and texture
        shaders.glUseProgram(0)
        glBindTexture(GL_TEXTURE_2D, 0)