'''
Created on 15 Aug 2011

@author: samgeen
'''

from OpenGL.GL import *
from OpenGL.GLUT import *

# TODO: REFACTOR DISPLAY WINDOW PARTS INTO HERE

class Window(object):
    '''
    classdocs
    '''


    def __init__(self, width, height):
        '''
        Constructor
        '''
        # Set defaults that can be overridden later
        self.__width = width
        self.__height = height
        self.__r = 0.0
        self.__g = 0.0
        self.__b = 0.0
    
    # Initialise window
    def Init(self):
        glutInitWindowSize (self.__width, self.__height)
        glutInitWindowPosition (0, 0)
        glutCreateWindow ("Alice")
    
    def Shape(self):
        return (self.__width, self.__height)
    
    def Reshape(self,width,height):
        '''
        Reshape the window with size (x,y)
        ''' 
        __width = width
        __height = height
        if __width > __height:
            glViewport((__width-__height)/2,0,
                          __height,__height)
        else:
            glViewport(0,(__height-__width)/2,
                          __width,__width)
        
    def Background(self,r,g,b):
        '''
        Set the background colour
        '''
        self.__r = r
        self.__g = g
        self.__b = b
        glClearColor(r,g,b)