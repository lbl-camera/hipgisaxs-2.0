import numpy as np
from scipy.special import j1
from numpy.polynomial.legendre import leggauss

from ..rotation import rotate

def quadrature(func, a, b, args=None, N=10):
    fq = lambda x: func(x) if args is None else func(x, *args)
    nodes, wghts = leggauss(N)
    pts = [(b-a)/2*x+(b+a)/2 for x in nodes]
    return (b-a)/2*sum(w*fq(x) for w,x in zip(wghts, pts))

def cone(qx, qy, qz, R, R1, H, orientation=None):

    tan_a = H / (R - R1)
    if orientation is None:
        q1, q2, q3 = qx.ravel(), qy.ravel(), qz.ravel()
    else:
        q1, q2, q3 = rotate(qx, qy, qz, orientation)

    qp = np.sqrt(q1**2 + q2**2)
    qzp = q3 * tan_a
    t1 = 2 * np.pi * tan_a * np.exp(1j * qzp * R) * dq

    # integrand
    fq = lambda r: r**2*np.exp(-1j*qzp*r)*j1(qp*r)/(qp*r)
    I = quadrature(fq, R, Rh)
    return (t1 * I)
