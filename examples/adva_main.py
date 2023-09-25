import os
import sys
import json

import numpy as np
from collections import OrderedDict

import math as m

from gisaxs.common  import xp, array_type
from gisaxs.ff import cone, cone_shell
from gisaxs import propagation_coeffs
from gisaxs import structure_factor
from gisaxs import qspace
from gisaxs import plot

if __name__ == '__main__':

    #
    energy = 878
    alphai = np.deg2rad(3.4)
    theta =  np.linspace(-9.32, 10.67, 1024) * np.pi/180
    alpha = np.linspace(-5.16, 18.5, 1212) * np.pi/180

    #refractive indices
    n_core =  1-complex(-6.1647E-05, 2.163E-04) # Ce2O3
    n_shell = 1-complex(-1.538E-04, 2.0297E-04) # CeO2
    n_substrate = complex(5.333E-04, 8.2545E-05) # Si
    
    radius = 60
    height = 24.3
    angle = np.deg2rad(50.3)
    lattice = np.array([[200,0,0],[0,200,0],[0,0,1]])
    repeats = np.array([500, 500,0])
    orient = OrderedDict({'z': np.deg2rad(3.2)})
    #-----------------------


    wavelength =1.23984E+03/energy
    theta, alpha = np.meshgrid(theta, alpha)
    qx, qy, qz = qspace(alpha, theta, alphai, wavelength)
    propagation = propagation_coeffs(alphai, alpha.ravel(), n_substrate)
  
    thickness = 0
    r = radius-thickness
    h = height-thickness

    # DWBA 00000000
    scat = xp.zeros(qx.size, dtype=np.csingle)
    for j in range(4):
        ff = cone(qx, qy, qz[j], r, h, angle)
        sf = 1
        scat +=  propagation[j] * ff * sf
            
    # Plotting
    img = np.abs(scat.reshape(qx.shape))**2
    qp = xp.sign(qy) * xp.sqrt(qx**2 + qy**2)
    qv = (qz[0] + qz[1])/2
    qrange = [qp.min(), qp.max(), qv.min(), qv.max()]
    img[qv<0] = 0
     
    plot.image_save(img, qrange, (10, 25), "figs/Scat_solid.png")
