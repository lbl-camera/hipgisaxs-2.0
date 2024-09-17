import os
import json
import h5py
import tifffile as tiff

import numpy as np

ENDIAN = {'>': 'big', '<': 'little', '=': 'native'}

class Output:
    def __init__(self, data, metadata: dict = None, outpath: str = '.'):
        self.data = data
        self.metadata = metadata
        self.outpath = outpath

    def hdf5(self, filename, group=None):
        f = os.path.join(self.outpath, filename)
        if group is not None:
            group = 'data'
        with h5py.File(f, 'w') as f:
            dset = f.create_dataset(group, data=self.data)
            dset.attrs.update(self.metadata)

    def tiff(self, filename):
        f = os.path.join(self.outpath, filename)
        tiff.imsave(filename, self.data)

    def json(self, filename):
        # write metadata as well as binary dump to json
        binary = self.data.tobytes()
        data = {
            'dtype': str(self.data.dtype), 
            'shape': self.data.shape, 
            'data': binary, 
            'byteroder': ENDIAN[self.data.dtype.byteorder]
        }
        meta = self.metadata
        meta.update(data)
        with open(filename, 'w') as f:
            json.dump(meta, f)
