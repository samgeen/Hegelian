'''
Created on Nov 8, 2012

@author: samgeen
'''

#TODO: FIGURE OUT HOW TO DO ABSTRACT BASE CLASSES AGAIN

class PointRenderer(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
        
    def Name(self):
        '''
        WHAT'S THIS RENDERER'S NAME? I NEED A NAME.
        '''
        raise NotImplementedError
    
    def Weight(self, weight):
        '''
        Weight the point densities by weight
        '''
        raise NotImplementedError
    
    def Build(self, points):
        '''
        Build the renderer with the given list of points
        '''
        raise NotImplementedError
    
    def Draw(self):
        '''
        Draw the points
        '''
        raise NotImplementedError
    
