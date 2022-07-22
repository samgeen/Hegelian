'''
Created on 29 May 2012

@author: samgeen
'''

# We do this as OpenGL/GLUT has name identifiers on all its funcions (e.g. glutInit)
#from OpenGL.GL import *
#from OpenGL.GLU import *
#from OpenGL.GLUT import *
#from OpenGL.GL.ARB.framebuffer_object import *
#from OpenGL.GL.ARB.texture_float import *
#from OpenGL.GL.ARB.imaging import *
#from OpenGL.GL import shaders
import pyglet
from pyglet.gl import *
from pyglet.gl.glu import *
import ctypes, array
import numpy as np

from ReductionShader import ReductionShader
from Shader import Shader

'''
class TestShader(object):
    def __init__(self, name):
        # Read shader files
        fragname = "Graphics/Shaders/"+name+".frag"
        vertname = "Graphics/Shaders/"+name+".vert"
        frag = self._ReadShader(fragname)
        vert = self._ReadShader(vertname)
        # Compile shaders
        VERTEX_SHADER = shaders.compileShader(vert, GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader(frag, GL_FRAGMENT_SHADER)        
        self.shader = shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)
        
    def Shader(self):
        return self.shader
    
    def _ReadShader(self, filename):
        f = open(filename,"r")
        data = f.read()
        f.close()
        return data
'''
    
