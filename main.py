import os
import sys
import json
import h5py

import numpy as np
from collections import OrderedDict

import matplotlib.pyplot as plt

from hipgisaxs import Unitcell
from hipgisaxs.rotation import rotate
from hipgisaxs.ff import cuboid, sphere
from hipgisaxs.fresnel import propagation_coeffs
from hipgisaxs.structure_factor import structure_factor
from hipgisaxs.detector import Detector

if __name__ == '__main__':


    # load instrumentation specs
    if len(sys.argv) == 2:
        if os.path.isdir(sys.argv[1]):
            input_sdir = sys.argv[1]
    elif len(sys.argv):
        if os.path.isdir('json'):
            input_sdir = 'json'
    
    
    # read configurations
    instrument_config = os.path.join(input_sdir, 'instrument.json')
    if not os.path.isfile(instrument_config):
        raise OSError('experiment config. not found.')
    with open(instrument_config) as fp:
        cfg = json.load(fp)

    # load sample description
    sample_config = os.path.join(input_sdir, 'sample.json') 
    if not os.path.isfile(sample_config):
        raise OSError('sample file not found')
    with open(sample_config) as fp:
       sample = json.load(fp)

    # output
    output_config = os.path.join(input_sdir, 'output.json')
    if not os.path.isfile(output_config):
        raise OSError('outout config not found')
    with open(output_config) as fp:
        output = json.load(fp)


    alphai = cfg['incident_angle'] * np.pi / 180
    sdd = cfg['sdd']
    energy = cfg['energy'] 

    detector = Detector.from_dict(cfg['detector'])
    beam_center = cfg['beam_center'] 

    
    # substrate
    substrate = sample['substrate']
    reflectivity_index = complex(substrate['delta'], substrate['beta'])

    # sample 
    unitcell = Unitcell(sample['unitcell'])

    theta, alpha = detector.angles(sdd, beam_center)
    qx, qy, qz = detector.dwba_qvectors(sdd, beam_center, energy, alphai)
    propagation = propagation_coeffs(alphai, alpha.ravel(), reflectivity_index)

    # struture factor
    dspacing = np.array([[200, 0, 0],[0, 200, 0],[0, 0, 1]]) 
    repeats = np.array([500, 500, 1])

   
    # DWBA
    scat = np.zeros_like(qx, dtype=complex)
    for j in range(4):
        ff = unitcell.ff(qx, qy, qz[j])
        scat += propagation[j] * ff
    img = np.abs(scat.reshape(detector.shape))**2 

    # write to hdf5
    fname = output['filename']
    fp = h5py.File(fname, 'w')
    dsetname = output['dataset']
    dset = fp.create_dataset(dsetname, data = img)
    qp = np.sign(qy) * np.sqrt(qx**2 + qy**2)
    qv = qz[0]
    dset.attrs['qlims'] = [qp.min(), qp.max(), qv.min(), qv.max()]
    fp.close()
