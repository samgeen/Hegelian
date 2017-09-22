'''
Created on 14 Jun 2013

@author: samgeen
'''

import pyglet

class Text(object):
    '''
    A wrapper around a Pyglet text object
    '''
    
    def __init__(self, text, x=0, y=0,font=None,colour=None):
        if font == None:
            font = pyglet.font.load("Palatino", 40,bold=True) 
        if colour == None:
            colour = color=(0.0,0.0,0.0,1.0)
        text = text.replace("\n"," ")
        text = text.replace("\r"," ")
        self._text = text
        self._pos = (x,y)
        self._sprite = pyglet.font.Text(font, text,x=x,y=y,halign='left',valign='center',color=colour)
        
    def Text(self):
        return self._text
    
    def Pos(self):
        return self._pos
    
    def Edge(self,edgename):
        if "right":
            return self._sprite.x + self._sprite.width
        if "left":
            return self._sprite.x
        if "top":
            return self._sprite.y + self._sprite.height
        if "down":
            return self._sprite.y
        # Oops - should not be here. Wrong key given?
        raise KeyError
    
    def Width(self):
        return self._sprite.width
    
    def Height(self):
        return self._sprite.height
            
    def Draw(self):
        self._sprite.draw()
    
    def UpdateText(self, text):
        text = text.replace("\n","")
        text = text.replace("\r","")
        self._text = text
        self._sprite.text = self._text
    
    def Move(self, pos):
        self._pos = pos
        x, y = pos
        self._sprite.x = x
        self._sprite.y = y