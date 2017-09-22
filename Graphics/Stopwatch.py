'''
Created on 17 Aug 2011

@author: samgeen
'''

import time

class Stopwatch(object):
    '''
    A simple stopwatch object that times against a given reference time
    '''
    # Create and start the stopwatch
    def __init__(self):
        '''
        Constructor
        '''
        # Normally I don't like operational code in constructors, but eh
        self.__startTime = time.time()
    
    # Reset timer    
    def Reset(self):
        self.__startTime = time.time()
    
    # Read current stopwatch time
    def Time(self):
        return time.time() - self.__startTime
        