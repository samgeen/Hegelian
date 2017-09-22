'''
Created on 18 Aug 2011

@author: samgeen
'''

import numpy as np
from OpenGL.GL import *
import Camera
from Maths.Vect3 import Vect3

class Viewport(object):
    '''
    A single OpenGL viewport inside the window
    '''

    def __init__(self, width, height):
        '''
        Constructor
        '''
        self.__camera = Camera() 
        self.__width = width
        self.__height = height

    def ReplaceCamera(self, camera):
        '''
        Replaces the existing camera
        '''
        self.__camera = camera
        
    def Camera(self):
        '''
        Returns the camera object used by the viewport
        '''
        return self.__camera
    
    def Begin(self):
        '''
        Begins the process of drawing the viewport to screen
        '''
        ' Draw the viewport '
        glViewport(0, 0, self.__width, self.__height)
        
        ' Draw the camera '
        self.__camera.Draw()
        
    def End(self):
        '''
        Ends the proces of drawing the viewport to screen
        '''
        pass
        
    # Do we draw this object, or is it too far away to see?
    # Takes a position and radius of bounding sphere
    # TODO: Allow more sophisticated diagnostics, e.g. a heightfield
    # TODO: Add some kind of frustum culling
    # TODO: Encapsulate this away?
    def DrawTest(self, position, radius):
        # Do a type test for position
        if type(position) != type(Vect3):
            position = Vect3(position)
        # Window pixel size
        winPix = np.min([self.__width, self.__height])
        # Smaller than 3 pixels, trigger failure of draw test
        pixLimit = 3
        # Minimum distance to object from camera
        pos = position - self.Camera().Position()
        dist = pos.Length() - radius
        # Pixel size of object
        # HACK! HARD CODED VIEW ANGLE 45 deg!!
        objPix = 2.0*np.arctan2(radius, dist) / (0.25*np.pi) * winPix
        # Is the object big enough?
        return objPix >= pixLimit