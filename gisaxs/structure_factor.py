import numpy as np
from .rotation import rotate

def structure_factor(q1, q2, q3, d_space, numelm, orientations = None):

    if not np.shape(d_space) == (3, 3):
        raise TypeError('d_space must be a 3x3 matrix')

    if not np.shape(numelm)[0] == 3:
        raise TypeError('numelm must be a vector of 3')   

    # rotate the q-vectors
    if orientations is None:
        qx,qy,qz = q1.ravel(), q2.ravel(), q3.ravel()
    else:
        qx,qy,qz = rotate(q1, q2, q3, orientations)

    # d-spacing is the set of vectors along which the unit cells repeats
    sf = 1
    for i in range(3):
        if numelm[i] > 1:
            v = d_space[i]
            qd = qx*v[0] + qy*v[1] + qz*v[2]
            ex = np.exp(1j * qd)
            with np.errstate(divide = 'ignore', invalid = 'ignore'):
                sft = (1 - ex**numelm[i])/(1 - ex)
            sft = np.where(np.abs(1 - ex) < 1.0E-10, numelm[i], sft)
            sf *= sft
    return sf

