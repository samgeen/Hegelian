'''
Created on 8 Sep 2011

@author: samgeen
'''
'''
TODO: ALLOW MULTIPLE THINGS TO REGISTER TO THE SAME EVENT!!!!
'''

class EventHandler(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__events = list()
        self.__register = dict()
        
    def FireEvent(self, eventName, fireData=0):
        '''
        Fires an event and notifies all registered objects and passes fireData to them
        NOTE! CURRENT IMPLEMENTATION ALLOWS ONLY ONE OBJECT TO RECEIVE AN EVENT - FIX THIS!
        '''
        if fireData != 0:
            self.__register[eventName](fireData)
        else:
            self.__register[eventName]()
        
    def Register(self, eventName, receivingObject):
        '''
        Registers an object to be fired when a certain event name is called
        NOTE! CURRENT IMPLEMENTATION ALLOWS ONLY ONE OBJECT TO RECEIVE AN EVENT - FIX THIS!
        '''
        self.__register[eventName] = receivingObject
        
    def Deregister(self, eventName, receivingObject):
        '''
        Deregisters this object so it no longer receives events
        NOTE! CURRENT IMPLEMENTATION ALLOWS ONLY ONE OBJECT TO RECEIVE AN EVENT - FIX THIS!
        '''
        self.__register.pop(eventName)
        
        
singletonEventHandler = EventHandler()

'''
Events
'''
' Fires an event; the event handler passes fireData to whatever is registered to receive the event '
def FireEvent(eventName, fireData):
    singletonEventHandler.FireEvent(eventName, fireData)
    
' Registers receivingObject to receive events with eventName '
def RegisterEvent(eventName, receivingObject):
    singletonEventHandler.Register(eventName, receivingObject)

' Stops the receivingObject receiving events with eventName '
def DeregisterEvent(eventName, receivingObject):
    singletonEventHandler.Deregister(eventName, receivingObject)