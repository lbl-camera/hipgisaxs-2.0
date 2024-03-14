import numpy as np

from ..rotation import rotate

def cuboid(qx, qy, qz, length, width, height, orientation = None):

    if orientation is None:
        q1, q2, q3 = qx.ravel(), qy.ravel(), qz.ravel()
    else:
        q1, q2, q3 = rotate(qx, qy, qz, orientation)
   
    vol = length * width * height
    shft = np.exp(1j * q3 * height / 2)
    ft = np.sinc(q1*length/2)*np.sinc(q2*width/2)*np.sinc(q3*height/2)
    return (vol * ft * shft)

