'''
Created on 17 Aug 2011

@author: samgeen

NOTE! THIS FILE IS MAINLY TO ALLOW OO IN OPENGL
YOU DON'T HAVE TO USE THIS FILE, NOR SHOULD YOU
THE ENTRY POINT INTO THIS IS Alice.py
'''

from Display import Display
from Input import Input
from EventHandler import EventHandler

from OpenGL.GLUT import *

# OpenGL requires only one display at a time
# It doesn't support OO or multiple instances very well
# Alice.py calls these as singleton instances to resolve this
singletonDisplay = Display()
singletonInput = Input()
    
'''
Wrapper functions
This is needed because GLUT only accepts statics or globals
'''

def DisplayFunc():
    singletonDisplay.Draw()
    
def ReshapeFunc(width, height):
    singletonDisplay.Window().Reshape(width, height)

def IdleFunc():
    singletonDisplay.Idle()

def MouseFunc(button, state, scrx, scry):
    singletonInput.OnMousePress(button, state, scrx, scry)

def MotionFunc(scrx, scry):
    singletonInput.OnMouseMove(scrx, scry)
    
def KeyboardFunc(key, scrx, scry):
    singletonInput.OnKeyDown(key, scrx, scry)
    
def KeyboardUpFunc(key, scrx, scry):
    singletonInput.OnKeyUp(key, scrx, scry)
    
def SetupOpenGLStatics():
    glutDisplayFunc(DisplayFunc)
    glutReshapeFunc(ReshapeFunc)
    glutIdleFunc(IdleFunc)
    glutKeyboardFunc(KeyboardFunc)
    glutKeyboardUpFunc(KeyboardUpFunc)
    glutMouseFunc(MouseFunc)
    glutMotionFunc(MotionFunc)