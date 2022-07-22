'''
Created on Feb 27, 2014

@author: sgeen
'''
# HACK SKETCH OF WHAT IT SHOULD LOOK LIKE

import pyglet
from pyglet.gl import *

import numpy as np

import os, sys
sys.path.append("../")
import hegelian
import random

from hegelian.Graphics.MeshDrawable import MeshDrawable

# Set up window
WINSIZE = 512
window = pyglet.window.Window(WINSIZE,WINSIZE)

# Test sprite
serious = pyglet.sprite.Sprite(pyglet.image.load('serious.png'), x=50, y=50)
silly = pyglet.sprite.Sprite(pyglet.image.load('silly.png'), x=window.width-550, y=50)

# Import simulation data
#snap = asvis.Snapshot("/data/Simulations/asvis_outs/output_00016")
#snap = asvis.Snapshot("/data/Simulations/asvis_outs/spiral68_010")
#drawable = snap.MakeCloud("stars")

# Import mesh data
#drawable = MeshDrawable("/data/Simulations/MC_RT/cubes/N48_M4_B02_C2_short/",window,["rho"])
#drawable = MeshDrawable("/data/Simulations/MC_RT/cubes/N50-SN/",window,["rho","T","xHII"])
#drawable = MeshDrawable("/data/Simulations/MC_RT/cubes/3304_hires/",window,["rho","T","xHII"])
#drawable = MeshDrawable("/data/Simulations/MC_RT/cubes/2701_fiducialsinks_single/",window,["rho","T","xHII"])
drawable = MeshDrawable("C:|Users|samge|Data|Simulations|MC2701|cubes".replace("|",os.sep),window,["rho","T","xHII"])
#drawable = MeshDrawable("/home/samgeen/Data/Simulations/MC2701/cubes",window,["rho","T","xHII"])

FIRST = True
frames = None

# Make frame in window
def OnInit():
    global frames
    randFrames = False
    if randFrames:
        frames = list()
        for i in range(0,3):
            size = random.randint(100,800)
            x = random.randint(0,window.width-size)
            y = random.randint(0,window.height-size)
            Print("Making frame of length", size, "at ("+str(x)+", "+str(y)+")")
            frame = hegelian.Frame(window, x, y, size, size)
            frame.Add(drawable)
            frames.append(frame)
    else:
        frame = hegelian.Frame(window, 0,0,WINSIZE,WINSIZE)
        frame.Add(drawable)
        frames = [frame]

    glClearColor(0.0, 0.0, 0.0, 1.0)

@window.event
def on_draw():
    global FIRST, frames
    if FIRST:
        OnInit()
        FIRST = False
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # You can draw whatever pyglet stuff here
    # funnysprite.draw()
    # serioussprite.draw()
    # etc
    #serious.draw()
    # IMPORTANT !! FRAME DRAW MUST CHECK THAT CAMERA, USER INPUT IS SET UP, 
    #              AND DO THAT IF NOT DONE ALREADY
    for frame in frames:
        frame.Draw()
    # And you can do more stuff afterwards
    #silly.draw()


print("ooooooooooooooooo")
print("RUNNING MAIN LOOP")
print("ooooooooooooooooo")
pyglet.app.run()
