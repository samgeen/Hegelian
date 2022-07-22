'''
Created on Nov 21, 2012

@author: samgeen
'''

from PointRendererSimple import PointRendererSimple
from PointRendererBillboard_Impl3 import PointRendererBillboard_Impl3
from PointRendererBillboard_Impl4 import PointRendererBillboard_Impl4

class PointRendererFactory(object):
    '''
    Factory class for point renderer
    '''


    def __init__(self):
        '''
        Constructor
        '''
        # Set up renderer list
        r = dict()
        r["PointRendererSimple"] = PointRendererSimple
        r["PointRendererBillboard"] = PointRendererBillboard_Impl3
        self._renderers = r
        
    def MakeRenderer(self, name):
        if name in self._renderers:
            r = self._renderers[name]()
        else:
            print "NO RENDERER WITH THE NAME \""+name+"\""
            raise NotImplementedError
        return r
