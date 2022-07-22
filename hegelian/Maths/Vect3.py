'''
Created on 5 Sep 2011

@author: samgeen
'''

import numpy as np
import math

# TODO: CHECK NUMPY DOESN'T ALREADY PROVIDE THIS?
class Vect3(object):
    '''
    classdocs
    '''

    def __init__(self, x=0.0, y=0.0, z=0.0):
        '''
        Constructor
        Examples:
           a = Vect3(0,1,2)
        or a = Vect3([0,1,2])
        or a = Vect3(numpy.matrix([0,1,2]))
        or a = Vect3(numpy.array([0,1,2]))
        NOTE: I don't think that using a Vect3 as an input works yet
        '''
        try:
            x[2] # does the input have at least 3 elements?
            # If it does, put it straight into the matrix
            self._v = np.array(x)
            #break
        except:
            # If the input only has one element, input as 3 coordinates
            self._v = np.array([x,y,z])
    
    # Deep copy
    def Copy(self):
        return Vect3(self._v)
    
    def __getitem__(self, index) :
        return self._v[index]
    
    def __setitem__(self, index, value) :
        self._v[index] = value
    
    def __str__(self):
        return str(self._v)
    
    def AsArray(self):
        return self._v

    # Negative of vector (i.e. -v)
    def __neg__(self):
        return Vect3(-self._v)
    
    # Add
    def __add__(self, rhs):
        return Vect3(self._v+rhs._v)
    
    # Subtract
    def __sub__(self, rhs):
        return Vect3(self._v-rhs._v)
    
    # Multiply by scalar, or element-wise multiplication with a vector
    def __mul__(self, rhs):
        return Vect3(self._v*rhs)
    
    # Right-handed multiply by scalar, or element-wise multiplication with a vector
    def __rmul__(self, lhs):
        return Vect3(self._v*lhs)
    
    # Division by a scalar, or element-wise division with a vector
    def __itruediv__(self, rhs):
        return Vect3(self._v/rhs)
    
    # Divide equals by a scalar, or element-wise division with a vector
    def __div__(self, rhs):
        return Vect3(self._v/rhs)
    
    # Length squared (faster than Length)
    def LengthSqrd(self):
        return self._v.dot(self._v)
    
    # Length of vector
    def Length(self):
        return math.sqrt(self._v.dot(self._v))
    
    # Return normal of this vector
    def Normal(self):
        # TODO: Make a fast normal function?
        return Vect3(self._v / self.Length())
    
    # Dot product operator (modulus sign: d = a % b)
    def __mod__(self, rhs):
        return Vect3(self._v.dot(rhs._v))
        
    # Dot product direct function
    def DotProduct(self, v2):
        return Vect3(self._v.dot(v2._v))
    
    # Cross product (hat/xor symbol: c = a ^ b)
    def __xor__(self, rhs):
        return Vect3(np.cross(self._v,rhs._v))
    
    # Cross product direct function
    def CrossProduct(self, rhs):
        return Vect3(np.cross(self._v,rhs._v))
        
    # Find an (arbitrary) vector perpendicular to this one
    def Perpendicular(self):
        if self._v[1]==0 and self._v[2]==0:
            return self ^ (self + Vect3(0,1,0))
        return Vect3(self ^ (self + Vect3(1,0,0)))
