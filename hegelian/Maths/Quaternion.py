'''
Created on 27 Sep 2011

@author: samgeen

NOTE: Basic arithmetic code taken from "curvedinfinity" at 
      http://ubuntuforums.org/showthread.php?t=1037392
'''

import math, sys, os
import numpy as np
from .Vect3 import Vect3

class Quaternion(object):
    '''
    classdocs
    '''

    def __init__(self, a=np.array([1.0,0.0,0.0,0.0]),vector=1):
        '''
        Constructor
        EXPLANATION!
        EITHER you can make a quaternion it directly with a 4-vector 'a'
        OR you can make it a rotation about the 3-vector 'vector' with angle 'a'
        Examples:
           q = Quaternion([0,1,2,3])
        or q = Quaternion(math.pi/2.0,[0,1,2])
        NOTE! The latter will NOT give you a quaternion angle + xi + yj + zk - see code!
        '''
        # Use exceptions to try setting an angle, and if that fails, use direct setting
        try:
            a[3] # is 'a' a 4-vector (continue) or an angle (jump to 'except') 
            self._q = np.array([a[0],a[1],a[2],a[3]])
        except:
            try:
                a[2] # is 'a' a 3-vector (continue) or an angle (jump to 'except')
                self._q = np.array([0.0,a[0],a[1],a[2]])
            except:
                # Rotation quaternion is (cos(a/2),x*sin(a/2),y*sin(a/2),z*sin(a/2))
                # where x,y,z are a normal vector
                a *= 0.5
                x,y,z = vector[0], vector[1], vector[2]
                s = math.sin(a)/math.sqrt(x*x+y*y+z*z)
                # Note! Normalisation not necessary here, but check just in case...
                self._q = np.array([math.cos(a),x*s,y*s,z*s])
    
    # Get an individual item of the quaternion
    def __getitem__(self, item):
        return self._q[item]
    
    # Return as string
    def __str__(self):
        return str(self._q[0])+" + " + \
               str(self._q[1])+"i + "+ \
               str(self._q[2])+"j + "+ \
               str(self._q[3])+"k "
                
    # Deep copy
    def Copy(self):
        return (self._q[0],self._q[1],self._q[2],self._q[3])
    
    # Add
    def __add__(self, rhs):
        return Quaternion(self._q+rhs._q)
    
    # Subtract
    def __sub__(self, rhs):
        return Quaternion(self._q-rhs._q)
        
    # Multiply (chooses scalar or Quaternion)
    def __mul__(self, rhs):
        if not isinstance(rhs,Quaternion):
            return Quaternion(self._q*rhs)
        else:
            # TODO: Reparse to save the intermediate copy?
            w1,x1,y1,z1 = self._q[0],self._q[1],self._q[2],self._q[3]
            w2,x2,y2,z2 = rhs._q[0],rhs._q[1],rhs._q[2],rhs._q[3]
            return Quaternion([w1*w2 - x1*x2 - y1*y2 - z1*z2,
                    w1*x2 + x1*w2 + y1*z2 - z1*y2,
                    w1*y2 + y1*w2 + z1*x2 - x1*z2,
                    w1*z2 + z1*w2 + x1*y2 - y1*x2])  
    
    # Right multiplication, for pre-multiplication (chooses scalar or Quaternion)
    def __rmul__(self, lhs):
        if not isinstance(lhs,Quaternion):
            return Quaternion(self._q*lhs)
        else:
            # TODO: Reparse to save the intermediate copy
            w1,x1,y1,z1 = self._q[0],self._q[1],self._q[2],self._q[3]
            w2,x2,y2,z2 = lhs._q[0],lhs._q[1],lhs._q[2],lhs._q[3]
            return Quaternion([w1*w2 - x1*x2 - y1*y2 - z1*z2,
                    w1*x2 + x1*w2 + y1*z2 - z1*y2,
                    w1*y2 + y1*w2 + z1*x2 - x1*z2,
                    w1*z2 + z1*w2 + x1*y2 - y1*x2]) 

    # Scalar division
    def __div__(self, rhs):
        return Quaternion(self._q / rhs)
    
    # Magnitude
    def Magnitude(self):
        return np.sqrt(np.vdot(self._q,self._q))
    
    # Magnitude squared (no sqrt, so faster)
    def MagnitudeSqrd(self):
        return np.vdot(self._q,self._q)
    
    # Return normalised quaternion 
    def Normal(self):
        return self._q / self.Magnitude()
    
    # Conjugate
    def Conjugate(self):
        return Quaternion([self._q[0], -self._q[1], -self._q[2], -self._q[3]])

    # Inverse
    def Inverse(self):
        return self.Conjugate() / self.MagnitudeSqrd()
    
    # Dot product (% operator)
    def __mod__(self, rhs):
        return np.vdot(self._q,rhs._q)

    # Dot product (explicit call)
    def DotProduct(self, rhs):
        return np.vdot(self._q,rhs._q)
    
    # Rotate a vector using this quaternion 
    def RotateVector(self, vector):
        qw, qx, qy, qz = self._q[0], self._q[1], self._q[2], self._q[3]
        x, y, z = vector[0], vector[1], vector[2]
        
        ww = qw*qw
        xx = qx*qx
        yy = qy*qy
        zz = qz*qz
        wx = qw*qx
        wy = qw*qy
        wz = qw*qz
        xy = qx*qy
        xz = qx*qz
        yz = qy*qz
        
        return Vect3([ww*x + xx*x - yy*x - zz*x + 2*((xy-wz)*y + (xz+wy)*z),
                ww*y - xx*y + yy*y - zz*y + 2*((xy+wz)*x + (yz-wx)*z),
                ww*z - xx*z - yy*z + zz*z + 2*((xz-wy)*x + (yz+wx)*y)])

    # Returns the quaternion as a matrix transform
    def AsMatrix(self):
        w,x,y,z = self._q[0], self._q[1], self._q[2], self._q[3]
        xx = 2.0*x*x
        yy = 2.0*y*y
        zz = 2.0*z*z
        xy = 2.0*x*y
        zw = 2.0*z*w
        xz = 2.0*x*z
        yw = 2.0*y*w
        yz = 2.0*y*z
        xw = 2.0*x*w
        return np.matrix([[1.0-yy-zz, xy-zw, xz+yw, 0.0],
                 [xy+zw, 1.0-xx-zz, yz-xw, 0.0],
                 [xz-yw, yz+xw, 1.0-xx-yy, 0.0],
                 [0.0, 0.0, 0.0, 1.0]])
    
    # Returns the Quaternion's imaginary elements as a vector (for unpacking rotations as vectors)
    def AsVect3(self):
        return Vect3([self._q[1],self._q[2],self._q[3]])    
    
    # Interpolate between two quaternions (e.g. for interpolating rotations)
    # factor: 0 = self, 1 = q2, 0-1 = in-between
    def Interpolate(self, q2, factor, shortest=True):
        ca = self.DotProduct(q2)
        if shortest and ca<0:
            ca = -ca
            neg_q2 = True
        else:
            neg_q2 = False
        o = math.acos(ca)
        so = math.sin(o)
    
        if (abs(so)<=1E-12):
            return self.Copy()
    
        a = math.sin(o*(1.0-factor)) / so
        b = math.sin(o*factor) / so
        if neg_q2:
            return (self._q*a) - (q2*b)
        else:
            return (self._q*a) + (q2*b)
        
# Utility function that returns a quaternion with a given input
# Rotates by "angle" about "vector"
def Rotation(angle, vector):
    return Quaternion(angle, vector)