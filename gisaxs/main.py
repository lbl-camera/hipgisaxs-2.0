
import json

from common import xp
import numpy as np
from collections import OrderedDict

import math as m
import matplotlib.pyplot as plt
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
    alpha = xp.array(cfg['alpha'], dtype=np.single)
    theta = xp.array(cfg['theta'], dtype=np.single)
    wavelength = cfg['wavelen']
    reflectivity_index = complex(cfg['delta'], cfg['beta'])
    
    N = 300
    
    #-----------------------
    temp = xp.array(np.load('/home/dkumar/Data/roth/agnw_data.npy'), dtype=np.single)
    #-----------------------
    # split work
    Ntotal = temp.shape[1]

    qx, qy, qz = generate_qspace(alphai, alpha, theta, wavelength)
    propagation = propagation_coeffs(alphai, alpha.ravel(), reflectivity_index)
    
    scat = xp.zeros((Ntotal, qx.size), dtype=np.csingle)
    for ibeg in range(0, Ntotal, N):

        # partition orientation and shifts
        iend = min(ibeg+N, Ntotal)
        shifts = temp[0:3, ibeg:iend]
        orientations = OrderedDict({'x': temp[3,ibeg:iend], 'y': temp[4,ibeg:iend], 'z': temp[5,ibeg:iend]})
        radius = temp[6,ibeg:iend]
        height = temp[7,ibeg:iend]

        # DWBA
        for j in range(4):
            ff = cylinder(qx, qy, qz[j], radius, height, orientation = orientations, shift = shifts)
            scat[ibeg:iend] = propagation[j] * ff

    img = scat.sum(axis=0)
    img = xp.abs(img)**2
    img = img.reshape(qx.shape) 
    plt.imshow(np.log(img.get()+1), cmap='jet', origin='lower')
    plt.show()
