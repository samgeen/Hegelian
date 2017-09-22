'''
Created on 5 Sep 2011

@author: samgeen
'''

import numpy as np
from OpenGL.GL import *
from Octree import AbstractTreeData
from PointRendererFactory import PointRendererFactory

# Maximum point cloud size before a split event (experiment with this...)
MAXSIZE = 10000
INVMAXSIZE = 1.0/MAXSIZE

class PointCloud(AbstractTreeData):
    '''
    Point cloud; designed to be inserted into an Octree object
    '''

    def __init__(self, weight=1.0, renderMode="PointRendererSimple"):
        '''
        Constructor
        '''
        # Point list (start empty)
        self._points = np.array([])
        # Point sizes (e.g. SPH smoothing kernel length)
        self._pointSizes = np.array([])
        # Display list (loads points into graphics memory)
        self._displayList = GLuint()
        # Has the object been loaded into graphics memory?
        self._preloaded = False
        # Position and radius of cloud (3-vector when set; since no points are preloaded, set to 0)
        self._position = 0#np.zeros((3))
        self._radius = 0.0
        # Weight of cloud (used to weight points in "smeared" clouds more highly)
        self._weight = weight
        self._alpha = INVMAXSIZE*self._weight*100
        # Make the point renderer
        factory = PointRendererFactory()
        self._renderer = factory.MakeRenderer(renderMode)
        
    # Copy function (lower case for compatibility)
    # ACCESSES PRIVATE MEMBERS OF THE COPY; THIS MIMICKS THE C++ COPY CONSTRUCTOR PATTERN
    def copy(self):
        cp = PointCloud()
        cp._points = self._points.copy()
        cp._pointSizes = self._pointSizes.copy()
        cp._displayList = self._displayList
        cp._preloaded = self._preloaded
        cp._weight = self._weight
        return cp
    
    # Number of points in list
    def Size(self):
        return self._points.size / 3
        
    # AbstractTreeData Methods
    # Split into eight for refining the tree
    def Split(self):
        p = self._points
        s = self._pointSizes
        print "Lengths:", len(p), len(s)
        if len(p) != len(s):
            raise ValueError
        # Find the midpoint of the point data
        mid = self._MidPoint()
        # Make empty objects
        spl = np.array([[[PointCloud(), PointCloud()],[PointCloud(), PointCloud()]],\
               [[PointCloud(), PointCloud()],[PointCloud(), PointCloud()]]])
        # Pre-compute point-cloud splits in each direction (u = up, d = down)
        # This returns truth values in an array of size p
        ux = p[:,0] <  mid[0]; uy = p[:,1] <  mid[1]; uz = p[:,2] <  mid[2];
        dx = p[:,0] >= mid[0]; dy = p[:,1] >= mid[1]; dz = p[:,2] >= mid[2];
        # Make the split
        spl[0,0,0].AddPoints(p[dx * dy * dz,:],s[dx * dy * dz,:])
        spl[1,0,0].AddPoints(p[ux * dy * dz,:],s[ux * dy * dz,:])
        spl[0,1,0].AddPoints(p[dx * uy * dz,:],s[dx * uy * dz,:])
        spl[1,1,0].AddPoints(p[ux * uy * dz,:],s[ux * uy * dz,:])
        spl[0,0,1].AddPoints(p[dx * dy * uz,:],s[dx * dy * uz,:])
        spl[1,0,1].AddPoints(p[ux * dy * uz,:],s[ux * dy * uz,:])
        spl[0,1,1].AddPoints(p[dx * uy * uz,:],s[dx * uy * uz,:])
        spl[1,1,1].AddPoints(p[ux * uy * uz,:],s[ux * uy * uz,:])
        return spl
            
    # Smear out the existing data to a low-res form
    # TODO: ENSURE THAT ALPHA VALUE / WHATEVER STAYS THE SAME; WEIGHT THESE POINTS HIGHER SOMEHOW
    def Smear(self): 
        num = 10
        p = self._points
        s = self._pointSizes
        smear = PointCloud((self._weight*self.Size())/num)
        # Return a point cloud with ten randomly sampled points
        # TODO: Think of a better algorithm
        sampler = np.random.random_integers(0,p.size/3-1,num)
        smear.AddPoints(p[sampler],s[sampler])
        return smear
    
    def CheckRefine(self):    
        return self.Size() > MAXSIZE
    
    def _MidPoint(self):
        p = self._points
        x = p[:,0]
        y = p[:,1]
        z = p[:,2]
        return 0.5*np.array([x.min()+x.max(),\
                             y.min()+y.max(),\
                             z.min()+z.max()])
    
    # Native methods
    def AddPoints(self, newPoints,sizes):
        isEmpty = self.Size() == 0
        if isEmpty:
            self._points = newPoints.copy()
        else:
            print self._points.shape, newPoints.shape
            self._points = np.concatenate((self._points,newPoints))
        if type(sizes) != type(None):
            if isEmpty:
                self._pointSizes = sizes.copy()
            else:
                self._pointSizes = np.concatenate((self._pointSizes,sizes))
        else:
            print "Sizes empty!"
        self._MakePositionAndRadius()
        
    def Preload(self):
        '''
        Preload object into graphics memory
        '''
        if self.Size() > 0:
            self._renderer.Build(self._points,self._pointSizes)
            self._renderer.Weight(self._weight)
        self._preloaded = True
        
    def Preloaded(self):
        return self._preloaded
        
    def Draw(self):
        '''
        Draw object (must be preloaded!)
        TODO: CREATE LISTS OF POINT SIZES FOR SMOOTHING
        '''
        if (not self.Preloaded()):
            self.Preload()
        #normvol = pow(self._points.size,0.333)
        #if self.Size() > 0.0:
        #    self._renderer.PointSize(300.0*self.Radius()/pow(self.Size(),0.333))
        #else:
        #    self._renderer.PointSize(1.0)
        if self.Size() > 0:
            self._renderer.Draw()
        
    def __str__(self):
        return "PointCloud size: "+self.Size()
    
    def Position(self):
        if type(self._position) == type(0):
            self._MakePositionAndRadius()
        return self._position
    
    def Radius(self):
        # Maximum bounding radius of cloud
        if type(self._position) == type(0):
            self._MakePositionAndRadius()
        return self._radius
    
    # INTERNAL USE ONLY
    # Sets the position of the clouds
    def _MakePositionAndRadius(self):
        # Find the MEAN position
        # TODO: Return peak value instead?
        if self.Size() > 0:
            self._position = np.sum(self._points,0) / float(self.Size())
            # Find radial distances
            r = self._points - self._position
            x = r[:,0]
            y = r[:,1]
            z = r[:,2]
            dists = x*x + y*y + z*z
            # Find maximum radial distance
            self._radius = np.sqrt(np.max(dists))
