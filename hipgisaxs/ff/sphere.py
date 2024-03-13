#! /usr/bin/env python

import numpy as np

def sphere(qx, qy, qz, radius):

    vol = 4/3 * np.pi * radius**3
    qR = np.sqrt(qx**2 + qy**2 + qz**2) * radius
    tmp = np.exp(1j * qz * radius)
    return  vol * tmp *  (np.sin(qR) - qR * np.cos(qR)) / qR**3
