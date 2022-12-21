
from .common import xp
from .fresnel import propagation_coeffs

def generate_qspace(alpha, theta, alphai, wavelength):

    k0 = 2 * xp.pi / wavelength
    qx = k0 * (xp.cos(alpha) * xp.cos(theta) - xp.cos(alphai))
    qy = k0 *  xp.cos(alpha) * xp.sin(theta) 

    # 4 components of qz
    kzi = k0 * xp.sin(alphai)
    kzf = k0 * xp.sin(alpha)
    qz = xp.array([kzf+kzi, kzf-kzi, -kzf+kzi, -kzf-kzi])
    return qx, qy, qz

