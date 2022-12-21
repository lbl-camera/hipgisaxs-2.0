#! /usr/bin/env python

from ..common import xp
from ..common import j1
from ..rotation import rotate

def cylinder(qx, qy, qz, radius, height, orientation = None, shift = None):

    # roatate if object is oriented
    if orientation is not None:
        angles = orientation.copy()
        q1, q2, q3 = rotate(qx, qy, qz, angles)
    else:
        q1, q2, q3 = qx.ravel(), qy.ravel(), qz.ravel()

    # shift w.r.t unrotated q-coords
    if shift is not None:
        dq = xp.outer(shift[0], qx.ravel())
        dq += xp.outer(shift[1], qy.ravel())
        dq += xp.outer(shift[2], qz.ravel())
        dq = xp.exp(1j * dq)
    else:
        dq = 1.

    vol = xp.pi * radius**2 * height
    qpR = (xp.sqrt(q1**2 + q2**2).T * radius).T

    ff =  xp.sinc((q3.T * height * 0.5).T)
    ff = ff * j1(qpR) / qpR
    if isinstance(height, float):
        ff = ff * xp.exp(-1j * 0.5 * height * q3)
        ff = vol * dq * ff
    else:
        tmp = xp.exp(-1j * 0.5 * height * q3.T).T
        ff = ff * tmp
        ff = ((vol * (dq * ff).T).T).sum(axis=0)
    return ff
