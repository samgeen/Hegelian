'''
Make a data cube from the fields in a simulation
Sam Geen, May 2015
'''

import Hamu
import numpy as np
import pymses
import hydrofuncs

import os

def run(snap,folder):
    ro = snap.RawData()
    filename = folder+"/cube_rho_"+str(snap.OutputNumber()).zfill(5)+".npy"
    if os.path.exists(filename):
        print filename, "exists, returning"
        return
    else:
        print "Making", filename,"...", 
    lmin = ro.info["levelmin"]
    lsize = 2**lmin
    coords = np.arange(0.0,1.0,1.0/float(lsize))
    grid = np.meshgrid(coords,coords,coords)
    points = np.array([grid[0].flatten(),grid[1].flatten(),grid[2].flatten()])
    points = points.T
    print "Sampling grid ...", 
    amr = ro.amr_source(["rho"])
    scale = hydrofuncs.scale_by_units(ro,"rho")
    samples = pymses.analysis.sample_points(amr,points)
    dens = scale(samples)
    np.save(filename, dens.astype("float32"))
    print "Done!"

def runforsim(simname):
    sim = Hamu.Simulation("N48_M4_B02_C2")
    simfolder = "../cubes/"+sim.Name()
    try:
        os.mkdir(simfolder)
    except:
        pass
    for snap in sim.Snapshots():  
        run(snap,folder=simfolder)

if __name__=="__main__":
    runforsim("N48_M4_B02_C2")
