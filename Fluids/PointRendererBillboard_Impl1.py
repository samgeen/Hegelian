'''
Created on Nov 8, 2012

@author: samgeen
'''

from OpenGL.GL import *
from OpenGL.GL import shaders
from PointRenderer import PointRenderer

from Shader import Shader

import numpy as np

class PointRendererBillboard_Impl1(PointRenderer):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._points = None
        self._displayList = 0
        self._name = "PointRenderBillboard"
        self._shader = None
        
    def Name(self):
        return self._name
    
    def Weight(self, weight):
        self._weight = weight
        
    def Build(self, points,pointSizes=None):
        
        # Make billboarding shader
        self._shader = Shader("Billboard")
        
        # Make display list
        self._points = points
        self._displayList = glGenLists(1)
        glNewList(self._displayList,GL_COMPILE) 
        c = 0.005
        c0 = np.array([-c,-c,0])
        c1 = np.array([-c,+c,0])
        c2 = np.array([+c,+c,0])
        c3 = np.array([+c,-c,0])
        
        glBegin(GL_TRIANGLES)
        for it in self._points:
            glVertex3fv(it+c0)
            glVertex3fv(it+c1)
            glVertex3fv(it+c2)
            
            glVertex3fv(it+c0)
            glVertex3fv(it+c2)
            glVertex3fv(it+c3)
        glEnd()
        
        glEndList()
    
    def Draw(self):
        glColor4f(1.0,0.0,1.0,0.4)
        shaders.glUseProgram(self._shader.Shader())
        glCallList(self._displayList)
        shaders.glUseProgram(0)