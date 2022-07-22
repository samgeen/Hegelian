'''
Created on Nov 6, 2012

@author: samgeen
'''

import Fluids.GaussianImage
import numpy as np
#from OpenGL.GL import *
from pyglet.gl import *
from pyglet.gl.glu import *
from ctypes import *
import Shader
# Vect3 object
from Maths.Vect3 import Vect3

_texture = -1
        
def _MakeTexture():
    
    global _texture
    if _texture < 0:
        # Make the billboarding texture
        texSize = 128
        im = Fluids.GaussianImage.GaussianImage(texSize,alpha=True)
        print im.max(), im.min(), im[im > 0.0].min()
        #im *= 255.0
        #im = im.astype(np.uint8)
        # Output image to debug?
        debug = False
        if debug:
            from PIL import Image
            res = Image.fromarray(im)
            res.save("testgaussian.jpg")
        im = im.flatten()
        #im = im*0.0 + 1.0
        print im.max(), im.min(), im[im > 0.0].min(), "IMRNG"
        im = (GLfloat * len(im))(*im)
        _texture = c_uint(0)
        glGenTextures(1,_texture)
        glEnable( GL_TEXTURE_2D )
        glBindTexture( GL_TEXTURE_2D, _texture )
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        #glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        #glPixelStorei(GL_UNPACK_ROW_LENGTH, 0)
        #glPixelStorei(GL_UNPACK_SKIP_PIXELS, 0)
        #glPixelStorei(GL_UNPACK_SKIP_ROWS, 0)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F_ARB, texSize, texSize, 0,\
             GL_RGBA, GL_FLOAT, im)
    return _texture

