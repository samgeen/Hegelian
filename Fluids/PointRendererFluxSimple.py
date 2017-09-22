'''
Created on Nov 8, 2012

@author: samgeen
'''

from OpenGL.GL import *
from PointRenderer import PointRenderer

class PointRendererSimple(PointRenderer):
    '''
    Render the flux from 
    TODO: DECOUPLE FLUX CALCULATIONS FROM POINT RENDERER
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._points = None
        self._weight = 1.0
        self._displayList = 0
        self._name = "PointRenderSimple"
        
    def Name(self):
        return self._name
    
    def Weight(self, weight):
        self._weight = weight
        
    def Build(self, points,dummy=None):
        
        self._points = points
        self._displayList = glGenLists(1)
        glNewList(self._displayList,GL_COMPILE) 
        
        glBegin(GL_POINTS)
        for it in self._points:
            glVertex3fv(it)
        glEnd()
        
        glEndList()
    
    def Draw(self):
        glColor4f(1.0,1.0,1.0,0.4*self._weight)
        #print self.__displayList
        glCallList(self._displayList)