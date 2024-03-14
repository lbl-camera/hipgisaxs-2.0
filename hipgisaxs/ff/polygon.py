#! /usr/bin/env python

try:
    import cupy as xp
    from cupy import sin, cos
    from cupyx.scipy.special import j1
except ImportError:
    import numpy as xp
    from numpy import sin, cos
    from scipy.special import j1

from math import pi
import ipdb


def polygon(qx, qy, qz, radius, angles, orientation = None):

    # roatate if object is oriented
    if orientation is not None:
        q1, q2, q3 = rotate(qx, qy, qz, orientation)
    else:
        q1, q2, q3 = qx, qy, qz

    # q
    qvec = xp.vstack((q1.ravel(), q2.ravel(), q3.ravel())).T
    qval = xp.linalg.norm(qvec, axis=1)

    # surface normal is parallel to x-axis
    nt = xp.array([1, 0, 0])  
    qnt = qx.ravel()
    projqt2 = qval**2 - qnt**2
    print(xp.any(projqt2 < 1.E-10))

    # vertices
    a = xp.array(angles)
    x = xp.zeros((len(angles)+1, 3))
    x[1:,1] = radius * cos(a)
    x[1:,2] = radius * sin(a)
    x[-1,:] = x[0,:]


    ff = xp.zeros(qval.shape, dtype=complex)
    for i in range(len(angles)):
        v1 = x[i,:]
        v2 = x[i+1,:]

        r = v2 - v1
        d = xp.linalg.norm(r)

        # normals
        nv = r/d
        ne = xp.cross(nv, nt)
    
        # projections
        qne = xp.dot(qvec, ne)
        qnv = xp.dot(qvec, nv)
        projqe2 = projqt2 - qne**2
        print(xp.any(projqe2 < 1.E-10))

        t1 = qval**2 * projqt2 * projqe2
        t2 = -1j * qnt * qne * qnv 
        t3 = xp.exp(-1j * (xp.dot(qvec, v2) - xp.dot(qvec, v1)))
        ff += t2 * t3 / t1

    return ff.reshape(qx.shape)


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    n = 4 
    beta = 2 * pi / n
    # counter clockwise
    angles = [xp.deg2rad(-126 + i*72) for i in range(n)]
    a0 = -pi/2 - beta/2
    angles = [a0 + i * beta  for i in range(n)]
    radius = 10

    a = xp.linspace(0, 0.25, 1024)
    t = xp.linspace(-0.125, 0.125, 1024)
    k0 = 50.68
    ai = 0.2 * pi / 180 

    t, a = xp.meshgrid(t, a)
    qx = k0 * (cos(a) * cos(t) - cos(ai))
    qy = k0 * (cos(a) * sin(t))
    qz = k0 * (sin(a) + sin(ai))

    ff = polygon(qx, qy, qz, radius, angles)
    img = xp.abs(ff)**2
    plt.imshow((xp.log(img)**2).get(), origin='lower')
    plt.savefig('foo.png')
