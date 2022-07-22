'''
Created on Oct 23, 2012

@author: samgeen
'''

import os, sys
import collections
import ctypes

'''
PygletShader OBJECT TAKEN FROM 
http://swiftcoder.wordpress.com/2008/12/19/simple-glsl-wrapper-for-pyglet/
ADDED UNDERSCORES TO MAKE NOMENCLATURE EASIER
USE Shader OBJECT FOR CLEANER INTERFACE; USES PygletShader TO WORK
Uses https://github.com/leovt/leovt/blob/master/framebuffer.py to update to Python 3
'''
#
# Copyright Tristam Macdonald 2008.
#
# Distributed under the Boost Software License, Version 1.0
# (see http://www.boost.org/LICENSE_1_0.txt)
#
 
# This is sort of OK because everything begins with GL already
# OpenGL predates a lot of modern coding practices huh
from pyglet.gl import *
 
class PygletShader:
    # vert, frag and geom take arrays of source strings
    # the arrays will be concattenated into one string by OpenGL
    def __init__(self, vert = [], frag = [], geom = []):
        # TESTING - Check OpenGL context
        #context = pyglet.gl.current_context
        #config = context.config
        #print("CONTEXT CONFIG", config)
        # create the program handle
        self.handle = glCreateProgram()
        # we are not linked yet
        self.linked = False
 
        # create the vertex shader
        self._createShader(vert, GL_VERTEX_SHADER)
        # create the fragment shader
        self._createShader(frag, GL_FRAGMENT_SHADER)
        # the geometry shader will be the same, once pyglet supports the extension
        # self.createShader(frag, GL_GEOMETRY_SHADER_EXT)
 
        # attempt to link the program
        self._link()
 
    def _createShader(self, strings, shaderType):
        # if we have no source code, ignore this shader
        if len(strings) < 1:
            return
        # Parse shader code into one string rather than a list of lines
        shadercode = ""
        for string in strings:
            if "//" in string:
                string = string[:string.find("//")]
            shadercode += string+" "
        # Encode string for Python 3
        shadercode = shadercode.encode(encoding='UTF-8')
        # Submit shader as one string rather than a set
        count = 1 
 
        print("SHADER", shadercode)

        # create the shader handle
        shader = glCreateShader(shaderType)
 
        # convert the source strings into a ctypes pointer-to-char array, and upload them
        # this is somewhat magic
        srcBuffer = ctypes.create_string_buffer(shadercode)
        buffer = ctypes.cast(ctypes.pointer(ctypes.pointer(srcBuffer)), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
        length = ctypes.c_int(len(shadercode) + 1)
        glShaderSource(shader, count, buffer, ctypes.byref(length))
 
        # compile the shader
        glCompileShader(shader)
 
        temp = ctypes.c_int(0)
        # retrieve the compile status
        glGetShaderiv(shader, GL_COMPILE_STATUS, ctypes.byref(temp))
 
        # if compilation failed, print the log
        if not temp:
            # retrieve the log length
            glGetShaderiv(shader, GL_INFO_LOG_LENGTH, ctypes.byref(temp))
            # create a buffer for the log
            buffer = ctypes.create_string_buffer(temp.value)
            # retrieve the log text
            glGetShaderInfoLog(shader, temp, None, buffer)
            # print the log to the console
            if shaderType == GL_FRAGMENT_SHADER:
                print("(Fragment shader)")
            if shaderType == GL_VERTEX_SHADER:
                print("(Vertex shader)")
            print("BUFFER VALUE", buffer.value)
        else:
            # all is well, so attach the shader to the program
            glAttachShader(self.handle, shader);
 
    def _link(self):
        # link the program
        glLinkProgram(self.handle)
 
        temp = ctypes.c_int(0)
        # retrieve the link status
        glGetProgramiv(self.handle, GL_LINK_STATUS, ctypes.byref(temp))
 
        # if linking failed, print the log
        if not temp:
            #   retrieve the log length
            glGetProgramiv(self.handle, GL_INFO_LOG_LENGTH, ctypes.byref(temp))
            # create a buffer for the log
            buffer = ctypes.create_string_buffer(temp.value)
            # retrieve the log text
            glGetProgramInfoLog(self.handle, temp, None, buffer)
            # print the log to the console
            print("BUFFER VALUE", buffer.value)
        else:
            # all is well, so we are linked
            self.linked = True
 
    def bind(self):
        # bind the program
        glUseProgram(self.handle)
 
    def unbind(self):
        # unbind whatever program is currently bound - not necessarily this program,
        # so this should probably be a class method instead
        glUseProgram(0)
 
    # upload a floating point uniform
    # this program must be currently bound
    def uniformf(self, name, *vals):
        # Fix name to work with Python 3 string encoding
        name = name.encode(encoding='UTF-8')
        # check there are 1-4 values
        if len(vals) in range(1, 5):
            # select the correct function
            { 1 : glUniform1f,
                2 : glUniform2f,
                3 : glUniform3f,
                4 : glUniform4f
                # retrieve the uniform location, and set
            }[len(vals)](glGetUniformLocation(self.handle, name), *vals)
 
    # upload an integer uniform
    # this program must be currently bound
    def uniformi(self, name, *vals):
        # Fix name to work with Python 3 string encoding
        name = str.encode(name)
        # check there are 1-4 values
        if len(vals) in range(1, 5):
            # select the correct function
            { 1 : glUniform1i,
                2 : glUniform2i,
                3 : glUniform3i,
                4 : glUniform4i
                # retrieve the uniform location, and set
            }[len(vals)](glGetUniformLocation(self.handle, name), *vals)
 
    # upload a uniform matrix
    # works with matrices stored as lists,
    # as well as euclid matrices
    def uniform_matrixf(self, name, mat):
        # Fix name to work with Python 3 string encoding
        name = str.encode(name)
        # obtian the uniform location
        loc = glGetUniformLocation(self.Handle, name)
        # uplaod the 4x4 floating point matrix
        glUniformMatrix4fv(loc, 1, False, (c_float * 16)(*mat))

class Shader(object):
    '''
    A wrapper class around a shader, including a vertex and a fragment shader pair
    '''
    def __init__(self, frag, vert="",geom=""):
        '''
        frag: name of fragment shader, where file is "Shaders/"+frag+".frag"
        vert: name of vertex   shader, where file is "Shaders/"+vert+".vert"
        NOTE: GEOMETRY SHADERS CURRENTLY NOT WORKING IF THAT'S WHAT YOU EXPECT TO HAPPEN
        '''
        print("Name: ", frag)
        
        # If no vertex shader name included, assume it has the same name as frag
        if len(vert) == 0:
            vert = frag
        if len(geom) == 0:
            geom = frag
        # Read shader files
        here = __file__[0:__file__.rfind(os.sep)] # TODO: Find solution to this that isn't dark magic
        fragname = here+"/Shaders/"+frag+".frag"
        geomname = here+"/Shaders/"+geom+".geom"
        vertname = here+"/Shaders/"+vert+".vert"
        frag = self._ReadShader(fragname)
        vert = self._ReadShader(vertname)
        self._pshader = PygletShader(vert.split("\n"),frag.split("\n"))
        self._attributes = dict()
        
        # Compile shaders
        '''
        vertexShader = shaders.compileShader(vert, GL_VERTEX_SHADER)
        fragmentShader = shaders.compileShader(frag, GL_FRAGMENT_SHADER)    
        # Add geometry shader?
        if os.path.isfile(geomname):
            geom = self._ReadShader(geomname)
            geometryShader = shaders.compileShader(geom, GL_GEOMETRY_SHADER)
            self.shader = shaders.compileProgram(fragmentShader, geometryShader, vertexShader)
        else:
            self.shader = shaders.compileProgram(fragmentShader, vertexShader)
        '''
    
    def Bind(self):
        self._pshader.bind()
        for attribute in self._attributes.values():
            glEnableVertexAttribArray(attribute)
        
    def Unbind(self):
        for attribute in self._attributes.values():
            glDisableVertexAttribArray(attribute)
        self._pshader.unbind()
        
    #def Shader(self):
    #    return self.shader
    
    def AddAttribute(self, name):
        '''
        Add an attribute
        '''
        loc = glGetAttribLocation( self._pshader.handle, name)
        print(loc, "LOC")
        self._attributes[name] = loc
        
    def FindAttribute(self, name):
        return self._attributes[name]
    
    def AddVariable(self, var, name, vartype):
        '''
        Add a generic variable to the shader (useful for weird OpenGL number types)
        NOTE - FOR MATRICES, USE AddMatrix !!
        var - The variable to use
        name - The name of the variable
        vartype - The type of variable to use (e.g. "1f" or "3uv")
        TODO: UNBREAK THIS
        '''
        # This works the same as the PygletShader implementation, so use this
        varloc = glGetUniformLocation( self._pshader.handle, name )
        exec("glUniform"+vartype+"( varloc , *var )")
        
    def AddFloat(self, var, name):
        '''
        Add a float variable to the shader (of any sized list)
        var - The variable to use (can be a list of floats)
        name - The name of the variable
        '''
        if isinstance(var, collections.Iterable):
            self._pshader.uniformf(name, *var)
        else:
            self._pshader.uniformf(name, var)
        
    def AddInt(self, var, name):
        '''
        Add an int variable to the shader (of any sized list)
        var - The variable to use (can be a list of ints)
        name - The name of the variable
        '''
        self._pshader.uniformi(name, var)
        
    def AddMatrix(self, matrix, name):
        '''
        Add a matrix object to the shader
        matrix - matrix to use **MUST BE A FLOAT MATRIX!!**
        name - Name of the matrix to use inside the shader
        '''
        self._pshader.uniform_matrixf(name, matrix)
    
    def _ReadShader(self, filename):
        f = open(filename,"r")
        data = f.read()
        f.close()
        return data