class BillboardDrawable(object):
    '''
    A simple billboarded point cloud object
    Algorithm - Pass to shader: 
    - point - float 3x3xN
    - a 0,1,2 unsigned byte telling us the corner - bytex3xN
    - a size array - 
    - a billboard texture - byte 1ximagesize
    - the modelview matrix (or something) - float*16
    '''
    def __init__(self,points,sizes,mass):
        '''
        Constructor
        '''
        self._window = 0
        self._first = True
        self._sizes = np.array(sizes)
        self._points = points
        self._pointmasses = mass
        self._pointsGL = None
        self._cornerX = None
        self._cornerY = None
        self._shader = Shader.Shader("Billboard")
        self._texture = 0
        
    def _Setup(self):
        '''
        Setup the object (refactor the points, etc)
        '''
        # Construct equilateral triangles from the points
        # Triple up each array since we plot each point 3 times for each corner of the triangle
        points = np.kron(self._points,np.ones((3,1)))
        sizes = np.kron(self._sizes,np.ones((3))).flatten()
        masses = np.kron(self._pointmasses,np.ones((3))).flatten()
        print np.min(sizes), np.max(sizes), "MINMAX SIZES"
        if sizes.min() == sizes.max() and sizes.max() == 0.0:
            sizes *= 0.0
            sizes += 1.0
        masses *= sizes**(-2.0) # Get the particle colour density
        masses /= np.max(masses)
        #masses *= 0.0
        #masses += 1.0
        masses = masses.astype("float32")
        #masses = (masses - np.min(masses))/(np.max(masses)-np.min(masses)).astype("float32")
        # Correct sizes to fit numrsph SPH radii inside 
        # The distance from the centre of an equliateral triangle to the edge is 1/(2sqrt3), so divide by that
        numrsph = 2
        sqrt3 = np.sqrt(3.0)
        fudge = 3.0
        triscale = numrsph*2.0*sqrt3 * fudge
        sizes *= triscale
        centre = np.array([3.0,sqrt3])/6.0
        triangle0 = np.array([0.0,0.0]) - centre
        triangle1 = np.array([0.5,0.5*sqrt3]) - centre
        triangle2 = np.array([1.0,0.0]) - centre
        self._cornerX = np.array([triangle0[0],triangle1[0],triangle2[0]],dtype=GLfloat)
        self._cornerY = np.array([triangle0[1],triangle1[1],triangle2[1]],dtype=GLfloat)
        #self._cornerX = [c_float(triangle0[0]),c_float(triangle1[0]),c_float(triangle2[0])]
        #self._cornerY = [c_float(triangle0[1]),c_float(triangle1[1]),c_float(triangle2[1])]
        # Note to self - e.g. arr[1::5] selects every 5th element starting at arr[1]
        #points[0::3] += (triangle0.T*sizes).T
        #points[1::3] += (triangle1.T*sizes).T
        #points[2::3] += (triangle2.T*sizes).T
        # Now slice the arrays to create the vertices
        flat = points.flatten()
        self._pointsGL = (GLfloat * len(flat))(*flat)
        # Make array of which corner of the triangles we're looking at
        corners = np.array([0,1,2])
        cornerIndices = np.kron(corners,np.ones((len(flat)/9,1))).flatten().astype("float32")
        cornerIndices = (GLfloat * len(cornerIndices))(*cornerIndices)
         # Texture coords are triangle corners in a flat list
        texCoords = np.array([0.0,0.0,0.5,0.5*sqrt3,1.0,0.0])
        # Scale coordinates to fit triangle
        X0 = 0.5 - sqrt3/6.0
        X1 = 0.5 + sqrt3/6.0
        Y0 = 0
        Y1 = sqrt3/3.0
        texCoords[0::2] -= X0
        texCoords[0::2] /= X1 - X0
        texCoords[1::2] -= Y0
        texCoords[1::2] /= Y1 - Y0
        texCoords = np.kron(texCoords,np.ones((len(flat)/9,1))).flatten().astype("float32")
        sizes = (GLfloat * len(sizes))(*sizes)
        masses = (GLfloat * len(masses))(*masses)
        texCoords = (GLfloat * len(texCoords))(*texCoords)
        # Don't need these none no more
        self._points = None
        self._texture = _MakeTexture()
        # Set up OpenGL gubbins
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        self._shader._pshader.bind()
        self._shader.AddAttribute("size")
        loc = self._shader.FindAttribute("size")
        glVertexAttribPointer(loc,1,GL_FLOAT,False,0,sizes)
        self._shader.AddAttribute("mass")
        loc = self._shader.FindAttribute("mass")
        glVertexAttribPointer(loc,1,GL_FLOAT,False,0,masses)
        self._shader.AddAttribute("cornerIndex")
        loc = self._shader.FindAttribute("cornerIndex")
        glVertexAttribPointer(loc,1,GL_FLOAT,False,0,cornerIndices)
        #tval = 0
        #self._shader.AddInt(tval,"texture")
        self._shader.AddFloat(self._cornerX, "cornerX")
        self._shader.AddFloat(self._cornerY, "cornerY")
        self._shader.Unbind() 
        glEnable( GL_TEXTURE_2D )
        glVertexPointer(3, GL_FLOAT, 0, self._pointsGL)
        glTexCoordPointer(2, GL_FLOAT, 0, texCoords)
        # DUN
        self._first = False
        
        #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texSize, texSize, 0, GL_RGBA, 
        #         GL_UNSIGNED_BYTE, im);
        glBindTexture(GL_TEXTURE_2D, 0)
        
    # Draw the points to screen
    def Draw(self, window):
        '''
        Draw object
        '''
        self._window = window
        
        # First time through?
        # NOTE: I have no idea how reliable this code is at determining whether we set these things
        if self._first:
            self._Setup()
        
        glColor4f(1.,1.,1.,1.)
        
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self._texture)
        self._shader.Bind()
        glDrawArrays(GL_TRIANGLES, 0, len(self._pointsGL) // 3)
        self._shader.Unbind() 
        glBindTexture(GL_TEXTURE_2D, 0)
        #glDisable(GL_TEXTURE_2D)
        #glBegin(GL_POINTS)
        #for it in self._points:
        #    glVertex3f(it[0],it[1],it[2])
        #glEnd()
        # DIAGNOSTIC PRINT
        #print "Number points shown:", len(self._pointsGL) // 3

class OldBillboardDrawable(object):
    '''
    Draws billboarded particles to screen based on particle size
    '''


    def __init__(self, pointCloud):
        '''
        Constructor
        '''
        self._viewport = 0
        
    # Native methods
    def AddPoints(self, newPoints):
        if self.Size() == 0:
            self._points = newPoints.copy()
        else:
            self._points = np.hstack((self._points,newPoints))
        self._MakeBillboardSizes()
        
    def Preload(self):
        '''
        Preload object into graphics memory
        '''
        self._displayList = glGenLists(1)
        glNewList(self._displayList,GL_COMPILE) 
        
        glBegin(GL_POINTS)
        for it in self._points:
            glVertex3fv(it)
        glEnd()
        
        self._preloaded = True
        
        glEndList()
        
    def Preloaded(self):
        return self._preloaded
        
    def Draw(self, viewport):
        '''
        Draw object (must be preloaded!)
        '''
        self._viewport = viewport
        if (not self.Preloaded()):
            self.Preload()
        glColor4f(1.0,1.0,1.0,self._alpha)
        #print self.__displayList
        glCallList(self._displayList)
        
    def _MakeBillboardSizes(self):
        raise NotImplementedError
    
    
# OLD SETUP CODE
'''

    def _Setup(self):
        # Construct equilateral triangles from the points
        points = np.kron(self._points,np.ones((3,1)))
        sizes = self._sizes
        sqrt3 = np.sqrt(3.0)
        centre = np.array([[3.0,sqrt3,0.0]])/6.0
        triangle0 = np.array([[0.0,0.0,0.0]]) - centre
        triangle1 = np.array([[0.5,0.5*sqrt3,0.0]]) - centre
        triangle2 = np.array([[1.0,0.0,0.0]]) - centre
        # Note to self - e.g. arr[1::5] selects every 5th element starting at arr[1]
        points[0::3] += (triangle0.T*sizes).T
        points[1::3] += (triangle1.T*sizes).T
        points[2::3] += (triangle2.T*sizes).T
        # Now slice the arrays to create the vertices
        flat = points.flatten()
        self._pointsGL = (GLfloat * len(flat))(*flat)
        # Make array of which corner of the triangles we're looking at
        corners = np.array([0,1,2],dtype=np.ubyte)
        self._cornerIndices = np.kron(corners,np.ones((len(flat)/3,1))).flatten()
        # Make the texture coordiate array
        self._texcoords = np.array([triangle0[0:1],triangle1[0:1],triangle2[0:1]]).flatten()
        self._texcoords = np.kron(self._texcoords,np.ones((len(flat)/3,1))).flatten()
        # Don't need these none no more
        self._points = None
        # Set up OpenGL gubbins
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self._pointsGL)
        glTexCoordPointer( 2, GL_FLOAT, 0, self._texcoords)
        self._shader.AddFloat(triangle0, "corner0")
        self._shader.AddFloat(triangle1, "corner1")
        self._shader.AddFloat(triangle2, "corner2")
        # DUN
        self._first = False
'''
        