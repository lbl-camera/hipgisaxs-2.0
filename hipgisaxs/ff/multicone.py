import numpy as np
from scipy.special import j1
from .cone import cone

from ..rotation import rotate

def cone_stack(qx, qy, qz, R, H, angles, orientation=None):

    if orientation is None:
        q1, q2, q3 = qx.ravel(), qy.ravel(), qz.ravel()
    else:
        q1, q2, q3 = rotate(qx, qy, qz, orientation)

    ff = np.zeros_like(q1, dtype=complex)
    for i, ang in enumerate(angles):
        f1 = cone(q1, q2, q3, R, H, ang)
        d1 = np.exp(1j * q3 * i * H)
        ff += (d1 * f1)
    return ff


def cone_shell(qx, qy, qz, R1, R2, H, angle1, angle2, orientation=None):

    if orientation is None:
        q1, q2, q3 = qx.ravel(), qy.ravel(), qz.ravel()
    else:
        q1, q2, q3 = rotate(qx, qy, qz, orientation)

    f1 = cone(q1, q2, q3, R1, H, angle1)
    f2 = cone(q1, q2, q3, R2, H, angle2)
    return (f1-f2)
