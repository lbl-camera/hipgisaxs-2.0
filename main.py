
import json

from common import xp
from common import array_type
import numpy as np
from collections import OrderedDict

import math as m
import matplotlib.pyplot as plt
import rotation

from ff.cylinder import cylinder
from fresnel import propagation_coeffs
from structure_factor import structure_factor
from qspace import generate_qspace
from common import memcopy_to_device

if __name__ == '__main__':

    # load input parameters
    with open('../json/config.json') as fp:
        cfg = json.load(fp)

    alphai = xp.single(cfg['incident'] * xp.pi / 180)
    alpha = xp.array(cfg['alpha'], dtype=xp.single)
    theta = xp.array(cfg['theta'], dtype=xp.single)
    wavelength = cfg['wavelen']
    reflectivity_index = complex(cfg['delta'], cfg['beta'])
    
    N = 50
    radius = cfg['cylinder']['radius']
    height = cfg['cylinder']['height']
    datafile = cfg['datafile'] 

    #-----------------------
    temp = xp.array(np.load(datafile), dtype=np.single).T
    indx = [0, 1, 2, 6, 7]
    # scale 
    temp[indx,:] *= 1000
    #-----------------------

    # split work
    Ntotal = temp.shape[1]

    qx, qy, qz = generate_qspace(alphai, alpha, theta, wavelength)
    propagation = propagation_coeffs(alphai, alpha.ravel(), reflectivity_index)
   
    #  sample rotations in plane to simulate incoherant part
    zrots = np.random.rand(1000) * m.pi
    
    scat = xp.zeros((Ntotal, qx.size), dtype=np.csingle)
    img = xp.zeros(qx.size, dtype=np.single)

    for zrot in zrots:
        for ibeg in range(0, Ntotal, N):

            # partition orientation and shifts
            iend = min(ibeg+N, Ntotal)
            slc = slice(ibeg, iend)
            shifts = temp[0:3, slc]
            orientations = OrderedDict({'x': temp[3, slc], 'y': temp[4,slc], 'z': temp[5,slc]})
            radius = temp[6,slc]
            height = temp[7,slc]

            # DWBA
            for j in range(4):
                rot1 = OrderedDict({'z': zrot})
                q1, q2, q3 = rotation.rotate(qx, qy, qz[j], rot1)
                ff = cylinder(q1, q2, q3, radius, height, orientation = orientations, shift = shifts)
                scat[slc] += propagation[j] * ff

        tmp = scat.sum(axis=0)
        img += xp.abs(tmp)**2

    img = img.reshape(qx.shape) 
    qp = xp.sign(qy) * xp.sqrt(qx**2 + qy**2)
    qv = qz[0]
    if "cupy" in array_type:
        qp = qp.get()
        qv = qv.get()
        img = img.get()

    qrange = [qp.min(), qp.max(), qv.min(), qv.max()]
    plt.imshow(np.log(img+1), cmap='jet', origin='lower', extent = qrange)
    plt.savefig('scat.png')
