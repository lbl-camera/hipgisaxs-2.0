#from numba import jit
import numpy as np
from scipy.special import j1
from numpy.polynomial.legendre import leggauss

from ..rotation import rotate

def cone(qx, qy, qz, R, H, angle, orientation=None):

    tan_a = np.tan(angle)
    Rh = R - H / tan_a
    if Rh < 0:
        raise ValueError('invalid side angle')

    if orientation is None:
        q1, q2, q3 = qx.ravel(), qy.ravel(), qz.ravel()
    else:
        q1, q2, q3 = rotate(qx, qy, qz, orientation)

    qp = np.sqrt(q1**2 + q2**2)
    qzp = q3 * tan_a
    t1 = 2 * np.pi * tan_a * np.exp(1j * qzp * R)

    # integrate
    ndeg = 8
    nodes, wghts = leggauss(ndeg)
    nodes = (Rh - R)/2 * nodes + (Rh + R)/2
    fq = lambda r: (r**2 * np.exp(-1j * qzp * r) * j1(qp * r)/(qp * r))
    I = sum(wghts[i] * fq(nodes[i]) for i in range(ndeg))
    return (t1 * I)
