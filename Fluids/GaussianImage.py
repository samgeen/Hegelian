'''
Created on Nov 21, 2012

@author: samgeen
'''

import numpy as np

def CubicImage(length,alpha=True):
    r = np.arange(-0.5,0.5,1.0/length)
    alphanum = 3
    if alpha:
        alphanum = 4
    a = np.zeros((length,length,alphanum))
    for i in range(0,length):
        for j in range(0,length):
            rt = np.sqrt(r[i]*r[i] + r[j]*r[j])*20
            if rt < 1:
                x = 1.0/6.0*( (2.0 - rt)**3.0 - 4*(1.0 - rt)**3.0)
            elif rt < 2:
                x = 1.0/6.0*( (2.0 - rt)**3.0)
            else:
                x = 0.0
            a[i,j,0:3] = x
    #a = np.exp(a)-1.0
    a /= a.max()
    a[:,:,3] = 1.0
    print np.max(a), np.min(a[a > 0.0]), np.min(a)
    return a

def GaussianImage(length,alpha=True):
    r = np.arange(-0.5,0.5,1.0/length)
    alphanum = 3
    if alpha:
        alphanum = 4
    a = np.zeros((length,length,alphanum))
    fact = 10.0
    for i in range(1,length-1):
        for j in range(1,length-1):
            rt = np.sqrt(r[i]*r[i] + r[j]*r[j])
            x = np.exp(-rt*fact)
            a[i,j,0:3] = x
    #a = np.exp(a)-1.0
    a /= a.max()
    a[a < 1e-2] = 0.0
    a[:,:,3] = 1.0
    print np.max(a), np.min(a[a > 0.0]), np.min(a)
    return a
    
def GaussianImage3D(length,alpha=True,kernel="gaussian"):
    '''
    Make a 2D square image of a 2D Gaussian scaled between 0 and 1
    NOTE: THIS IS A 3D COLUMN DENSITY OF A GAUSSIAN!!!!!
    length: integer length of image
    centre: centre of gaussian
    rscale: radius to scale to
    '''
    r = np.arange(-0.5,0.5,1.0/length)
    alphanum = 3
    if alpha:
        alphanum = 4
    a = np.zeros((length,length,length,alphanum))
    if kernel == "gaussian":
        fact = 10.0
    if kernel == "cubic":
        fact = 16.0
    if kernel == "poly":
        fact = 4.0
    for i in range(0,length):
        for j in range(0,length):
            for k in range(0,length):
                if kernel == "gaussian":
                    x = np.exp(-fact*(r[i]*r[i] + r[j]*r[j] + r[k]*r[k])**(0.5))
                    x -= 1e-3
                    x = np.max([0.0,x])
                elif kernel == "cubic":
                    rt = 2.0*np.sqrt(fact*(r[i]*r[i] + r[j]*r[j] + r[k]*r[k]))
                    if rt < 1:
                        x = 1.0/6.0*( (2.0 - rt)**3.0 - 4*(1.0 - rt)**3.0)
                    elif rt < 2:
                        x = 1.0/6.0*( (2.0 - rt)**3.0)
                    else:
                        x = 0.0
                else:
                    rt = fact*(r[i]*r[i] + r[j]*r[j] + r[k]*r[k])
                    x = (1 - rt)**3.0
                    if rt > 1.0:
                        x = 0.0
                a[i,j,k,0] = x
                a[i,j,k,1] = x
                a[i,j,k,2] = x
                if alpha:
                    a[i,j,k,3] = 1.0
    if kernel == "gaussian":
        a = np.sum(a,0)
    else:
        a = np.max(a,0)
    a = np.exp(a)
    a -= a.min()
    a /= np.max(a)
    print np.max(a), np.min(a[a > 0.0]), np.min(a)
    return a
    
if __name__=="__main__":
    import matplotlib.pyplot as plt
    length = 64
    image = GaussianImage(length)
    image[image == 0.0] = np.min(image[image > 0.0])
    image = np.log(image)
    image = (image - image.min()) / (image.max() - image.min())
    print np.max(image), np.min(image)
    plt.imshow(image)
    #plt.plot(image[:,length/2])
    #plt.yscale("log")
    plt.show()
