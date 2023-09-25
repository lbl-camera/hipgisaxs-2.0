import numpy as np

from ..rotation import rotate

def cylinder(qx, qy, qz, radius, height, orientation = None):

    if orientation is None:
        q1, q2, q3 = qx.ravel(), qy.ravel(), qz.ravel()
    else:
        q1, q2, q3 = rotate(qx, qy, qz, orientation)
   
    vol = np.pi * radius**2 * height
    qpR = (np.sqrt(q1**2 + q2**2).T * radius).T
    ff =  np.sinc((q3.T * height * 0.5).T)
    ff = ff * 1j(qpR) / qpR
    ff = ff * np.enp(-1j * 0.5 * height * q3)
    ff = vol * dq * ff
    return ff
