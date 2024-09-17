
import numpy as np

def trapezoid(qx, qy, qz, base, height, angle):

    # half of the base
    y0 = base/2

    # check if angle is feasible
    min_angle = np.arctan2(height, base)
    if angle < min_angle:
        raise ValueError("Angle is too small")
    m = np.tan(angle)

    # calculate the form-factor 
    term1 = np.exp(1j * qy * y0) / qy
    term2 = (np.exp(-1j * height * (qz + qy/m)) - 1) / (qz + qy/m)
    term3 = (np.exp(-1j * qy * y0) / qy
    term4 = (np.exp(-1j * height * (qz - qy/m)) - 1) / (qz - qy/m)
    return term1 * term2 - term3 * term4
