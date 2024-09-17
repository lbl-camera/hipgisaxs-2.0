
# This file contains the Detector class which is used to define the detector

import numpy as np
from numpy import cos, sin

class Detector:
    """
    @brief The detector is defined by the name, shape, and pixel size.  It is used to 
    calculate the q-vectors and q-values for the detector.

    Parameters:
        name: name of the detector
        shape: shape of the detector (nrow, ncol)
        pixle_size: pixel size of the detector (dx, dy)
    """
    
    def __init__(self, name = 'Pilatus1M', shape = (981, 1043), pixle_size = (0.172, 0.172)):
        self.name = name
        self.shape = shape
        self.pixle_size = pixle_size

    def angles(self, sdd, center):
        """
        Calculate the angles from the center of the sample to the detector.
    
        Parameters:
            sdd: sample to detector distance
            center: center of beam on the detector
        """
        nrow = self.shape[0]
        ncol = self.shape[1]
        y, x = np.mgrid[0:nrow, 0:ncol]

        # shift coordinate with center
        x = (x - center[0]) * self.pixle_size[0]
        y = (y - center[1]) * self.pixle_size[1]

        # angles 
        tmp = np.sqrt(x**2 + sdd**2)
        theta = np.arcsin(x/tmp)
        alpha = np.arctan2(y, tmp)
        return theta, alpha

    def qvectors(self, sdd, center, energy):
        """
        Calculate the q-vectors for the detector.

        Parameters:
            sdd: sample to detector distance
            center: center of beam on the detector
            energy: energy of the x-ray

        Returns:
            qx, qy, qz: q-vectors for the detector
        """

        wavelen = 1.23094e+03 / energy
        theta, alpha = self.angles(sdd, center)
        theta = theta.ravel()
        alpha = alpha.ravel()

        # radius of Ewald's sphere
        k0 = 2 * np.pi / wavelen

        # q-vector
        qx = k0 * (cos(alpha) * cos(theta) - 1)
        qy = k0 * (cos(alpha) * sin(theta))
        qz = k0 * (sin(alpha))
        return qx, qy, qz

    def qvalues(self, sdd, center, energy):
        """
        Calculate the q-values for the detector.

        Parameters:
            sdd: sample to detector distance
            center: center of beam on the detector
            energy: energy of the x-ray

        Returns:
            q: q-values for the detector
        """

        wavelen = 1230.94 / energy
        q = self.qvectors(sdd, center, wavelen)
        return np.linalg.norm(q, axis=1)


    def dwba_qvectors(self, sdd, center, energy, alphai):
        """
        Calculate the q-vectors, including the four qz-components, for the experimental geometry.

        Parameters:
            sdd: sample to detector distance
            center: center of beam on the detector
            energy: energy of the x-ray
            alphai: incident angle

        Returns:
            qx, qy, [qz1...qz4]: q-vectors for the detector
        """

        theta, alpha = self.angles(sdd, center)
        theta = theta.ravel()
        alpha = alpha.ravel()

        wavelen = 1230.94 / energy

        # radius of the Ewald's sphere
        k0 = 2 * np.pi / wavelen

        # q-vector
        qx = k0 * (cos(alpha) * cos(theta) - cos(alphai))
        qy = k0 * (cos(alpha) * sin(theta))
        kzf = k0 * sin(alpha)
        kzi = -k0 * sin(alphai)

        # (Ti, Tf)
        q1 = kzf - kzi

        # (Ri, Tf)
        q2 = kzf + kzi

        # (Ti, Rf)
        q3 = -kzf - kzi

        # (Ri, Rf)
        q4 = -kzf + kzi

        return qx, qy, [q1, q2, q3, q4]
        
