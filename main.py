import os
import sys

import h5py
import click

import json

import numpy as np

from hipgisaxs import build_instrument, build_sample, setup_experiment, build_output, run_experiment


def setup_experiment(instrument, sample, output):
    # pass in either instrument object or instrument file
    if isinstance(instrument, str):
        instrument = build_instrument(instrument)
    ... # same for sample, output

    experiment = Experiment(instrument, sample, output)

    return experiment


# TODO: consider adding a console_scripts entrypoint to setup.py
@click.command()
@click.argument('instrument')
@click.argument('sample')
@click.argument('output')
def run_experiment(instrument, sample, output):
    # pass in either instrument object or instrument file
    experiment = setup_experiment(instrument, sample)
    data = experiment.run(...)

    if output is not None:
        output.write(data, metadata=experiment.metadata)

    return data


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
    dspacing = np.array([[200, 0, 0], [0, 200, 0], [0, 0, 1]])
    repeats = np.array([500, 500, 1])

    # DWBA
    scat = np.zeros_like(qx, dtype=complex)
    for j in range(4):
        ff = unitcell.ff(qx, qy, qz[j])
        sf = structure_factor(qx, qy, qz[j], dspacing, repeats)
        scat += propagation[j] * sf * ff

    # compute intensity
    img = np.abs(scat.reshape(detector.shape)) ** 2

    # if we have cupy, transfer to numpy
    if np.__name__ == 'cupy':
        img = img.get()

    # write to hdf5
    fname = output['filename']
    fp = h5py.File(fname, 'w')
    dsetname = output['dataset']
    dset = fp.create_dataset(dsetname, data=img)
    qp = np.sign(qy) * np.sqrt(qx ** 2 + qy ** 2)
    qv = qz[0]
    if np.__name__ == 'cupy':
        qp = qp.get()
        qv = qv.get()
    dset.attrs['qlims'] = [qp.min(), qp.max(), qv.min(), qv.max()]
    fp.close()
