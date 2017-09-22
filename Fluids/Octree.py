'''
Created on 13 Dec 2011

@author: samgeen
'''

import numpy as np

# Maximum level allowed
_MAXLEVEL = 20 # arbitrary default value
def MaxLevel(newMaxLevel):
    _MAXLEVEL = np.max([newMaxLevel,0])

# Simple null check (todo: optimise?)
NULL = type(0)
def IsNull(obj):
    return type(obj) == NULL

# NOTES:
# TODO: Iterator doesn't work
# The pattern requires that the collection class remain static
# Hence we need to contain cells inside the octree object
# Make list of items inside octree and iterate through that
# Split Cell class off that contains data, level, etc
# Keep Octree as head class
        
class Octree(object):    
    '''
    An octree. This provides a simple Octree interface that takes a data object of type AbstractTreeData.
    The motivation is to separate the tree structure and data structure and define an interface between
    the two. 
    '''
    def __init__(self, data):
        '''
        Constructor
        '''
        # Head node of tree
        self._tree = OctreeCell(data)
        # Refine
        # Iterator bookmark
        self._iter = self._tree
        # Next iterator; used in case we need to skip levels of the tree
        self._next = self._iter.Next()
        # Is this the first iteration?
        self._first = True
        # Ignore branches while iterating?
        self._ignoreBranches = True
        # TODO: THINK OF A WAY TO MOVE THIS OUT OF THE CONSTRUCTOR
        # THIS PREVENTS FREAK, HALF-FORMED OBJECTS IF Refine() FAILS
        self._tree.Refine()
        # Check child function is by default always true
        self._CheckChild = lambda x: True
        
    # Ignore branches when iterating? 
    # NOTE: This will be overridden if FollowTreeDown returns false; 
    #       Here, the branch will be used instead
    def IgnoreBranches(self, ignoreBool):
        self._ignoreBranches = ignoreBool

    # Give the tree a function that tells it whether to iterate down or stop and use the branch instead
    # INPUT: Function returning a bool that accepts an OctreeCell object; default True
    def FollowTreeTest(self, Func=lambda x: True):
        self._CheckChild = Func
    
    # Iterate through the tree cells
    # TODO: THINK OF A WAY OF ALLOWING SELECTIVE ITERATION THROUGH ONLY SOME CELLS
    #       e.g. when a camera is far away, show low-res data instead
    def __iter__(self):
        self._first = True
        self._iter = self._tree
        return self
    
    def next(self):
        ignoreBranch = self._ignoreBranches
        # Don't jump to the next item if this is the first iteration
        if not self._first: 
            self._iter = self._next
        else:
            self._first = False
        # Is the next item null?
        if IsNull(self._iter):
            raise StopIteration
        # Is this a leaf node? If so, just return it
        if self._iter.IsLeaf():
            self._next = self._iter.Next()
            return self._iter
        # Is it not a leaf node? This is trickier.
        # We test whether we need to go further down the tree or stop and use the branch
        # Ignore branches? If so, skip to the next item until we find a leaf
        else:
            # Check whether we iterate down; if not, override ignoreBranch and return this only
            # Also, set the _next item to point to the correct place
            if not self._CheckChild(self._iter):
                # Here, we don't need to check the children: 
                #  Return this and step to the next cell on the same level number or lower
                self._next = self._iter.NextSameLevel()
                return self._iter
            else:
                # Here, we do need to check the children.
                # Check whether we ignore branches first, though
                if not ignoreBranch:
                    self._next = self._iter.Next()
                    return self._iter
                else:
                    # If we do ignore branches, just skip to the next one
                    self._next = self._iter.Next()
                    return self.next()
        return self._iter
    
    # Return tree info as a string if the object is printed or cast to string
    def __str__(self):
        out = ""
        # Don't ignore branches; print everything
        tempIgnore = self._ignoreBranches
        self._ignoreBranches = False
        # Run through the items
        for cell in self:
            out += str(cell)+"\n"
        # Reset ignore branches boolean
        self._ignoreBranches = tempIgnore
        # Return completed string
        return out
        
