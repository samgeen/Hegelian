'''
Created on Oct 23, 2012

@author: samgeen
BASED ON CODE FROM http://www.lcg.ufrj.br/Cursos/GPUProg/GPGPU_Reductions
'''
import math
import numpy as np

#from OpenGL.GL import *
#from OpenGL.GLU import *
#from OpenGL.GLUT import *
#from OpenGL.GL.ARB.framebuffer_object import *
#from OpenGL.GL.ARB.texture_float import *

from pyglet.gl import *

from Shader import Shader

from ctypes import *

class ReductionLevel(object):
    '''
    Wrapper class around one level of the reduction; used by ReductionShader
    '''
    
    def __init__(self, texture, size, nextTexture, quadList):
        '''
        Constructor
        level of reduction
        '''
        self._size = int(size)
        self._dt = 0.5 / float(self._size)
        self._texture = texture
        self._nextTexture = nextTexture
        self._quadList = quadList
        
    def Reduce(self, shader):
        size = self._size
    
        # attach texture to the FBO     
        glFramebufferTexture2D(GL_FRAMEBUFFER,  
                      GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self._nextTexture,0)
        glDrawBuffer(GL_COLOR_ATTACHMENT0) 
        
        glViewport(0, 0, size/2, size/2)
        
        shader.AddFloat(self._dt, "dt")
        #glActiveTexture(0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self._texture)
        glCallList(self._quadList) # call to gl list   
        glBindTexture(GL_TEXTURE_2D, self._nextTexture) 
        # TODO: FIGURE OUT WHY THIS *ALMOST* FINDS THE MAX BUT NOT QUITE...
        #data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGBA, GL_FLOAT)
        #red = data[:,:,0]
        #print self._texture, self._nextTexture, size, np.min(red), np.max(red)
        #import scipy
        #scipy.misc.imsave('outfile'+str(size)+'.jpg', red)


class ReductionShader(object):
    '''
    Reduces a texture in video memory to find the min/max of the texture
    Allows the passing in of multiple fragment shaders 
    (e.g. a max shader and a min shader)
    '''

    def __init__(self, textureID, length, fragShaderNames):
        '''
        Constructor
        texture - a texture object to reduce on TODO: OR A FBO???
        fragShaderNames - an iterable container of fragment shader names to reduce on
        '''
        # Set up input texture
        self._inputID = textureID
        self._length = length
        # Set up maximum buffer level (one below level of texture, where length = 2^level)
        self._bufferLevel = int(math.log(length,2))
        # Set up shaders
        self._shaders = list()
        for frag in fragShaderNames:
            self._shaders.append(Shader(frag,"DoNothing"))
        self._outputs = np.zeros((len(self._shaders),2))
        # Generates a FBO handler
        self._frameBuffer = c_uint(0)
        glGenFramebuffers(1, self._frameBuffer)
        # Make quad display list to draw to
        self._quadList = glGenLists(1)
        # Levels to use (leave empty for now)
        self._levels = None
        # Initialise (yes, I know, functional code in a constructor)
        self._Init()
        
    def _Init(self):
        '''
        Initialise buffers
        '''
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        
        # Set up quad to draw to
        sz = 1.0#self._length
        glNewList(self._quadList, GL_COMPILE)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0) 
        glVertex3f( 0.0, 0.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sz, 0.0, 0.0)
        glTexCoord2f(1.0, 1.0) 
        glVertex3f(sz, sz, 0.0)
        glTexCoord2f(0.0, 1.0) 
        glVertex3f(0.0, sz, 0.0)
        glEnd()      
        glEndList()
        
        # Initialise the reduction textures
        self._InitTextures()
    
    def Run(self):
        '''
        Run the reduction and return a numpy array of values for each fragment shader
        '''
        iout = 0
        for shader in self._shaders:
            self._outputs[iout,:] = self._RunShader(shader)
            iout += 1
        return self._outputs
    
    def _RunShader(self, shader):
        '''
        Run a fragment shader to reduce the texture and return a value
        '''
        
        # enable the FBO     
        # HACK - ASSUME THAT THE PROJECTION IS GOOD 
        '''
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        '''
        
        glEnable(GL_TEXTURE_2D)
        
        shader.Bind()
        
        # Enable the FBO to render to texture
        glBindFramebuffer(GL_FRAMEBUFFER,self._frameBuffer)
        for level in self._levels:
            level.Reduce(shader)
        glBindFramebuffer(GL_FRAMEBUFFER,0)
        
        size = int(self._length / math.pow(2,0))
        data = (c_float * 4)(0)
        glGetTexImage(GL_TEXTURE_2D, 0, GL_RGBA, GL_FLOAT, data)
        
        output = np.array([data[0],data[3]])
        
        # disable the FBO
        glBindFramebuffer(GL_FRAMEBUFFER,0)   
        shader.Unbind()
        
        
        # TODO: DON'T JUST DO MAX VALUE
        # TODO: WORK OUT WHY LAST REDUCTION DOESN'T WORK??
        return output

    def _InitTextures(self):
        '''
        Initialises all textures 
        '''
        BUFFER_LEVEL = self._bufferLevel
        BUFFER_RESOLUTION = self._length
        self._levels = list()
        
        # Creates a new textures group 
        tex = (c_uint * (BUFFER_LEVEL + 1))(0)
        glGenTextures(BUFFER_LEVEL + 1, tex)
        tex[0] = self._inputID
        
        # Make lower-resolution texture images
        for i in range(0,BUFFER_LEVEL+1):
            # Set up level object
            size = int(BUFFER_RESOLUTION / math.pow(2,i))
            # (Note: Don't reduce the last, 1x1 texture...)
            if i < BUFFER_LEVEL:
                self._levels.append(ReductionLevel(tex[i],size,tex[i+1],self._quadList))
            if i > 0:
                # Set up texture
                glBindTexture(GL_TEXTURE_2D, tex[i])
                # Set texture parameters
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)  
                # Define texture with floating point format
                glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA32F,size, size,0,GL_RGBA,GL_FLOAT,0)

if __name__=="__main__":
    import Visualisation
    Visualisation.GadgetTest()