'''
Created on 4 Jan 2012

@author: samgeen
'''

# Numpy
import numpy as np
# Point cloud tree method
from Fluids.Octree import Octree
from Fluids.PointCloud import PointCloud
# Vect3 object
from Maths.Vect3 import Vect3
# Open GL (preface "gl" counts as a namespace in my book)
from pyglet.gl import *

# Point cloud with draw properties; allows optimisation methods inside cloud
# TODO: Define an abstract Drawable that has a defined interface
class PointDrawable(object):
    '''
    classdocs
    '''

    def __init__(self,pointCloud):
        '''
        Constructor
        '''
        self._tree = Octree(pointCloud)
        self._tree.FollowTreeTest(self.DrawTest)
        self._window = 0
        
    # Draw the points to screen
    def Draw(self, window):
        '''
        Draw object
        '''
        self._window = window
        # Draw the data in each cell
        i = 0
        # Set viewport in object to allow running of draw test
        # TODO: FIGURE OUT HOW TO REMAP THIS FN
        self._tree.FollowTreeTest(self.DrawTest)
        # List colours:
        # 0=white,1=red,2=green,3=yellow,4=blue,5=magenta,6=cyan?,7=black
        ar = np.array([1,1,0,1,0,1,0,0],dtype='float')
        ag = np.array([1,0,1,1,0,0,1,0],dtype='float')
        ab = np.array([1,0,0,0,1,1,1,0],dtype='float')
        numpts = 0
        glColor4f(1.,1.,1.,0.01)
        for cell in self._tree:
            # Hacky colour setting!!!
            #i = cell.Frame()
            #r = ar[i%8]
            #b = ab[i%8]
            #g = ag[i%8]
            #glColor4f(r,g,b,0.2)
            numdrawn = cell.Data().Draw()
            numpts += cell.Data().Size()
        # DIAGNOSTIC PRINT
        print "Number points shown:", numpts
            
    # Remap draw test inputted to Draw(...) to allow the tree to interpret it
    def DrawTest(self, cell):
        # Run viewport's draw test on the point cloud's mean position and maximum radius
        if type(self._viewport) != type(0):
            return self._window.DrawTest(cell.Data().Position(),cell.Data().Radius())
        else:
            return True