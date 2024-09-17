from . import Unitcell
from . import Substrate

class Sample:
    """A class to represent a sample in a GISAXS experiment.

    Attributes:
    unitcell (Unitcell): the unit cell of the sample
    substrate (Layer): the substrate of the sample
    """
    def __init__(self, unitcell = None, substrate = None):
        self._unitcell = unitcell
        self._substrate = substrate

    @property
    def unitcell(self):
        return self._unitcell
    
    @property
    def substrate(self):
        return self._substrate

def build_sample(sample: dict = None, sample_file: str = None) -> Unitcell:

    if sample is not None and isinstance(sample, dict):
        if 'unitcell' in sample:
            unitcell = Unitcell(**sample['unitcell'])
        else:
            raise ValueError('Sample must contain a unitcell')
        
        if 'substrate' in sample:
            substrate = Substrate(**sample['substrate'])
        else:
            raise ValueError('Sample must contain a substrate')

    elif sample_file is not None and isinstance(sample_file, str):
        # check if string is a json file
        if sample_file.endswith('.json'):
            if os.path.isfile(sample_file):
                with open(sample_file) as fp:
                    sample = json.load(fp)
                    if 'unitcell' in sample:
                        unitcell = Unitcell(**sample['unitcell'])
                    else:
                        raise ValueError('Sample must contain a unitcell')
                    
                    if 'substrate' in sample:
                        substrate = Substrate(**sample['substrate'])
                    else:
                        raise ValueError('Sample must contain a substrate')
            else:
                raise OSError('Sample file not found')
    elif sample is None and sample_file is None:
        if os.path.isfile('json/sample.json'):
            with open('json/sample.json') as fp:
                sample = json.load(fp)
                if 'unitcell' in sample:
                    unitcell = Unitcell(**sample['unitcell'])
                else:
                    raise ValueError('Sample must contain a unitcell')
                
                if 'substrate' in sample:
                    substrate = Substrate(**sample['substrate'])
                else:
                    raise ValueError('Sample must contain a substrate')
        else:
            raise ValueError('Unable to build sample from default file')
    return Sample(unitcell, substrate)
