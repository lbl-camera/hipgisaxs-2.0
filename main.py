import os
import json
import h5py

import numpy as np
from collections import OrderedDict

import math as m
import matplotlib.pyplot as plt

from gisaxs import Unitcell
from gisaxs.rotation import rotate
from gisaxs.ff import cuboid, sphere
from gisaxs.fresnel import propagation_coeffs
from gisaxs.structure_factor import structure_factor
from gisaxs.detector import Detector

if __name__ == '__main__':


    # load instrumentation specs
    with open('json/instrument.json') as fp:
        cfg = json.load(fp)

    alphai = cfg['incident_angle'] * np.pi / 180
    sdd = cfg['sdd']
    energy = cfg['energy'] 
    detector = Detector.from_dict(cfg['detector'])

    beam_center = cfg['beam_center'] 

    # load sample description
    with open('json/sample.json') as fp:
       sample = json.load(fp)

    # output
    with open('json/output.json') as fp:
        output = json.load(fp)

    
    # substrate
    substrate = sample['substrate']
    reflectivity_index = complex(substrate['delta'], substrate['beta'])

    # sample 
    unitcell = Unitcell(sample['unitcell'])

    theta, alpha = detector.angles(sdd, beam_center)
    qx, qy, qz = detector.dwba_qvectors(sdd, beam_center, energy, alphai)
    propagation = propagation_coeffs(alphai, alpha.ravel(), reflectivity_index)

    #  sample rotations in plane to simulate incoherant part
    scat = np.zeros(qx.size, dtype=np.csingle)
    
    # struture factor
    dspacing = np.array([[1, 0, 0],[0, 100, 0],[0, 0, 1]])
    repeats = np.array([1, 10000, 1])

    # DWBA
    for j in range(4):
        ff = unitcell.calcff(qx, qy, qz[j])
        sf = structure_factor(qx, qy, qz[j], dspacing, repeats)
        scat += propagation[j] * sf * ff

    img = np.reshape(np.abs(scat)**2, detector.shape)
    
    qp = np.sign(qy) * np.sqrt(qx**2 + qy**2)
    qv = qz[0]
    qrange = [qp.min(), qp.max(), qv.min(), qv.max()]
 

    energy_grp = str(energy)+'ev'
    incident_ang = str(cfg['incident_angle'])
    fname = output['filename']

    fp = h5py.File(fname, 'a')
    dst = os.path.join(energy_grp, incident_ang)
    if not dst in fp:
        fp.create_group(dst)

    # intensities
    if 'I' in fp[dst]:
        dset = fp[os.path.join(dst, 'I')]
        dset[:] = img 
    else:
        dset = fp[dst].create_dataset('I', data = img)
    dset.attrs['qlims'] = [qp.min(), qp.max(), qv.min(), qv.max()]
    fp.close()
 

