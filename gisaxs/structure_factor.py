
from .common import xp
from .rotation import rotate


def structure_factor(q1, q2, q3, d_space, numelm, orientations = None):

    if not xp.shape(d_space) == (3, 3):
        raise TypeError('d_space must be a 3x3 matrix')

    if not xp.shape(numelm)[0] == 3:
        raise TypeError('numelm must be a vector of 3')   

    # rotate the q-vectors
    if orientations is None:
        qx, qy, qz = q1.ravel(), q2.ravel(), q3.ravel()
    else:
        qx,qy,qz = rotate(q1, q2, q3, orientations)

    nx, ny, nz = numelm
    # x-components
    if nx > 0:
        z = xp.exp(-1j * qx * d_space[0,0])
        sfx = (1 - z**nx)/(1 - z)
        if d_space[1,0] != 0:
            z = xp.exp(-1j * qy * d_space[1,0])
            sfx += (1 - z**nx)/(1 - z)
        if d_space[2,0] != 0:
            z = xp.exp(-1j * qz * d_space[2,0])
            sfx += (1 - z**nx)/(1 - z)
        sfx[xp.isnan(sfx)] = 1
    else:
        sfx = 1

    # y-components
    if ny > 0:
        z = xp.exp(-1j * qy * d_space[1,1])
        sfy = (1 - z**numelm[1])/(1 - z)
        if d_space[0,1] != 0:
            z = xp.exp(-1j * qx * d_space[0,1])
            sfy += (1 - z**numelm[1])/(1 - z)
        if d_space[2,1] != 0:
            z = xp.exp(-1j * qz * d_space[2,1])
            sfy += (1 - z**numelm[1])/(1 - z)
        sfy[xp.isnan(sfy)] = 1
    else:
        sfy = 1

    # z-components
    if nz > 0:
        z = xp.exp(-1j * qz * d_space[2,2])
        sfz = (1 - z**numelm[2])/(1 - z)
        if d_space[0,2] != 0:
            z = xp.exp(-1j * qx * d_space[0,2])
            sfz = (1 - z**numelm[2])/(1 - z)
        if d_space[1,2] != 0:
            z = xp.exp(-1j * qt * d_space[1,2])
            sfz += (1 - z**numelm[2])/(1 - z)
        sfz[xp.isnan(sfz)] = 1
    else:
        sfz = 1
    
    return sfx * sfy * sfz

