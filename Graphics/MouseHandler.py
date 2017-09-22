'''
Created on 14 Sep 2011

@author: samgeen
'''

import EventHandler as Events
from OpenGL.GLUT import *
# TODO: Can we have circular imports? How does that work? Works fine in C++!
# We really need this in case we have more than one camera.
# Plus firing everything through the event handler is tiring
#from Camera import Camera

# TODO: CONVERT THIS INTO A CAMERA HANDLER OBJECT
# TODO: FOLD MOUSE INPUTS INTO KEYHANDLER AND RENAME THAT
# TODO: ALLOW MOUSE INPUT "ZONES" ON THE SCREEN THAT FIRE DIFFERENT EVENTS DEPENDING 
#       ON THE POSITION OF THE CURSOR

class MouseHandler(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Mouse state information (hacky?)
        self.__x = 0
        self.__y = 0
        self.__leftPressed = False
        self.__rightPressed = False
        self.__rotateSpeed = 100.0
        self.__zoomSpeed = 1.01
        
    def RegisterEvents(self):
        '''
        Register this object to receive mouse movement commands
        '''
        Events.RegisterEvent("MOUSEMOVE", self.ReceiveMouseMove)
        Events.RegisterEvent("MOUSEPRESS", self.ReceiveMousePress)
        
    def ReceiveMouseMove(self, data):
        '''
        Receive mouse movement information
        '''
        # Is the left button pressed? If so, rotate the camera
        if self.__leftPressed:
            ax = (self.__x - data.scrx) / self.__rotateSpeed
            ay = (self.__y - data.scry) / self.__rotateSpeed
            angle = [ax,ay]
            Events.FireEvent("CAMERA_ROTATE", angle)
            self.__x = data.scrx
            self.__y = data.scry
        
    def ReceiveMousePress(self, data):
        '''
        Receive mouse button press information
        '''
        if data.button == GLUT_LEFT_BUTTON:
            self.__leftPressed = data.state
        if self.__leftPressed:
            self.__x = data.scrx
            self.__y = data.scry
            
    def RotateSpeed(self, newSpeed):
        self.__rotateSpeed = newSpeed