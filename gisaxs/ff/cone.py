import numpy as np
from scipy.special import j1
from numpy.polynomial.legendre import leggauss

from ..rotation import rotate

def quadrature(func, a, b, args=None, N=10):
    fq = lambda x: func(x) if args is None else func(x, *args)
    nodes, wghts = leggauss(N)
    pts = [(b-a)/2*x+(b+a)/2 for x in nodes]
    return (b-a)/2*sum(w*fq(x) for w,x in zip(wghts, pts))

def trapaziod(func, a, b, args=None, N=100):
    fq = lambda x: func(x) if args is None else func(x, *args)
    dx = (b-a)/N
    I = fq(a) + fq(b)
    for i in range(1, N):
        x = a + i * dx
        I += 2*fq(x)
    return (I*dx/2)


def cone(qx, qy, qz, R, H, alpha, orientation=None, shift=None):

    tan_a = np.tan(alpha)
    Rh = R - H / tan_a
    if not Rh > 0:
        raise ValueError('invalid cone angle')

    if orientation is None:
        q1, q2, q3 = qx.ravel(), qy.ravel(), qz.ravel()
    else:
        q1, q2, q3 = rotate(qx, qy, qz, orientation)

    if shift is not None:
        dq = np.exp(1j * shift[0] * qx.ravel())
        dq += np.exp(1j * shift[1] * qy.ravel())
        dq += np.exp(1j * shift[2] * qz.ravel())
    else:
        dq = 1

    qp = np.sqrt(q1**2 + q2**2)
    qzp = q3 * tan_a

    t1 = 2 * np.pi * tan_a * np.exp(1j * qzp * R) * dq

    # integrand
    fq = lambda r: r**2*np.exp(-1j*qzp*r)*j1(qp*r)/(qp*r)
    I = quadrature(fq, R, Rh)
    return (t1 * I)


def cone_shell(qx, qy, qz, R, H, alpha, t, orientation=None, shift=None):
    ff_inner = cone(qx, qy, qz, R, H, alpha, orientation, shift)
    ff_outer = cone(qx, qy, qz, R+t, H+t, alpha, orientation, shift)
    return (ff_outer-ff_inner)


