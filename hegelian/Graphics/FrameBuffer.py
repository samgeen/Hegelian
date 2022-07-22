'''
Created on 29 May 2012

@author: samgeen
'''

import pyglet
from pyglet.gl import *
from pyglet.gl.glu import *
import ctypes, array
import numpy as np

    
class FrameBuffer(object):
    '''
    Framebuffer object designed to store rendered object as a texture for later manipulation
    '''


    def __init__(self, x, y, width, height, postShader=None, preShader=None):
        '''
        Constructor
        width, height - width and height of buffer in pixels
        postShader - applies a shader to the output of the frame buffer
        preShader - processes input fragments before they are put into the frame buffer
        '''
        self._pos = (x,y)
        self._width, self._height = (width, height)
        self._texW = 0
        self._texH = 0
        self._postShader = postShader
        self._preShader = preShader
        self._depth = 0#ctypes.c_int(0)
        self._frame = 0#ctypes.c_int(0)
        self._texture = 0#ctypes.c_int(0)
        self._image = 0
        self._prepared = False
        
    def Pos(self):
        return self._pos
        
    def Width(self):
        return self._width
    
    def Height(self):
        return self._height
        
    def Texture(self):
        '''
        Return the frame buffer's OpenGL texture ID
        '''
        return self._texture
    
    # Do this when the program is loaded
    def Init(self):
        
        if not self._prepared:
            # Set up image 
            
            # Set up empty texture to draw to
            self._texture = ctypes.c_uint(0)
            glGenTextures(1,self._texture)
            #self._texture = pyglet.image.Texture.create(self._width, self._height, rectangle=True,internalformat=GL_RGBA32F_ARB)
            
            
            # I honestly don't know what half of this stuff is supposed to do
            glEnable( GL_TEXTURE_2D )
            glBindTexture( GL_TEXTURE_2D, self._texture )
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glPixelStorei(GL_UNPACK_ROW_LENGTH, 0)
            glPixelStorei(GL_UNPACK_SKIP_PIXELS, 0)
            glPixelStorei(GL_UNPACK_SKIP_ROWS, 0)
            # Find the width of the texture in 2^N
            self._texW = 2**int(np.log2(self._width)+1)
            self._texH = 2**int(np.log2(self._height)+1)
            
            # On some systems this is needed to wipe the initial frame buffer rather than just setting the pointer to 0
            empty = np.zeros((self._texW,self._texH,4))
            c_float_p = ctypes.POINTER(ctypes.c_float)
            empty_p = empty.ctypes.data_as(c_float_p)
            
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F_ARB, self._texW, self._texH, 0,\
             GL_RGBA, GL_FLOAT, empty_p)
            #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self._width, self._height, 0,\
            # GL_RGBA, GL_UNSIGNED_BYTE, 0)
            glBindTexture(GL_TEXTURE_2D, 0)
            
            # Set up the frame buffer object
            self._frame = ctypes.c_uint(0)
            glGenFramebuffers(1,self._frame)
            #self._frame = glGenFramebuffers(1)
            glBindFramebuffer(GL_FRAMEBUFFER, self._frame)
            
            # Set up the depth buffer
            #self._depth = glGenRenderbuffers(1)
            self._depth = ctypes.c_uint(0)
            glGenRenderbuffers(1,self._depth)
            glBindRenderbuffer(GL_RENDERBUFFER, self._depth)
            
            glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, self._width, self._height)
            glBindRenderbuffer(GL_RENDERBUFFER, 0)
            
            # Attach texture and depth buffer
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self._texture, ctypes.c_int(0))
            glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self._depth)
            
            # Unbind frame buffer for now
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
        
            status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
            print("FRAME BUFFER STATUS:", status)
            
            # Set up the shaders
            if not self._preShader is None:
                self._preShader.Init(self)
                
            if not self._postShader is None:
                self._postShader.Init(self)
            
            self._prepared = True
        
    # Do this before the objects are rendered
    def Begin(self):
        
        if not self._prepared:
            self.Init()
        # Bind frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, self._frame)
        
        # Allow texture access to frame buffer
        #glActiveTexture(GL_TEXTURE1)
        #glBindTexture(GL_TEXTURE_2D,self._texture)
        
        # Clear frame buffer
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDisable( GL_TEXTURE_2D )
        glViewport(0,0,self._width, self._height)
        # At this point we draw the scene
        
        if not self._preShader is None:
            self._preShader.Begin()
        
    # Do this after the objects are rendered
    def End(self):
        # Unbind frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        if not self._preShader is None:
            self._preShader.End()
        # Clean up texture
        #glActiveTexture(GL_TEXTURE1)
        #glBindTexture(GL_TEXTURE_2D,0)
        glActiveTexture(GL_TEXTURE0)
        # Inform the shader that the image has changed
        if not self._postShader is None:
            self._postShader.Reset()
    
    def DrawTexture(self):
        # Now we need to plot the texture to screen
        # Set up an orthogonal projection
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 1, 0, 1, -10, 10)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glDisable(GL_BLEND)
        #glDrawPixels(self._width, self._height, GL_RGBA, GL_FLOAT, self._texture)
        # Now draw the texture with the log shader
        # Draw the texture onto a flat plane
        glColor4f(1.0,1.0,1.0,1.0)
        glEnable( GL_TEXTURE_2D )
        #glDisable(GL_TEXTURE_GEN_S)
        #glDisable(GL_TEXTURE_GEN_T)
        if not self._postShader is None:
            self._postShader.Begin()
        glBindTexture( GL_TEXTURE_2D, self._texture )
        glBegin(GL_TRIANGLES)
        # Scale texture coords to only show used part of texture
        s = float(self._width)/float(self._texW)
        t = float(self._height)/float(self._texH)
        glTexCoord2d(0.0,0.0);        glVertex3f(0.0, 0.0, 0.0);
        glTexCoord2d(s,  0.0);        glVertex3f(1.0, 0.0, 0.0);
        glTexCoord2d(s,  t  );        glVertex3f(1.0, 1.0, 0.0);
        
        glTexCoord2d(s,  t  );        glVertex3f(1.0, 1.0, 0.0);
        glTexCoord2d(0.0,t  );        glVertex3f(0.0, 1.0, 0.0);
        glTexCoord2d(0.0,0.0);        glVertex3f(0.0, 0.0, 0.0);
        glEnd()
        glBindTexture( GL_TEXTURE_2D, 0 )
        if not self._postShader is None:
            self._postShader.End()