class ColourShader(object):
    '''
    Simple shader to project images in log space
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._x, self._y = (0,0)
        self._width, self._height = (0,0)
        self._depth = 0#ctypes.c_int(0)
        self._frame = 0#ctypes.c_int(0)
        self._texture = 0#ctypes.c_int(0)
        self._image = 0
        self._incShader = 0
        self._logShader = 0
        self._recalcMaxMin = 0 # Counter to recalculate max/min
        self._logmin = -16.11 # = ln(1e-7)
        self._invlogrng = 0.135 # Arbitrary value
        self._prepared = False
        self._reduction = None # Reduction shader for calculating min/max
        
    def ViewPos(self, x, y):
        '''
        Set the view position of the outputted shader
        '''
        self._x = x
        self._y = y
        
    # Do this when the program is loaded
    def Init(self, display):
        
        if not self._prepared:
            # Set up image 
            self._width, self._height = display.Window().get_size()
            # Set up empty texture to draw to
            #self._texture = glGenTextures(1)
            self._texture = ctypes.c_uint(0)
            glGenTextures(1,self._texture)
            #self._texture = pyglet.image.Texture.create(self._width, self._height, rectangle=True,internalformat=GL_RGBA32F_ARB)
            
            glEnable( GL_TEXTURE_2D )
            glBindTexture( GL_TEXTURE_2D, self._texture )
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            #glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glPixelStorei(GL_UNPACK_ROW_LENGTH, 0)
            glPixelStorei(GL_UNPACK_SKIP_PIXELS, 0)
            glPixelStorei(GL_UNPACK_SKIP_ROWS, 0)
            #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, self._width, self._height, 0,\
            # GL_RGBA, GL_FLOAT, 0)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F_ARB, self._width, self._height, 0,\
             GL_RGBA, GL_FLOAT, 0)
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
            
            glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, 
                                  self._width, self._height)
            glBindRenderbuffer(GL_RENDERBUFFER, 0)
            
            # Attach texture and depth buffer
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self._texture, ctypes.c_int(0))
            glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self._depth)
            
            # Unbind frame buffer for now
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
        
            status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        
            # Create shaders
            self._incShader = Shader("IncrementBuffer")
            self._logShader = Shader("LogBuffer")
            self._reduction = ReductionShader(self._texture, max(self._width,self._height),
                                              ["ReduceMaxMin"])
            
            self._prepared = True
        
        # Pass everything through since we want to make a projected density map
        glEnable( GL_BLEND )
        glBlendFunc( GL_ONE, 
                     GL_ONE )
        
    # Do this before the objects are rendered
    def Begin(self, display):
        
        # Re-bind frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, self._frame)
        
        # Clear frame buffer
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDisable( GL_TEXTURE_2D )
        glDisable(GL_DEPTH_TEST)
        glEnable( GL_BLEND )
        glBlendFunc( GL_ONE, 
                     GL_ONE )
        #self._incShader.Bind()
        # At this point we draw...
        
    # Do this after the objects are rendered
    def End(self, display):
        # Take out the shader currently in use
        #self._incShader.Unbind()
        # Unbind frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        # TEST REDUCTION
        reduce = self._reduction.Run()
        maxval = reduce[0,0]
        minval = reduce[0,1]
        # Get the max/min value in the texture to pass to the shader
        self._recalcMaxMin -= 1
        properScale = self._recalcMaxMin <= 0
        properScale = True
        if properScale:
            #data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGBA, GL_FLOAT)
            #red = data[:,:,0]
            #minval = np.min(red[np.nonzero(red)])
            #maxval = np.max(red)
            if minval == maxval:
                dmin = 0.0
                dmax = 0.0
                invrng = 1.0
            else:
                dmin = float(np.log(minval))
                dmax = float(np.log(maxval))
                #dmin = dmax - 10.0
                try:
                    invrng = 1.0/(dmax-dmin)
                except:
                    invrng = 1.0
            #print "Image min, range, max:", dmin, 1.0/invrng, dmax
            #newrng = np.min([10.0,1.0/invrng]) # HACK - stops weird hard circle effect
            #dmin = dmax - newrng
            #invrng = 1.0/newrng
            dmax = 3.0
            dmin = -3.0
            self._logmin = dmin
            self._invlogrng = invrng
            self._recalcMaxMin = 10
            #print self._logmin, self._invlogrng
            #del(data)
        # HACK
        #data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGBA, GL_FLOAT)
        #import scipy
        #scipy.misc.imsave('outfile.jpg', data)
        # HACK END
    
    def DrawTexture(self):
        logshade = True
        if logshade:
            self._logShader.Bind()
            self._logShader.AddFloat(self._logmin, "texmin")
            self._logShader.AddFloat(self._invlogrng, "texinvrng")
        #shaders.glUseProgram(self._logShader.Shader())
        #minloc = glGetUniformLocation( self._logShader.Shader(), 'texmin' )
        #invrngloc = glGetUniformLocation( self._logShader.Shader(), 'texinvrng' )
        #glUniform1f( minloc,self._logmin)
        #glUniform1f( invrngloc,self._invlogrng)
        #shaders.glUseProgram(0)
        glLoadIdentity()
        glViewport(self._x, self._y, self._width, self._height)
        # Now we need to plot the texture to screen
        # Set up an orthogonal projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 1, 0, 1, -10, 10)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        #glDrawPixels(self._width, self._height, GL_RGBA, GL_FLOAT, self._texture)
        # Now draw the texture with the log shader
        # Draw the texture onto a flat plane
        glColor4f(1.0,1.0,1.0,1.0)
        glEnable( GL_TEXTURE_2D )
        #glDisable(GL_TEXTURE_GEN_S)
        #glDisable(GL_TEXTURE_GEN_T)
        glBindTexture( GL_TEXTURE_2D, self._texture )
        glBegin(GL_TRIANGLES)
        glTexCoord2d(0.0,0.0);        glVertex3f(0.0, 0.0, 0.0);
        glTexCoord2d(1.0,0.0);        glVertex3f(1.0, 0.0, 0.0);
        glTexCoord2d(1.0,1.0);        glVertex3f(1.0, 1.0, 0.0);
        
        glTexCoord2d(1.0,1.0);        glVertex3f(1.0, 1.0, 0.0);
        glTexCoord2d(0.0,1.0);        glVertex3f(0.0, 1.0, 0.0);
        glTexCoord2d(0.0,0.0);        glVertex3f(0.0, 0.0, 0.0);
        glEnd()
        if logshade:
            self._logShader.Unbind()
        glBindTexture( GL_TEXTURE_2D, 0 )
        #glDeleteTextures(self._texture)
        #glDeleteFramebuffers(2,[self._frame,self._depth])
        
if __name__=="__main__":
    import Visualisation
    Visualisation.TestRamses()
