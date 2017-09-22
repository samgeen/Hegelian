'''
Created on 8 May 2013

@author: samgeen
'''

'''
A module listing all events used by the game with some convenience functions
'''

import pyglet


class UserDispatcher(pyglet.event.EventDispatcher):
    def doredraw(self):
        self.dispatch_event("redraw")
        
UserDispatcher.register_event_type("redraw")

dispatcher = UserDispatcher()

def Redraw():
    dispatcher.doredraw()

class UserInputHandler(object):
    '''
    Handles user input from mouse and keyboard and passes it to a specified handler object
    '''
    def __init__(self, handler):
        # Use pyglet's inbuilt key state handler (NOTE - MIGHT NOT BE ABLE TO USE MODIFIER KEYS LIKE THIS)
        self._handler = handler
        dispatcher.push_handlers(self)
        
    def __del__(self):
        # TODO: CHECK THAT THIS DOESN't MAKE BAD THINGS HAPPEN IF IT'S NOT DELETED IMMEDIATELY
        dispatcher.pop_handlers(self)
    
    def on_mouse_press(self, x, y, button, modifiers):
        press = {"pos": (x,y), "button":button, "mod": modifiers, "pressed":True}
        self._handler.OnMouseButton(press)

    def on_mouse_release(self, x, y, button, modifiers):
        release = {"pos": (x,y), "button":button, "mod": modifiers, "pressed":False}
        self._handler.OnMouseButton(release)

    # NOTE: Functions drag and move merged to make things easier
    def on_mouse_motion(self, x, y, dx, dy):
        motion = {"pos": (x,y), "diff": (dx, dy), "buttons":0, "mod":0}
        self._handler.OnMouseMove(motion)
        
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        motion = {"pos": (x,y), "diff": (dx, dy), "buttons":buttons, "mod":modifiers}
        self._handler.OnMouseMove(motion)
        
    def on_key_press(self, button, modifiers):
        press = {"button":button, "mod": modifiers, "pressed":True}
        self._handler.OnKeyboard(press)

    def on_key_release(self, button, modifiers):
        release = {"button":button, "mod": modifiers, "pressed":False}
        self._handler.OnKeyboard(release)
    
    def on_redraw(self):
        # Try to redraw if the level has such a functionality. If not, ignore.
        try:
            self._level.Redraw()
        except:
            pass
