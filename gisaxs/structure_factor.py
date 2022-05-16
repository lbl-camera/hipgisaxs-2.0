
from common import xp
import rotation


def structure_factor(q1, q2, q3, d_space, numelm, rotation = None):

    if not xp.shape(d_space) == (3, 3):
        raise TypeError('d_space must be a 3x3 matrix')

    if not xp.shape(numelm)[0] == 3:
        raise TypeError('numelm must be a vector of 3')   

    if rotation is None:
        rotation = xp.eye(3)
    elif not xp.shape(rotation) == (3,3):
        raise TypeError('rotation must be a 3x3 matrix')

    # rotate the q-vectors
    qx,qy,qz = rotate.rotate(q1, q2, q3, rotation)

    # x-components
    z = xp.exp(-1j * qx * d_space[0,0])
    sfx = (1 - z**numelm[0])/(1 - z)

    if d_space[1,0] != 0:
        z = xp.exp(-1j * qx * d_space[1,0])
        sfx += (1 - z**numelm[0])/(1 - z)

    if d_space[2,0] != 0:
        z = xp.exp(-1j * qx * d_space[2,0])
        sfx += (1 - z**numelm[0])/(1 - z)
    sfx[xp.isnan(sfx)] = 0

    # y-components
    z = xp.exp(-1j * qy * d_space[1,1])
    sfy = (1 - z**numelm[1])/(1 - z)
    if d_space[0,1] != 0:
        z = xp.exp(-1j * qy * d_space[0,1])
        sfy += (1 - z**numelm[1])/(1 - z)

    if d_space[2,1] != 0:
        z = xp.exp(-1j * qy * d_space[2,1])
        sfy += (1 - z**numelm[1])/(1 - z)
    sfy[xp.isnan(sfy)] = 0

    # z-components
    z = xp.exp(-1j * qz * d_space[2,2])
    sfz = (1 - z**numelm[2])/(1 - z)
    if d_space[0,2] != 0:
        z = xp.exp(-1j * qz * d_space[0,2])
        sfz = (1 - z**numelm[2])/(1 - z)

    if d_space[1,2] != 0:
        z = xp.exp(-1j * qz * d_space[1,2])
        sfz += (1 - z**numelm[2])/(1 - z)
    sfz[xp.isnan(sfz)] = 0
    
    return sfx * sfy * sfz

