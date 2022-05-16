#! /usr/bin/env python

from common import xp
from common import j1

def sphere(qx, qy, qz, radius, shift = None):

    if shift is not None:
        qd = xp.exp(j1 * (qx * shift[0] + qy * shift[1] * qz * shift[2]))
    else:
        qd = 1.

    vol = 4 * xp.pi * radius**3
    qR = xp.sqrt(xp.power(qx,2) + xp.power(qy,2) + xp.power(qz,2)) * radius
    tmp = xp.exp(-1j * qz * radius)
    return  qd * vol * tmp *  (xp.sin(qR) - qR * xp.cos(qR)) / qR**3
