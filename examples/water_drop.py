import os
import sys
import json
from tqdm import tqdm

import numpy as np
from stl import mesh
import math as m
from collections import OrderedDict
import time

from gisaxs.common  import xp, array_type
from gisaxs import fftriangulation
from gisaxs import propagation_coeffs
from gisaxs import rotation
from gisaxs import qspace
from gisaxs import plot

if __name__ == '__main__':

    #  q-space #
    N = 512
    energy = 10000
    alphai = xp.deg2rad(0.2)
    theta =  xp.linspace(0, 1, N) * np.pi/180
    alpha = xp.linspace(0, 1, N) * np.pi/180

    #refractive indices # Si
    n_substrate = complex(4.8889242E-06, 7.37912842E-08)

    
    # stl file
    stl_file = "sphere.stl"
    data_path = "/home/dkumar/data/Chris"
    vertices = mesh.Mesh.from_file(os.path.join(data_path, stl_file)).points 
    print(vertices.shape)
    print(vertices.min())
    print(vertices.max())

    #vertices /= 10

    wavelength =1.23984E+03/energy
    theta, alpha = np.meshgrid(theta, alpha)
    qx, qy, qz = qspace(alpha, theta, alphai, wavelength)
    propagation = propagation_coeffs(alphai, alpha.ravel(), n_substrate)
  
    dummy = np.eye(3)

    # DWBA 
    scat = xp.zeros(qx.size, dtype=np.complex128)
    t0 = time.time()
    for j in range(4):
        q1, q2, q3 = qx, qy, qz[j]
        ff = fftriangulation(q1, q2, q3, dummy, vertices).ravel()
        scat +=  propagation[j] * ff

    dt = time.time() - t0
    print('time taken for GPU code', dt)

    # plotting
    img = np.abs(scat.reshape(qx.shape))**2
    qp = xp.sign(qy) * xp.sqrt(qx**2 + qy**2)
    qv = (qz[0] + qz[1])/2
    qrange = [qp.min(), qp.max(), qv.min(), qv.max()]

    img[qv<0] = 0
    if array_type == "cupy":
        qrange = [q.get() for q in qrange]
        img = img.get()

    fig_name = os.path.splitext(stl_file)[0] + ".png"
    plot.image_save(img, os.path.join(data_path, fig_name), qrange)