# In effect, this is the iterator object for Octree
class OctreeCell(object):
    '''
    An octree cell.
    '''

    def __init__(self, data, level=0, parent=0):
        '''
        Constructor
        '''
        # Child cells
        self._children = 0
        # Data stored inside cell of type AbstractTreeData
        self._data = data.copy()
        # Frame of refinement (top = 0)
        self._level = level
        # Next item
        # NOTE: This is typically set in method _MakeNexts
        self._next = 0
        # Next item *ON SAME LEVEL OR LOWER*
        # This is in case we want to skip the higher levels of the tree
        self._nextSameLevel = 0
        # Parent cell. This is required if we want to step out of the iterator
        self._parent = parent
        # Do we iterate through the children or just jump back to the parents?
        self._checkChild = True
        
    # Is this branch a leaf node?
    def IsLeaf(self):
        return IsNull(self._children)
            
    # Return a reference to the data object
    def Data(self):
        return self._data
    
    # Return the level of the cell in the tree
    def Level(self):
        return self._level
        
    # Refine this cell (i.e. create children), conditional on data needing refinement 
    # TODO: ALLOW DEREFINING
    def Refine(self,forceRefine=False):
        # Check for forcing refinement; if not, check whether the data needs refining
        if not forceRefine and self._level != _MAXLEVEL: 
            refine = self._data.CheckRefine()
        else:
            refine = forceRefine
        # Refine? Refine!
        if refine and IsNull(self._children):
            # Split the data into 8
            splitData = self._data.Split()
            # Smear out the remaining data for use in low-res version
            self._data = self._data.Smear()
            # Refine cells
            # This makes a new Octree object in each child object in a 2x2x2 array
            # This is horrible syntax, guys
            parent = self
            self._children = np.empty((2,2,2),dtype=object)
            self._children[0,0,0] = OctreeCell(splitData[0,0,0],self._level+1,parent)
            self._children[1,0,0] = OctreeCell(splitData[1,0,0],self._level+1,parent)
            self._children[0,1,0] = OctreeCell(splitData[0,1,0],self._level+1,parent)
            self._children[1,1,0] = OctreeCell(splitData[1,1,0],self._level+1,parent)
            self._children[0,0,1] = OctreeCell(splitData[0,0,1],self._level+1,parent)
            self._children[1,0,1] = OctreeCell(splitData[1,0,1],self._level+1,parent)
            self._children[0,1,1] = OctreeCell(splitData[0,1,1],self._level+1,parent)
            self._children[1,1,1] = OctreeCell(splitData[1,1,1],self._level+1,parent)
            # TODO: FIX fromfunction IMPLEMENTATION
            # Vectorised octree
            #VOct = np.vectorize(Octree)
            #MakeFunc = lambda i,j,k: VOct(splitData[i,j,k],parent=parent,level=self._level+1)
            #self._children = np.fromfunction(MakeFunc, (2,2,2), dtype=int)
            # Set next items
            self._MakeNexts(self._children.flat)
            #print self._children[1,1,1]._next
            
            # Now refine the children!
            for child in self._children.flat:
                child.Refine(forceRefine)
        
    # Return info for this object as a string
    def __str__(self):
        sp = " "*self._level
        if self.IsLeaf():
            return sp+"Leaf node at level "+str(self._level)+" containing: "+str(self._data)
        else:
            return sp+"Branch at level "+str(self._level)+"..."


        # TODO: FIGURE OUT SELECTIVE ITERATION
        #if self._checkChild:
        #    return self._next
        #else:
        #    return self._parent._next

    def Next(self):
        return self._next
    
    def Parent(self):
        return self._parent
    
    def NextSameLevel(self):
        return self._nextSameLevel
    
    # Set the next pointers
    # Input a *FLAT* array of children
    # ONLY CALL THIS JUST AFTER THE CHILDREN ARE MADE
    def _MakeNexts(self, children):
        # Set the first 7 objects to point to the (i+1)th item
        # Uses the C++ tradition of allowing access to private members of different 
        #   objects of the same class type
        for i in range(0,7):
            children[i]._next = children[i+1]
            children[i]._nextSameLevel = children[i+1]
        # Now set the last one to point to this object's next item
        children[7]._next = self._next
        children[7]._nextSameLevel = self._next
        # Finally, reset own next pointer to the first child
        self._next = children[0]
        # DO NOT CHANGE self._nextSameLevel HERE!

# SAMPLE TREE DATA CLASSES            

# Abstract tree data object with methods needed to be implemented
# TODO: ADD NON-IMPLEMENTATION ERROR IF FUNCTIONS ARE CALLED
class AbstractTreeData(object):
    def __init__(self):
        raise NotImplementedError, "Abstract class method called (AbstractTreeData.__init__)"
    # Split the data into 2x2x2 and return the results of the splitting
    def Split(self):
        raise NotImplementedError, "Abstract class method called (AbstractTreeData.Split)"
    # Returns a "smeared-out" low-res alternative to this data
    def Smear(self):
        raise NotImplementedError, "Abstract class method called (AbstractTreeData.Smear)"
    # Check to see whether the data needs refining and return True/False
    def CheckRefine(self):
        raise NotImplementedError, "Abstract class method called (AbstractTreeData.CheckRefine)"

# Empty Data Object
class EmptyTreeData(AbstractTreeData):
    def __init__(self):
        pass
    # Split the data into 2x2x2
    def Split(self):
        # NOTE: DOESN'T WORK AS ITERATORS DON'T MODIFY THE ORIGINAL OBJECT
        split = np.empty((2,2,2),dtype=object)
        for spl in split.flat:
            spl = EmptyTreeData()
        return split 
    
    # Smear out the data to provide a low-res alternative
    def Smear(self):
        return EmptyTreeData()
    
    # Check to see whether the data needs refining
    def CheckRefine(self):
        return False
    
def UnitTest():
    from PointCloud import PointCloud
    points = PointCloud()
    mean = [0,0,0]
    cov = [[1.0,0,0],[0,1.0,0],[0,0,1.0]]*np.array([0.01])
    p = np.random.multivariate_normal(mean,cov,20000)
    points.AddPoints(np.array(p))
    tree = Octree(points)
    print "Printing tree directly:"
    print tree
    print "Printing tree by iterating through cells:"
    for cell in tree:
        print cell
    
if __name__=="__main__":
    UnitTest()    