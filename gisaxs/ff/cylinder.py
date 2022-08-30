#! /usr/bin/env python

from common import xp
from common import j1
from rotation import rotate

def cylinder(qx, qy, qz, radius, height, orientation = None, shift = None):

    # output shape
    if shift is not None:
        o_shape = (shift.shape[1], qx.shape[0], qx.shape[1])
    else:
        o_shape = (1, qx.shape[0], qx.shape[1])

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
    qpR = (xp.sqrt(q2**2 + q3**2).T * radius).T

    ff =  xp.sinc((q1.T * height).T)
    ff = ff * j1(qpR) / qpR
    ff = ff * xp.exp(-1j * xp.outer(radius, qz.ravel()))
    ff = (vol * (dq * ff).T).T
    return ff.sum(axis=0)
