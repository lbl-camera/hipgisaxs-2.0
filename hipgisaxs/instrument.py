import os
import math
import json
from .detector import Detector

class Instrument:
    def __init__(self, detector = None, distance = 1.0, energy = 1.0e4, incident_angle = 0.2, beam_center = (0,0)):
        self._distance = distance
        self._wavelength = 1239.8/energy
        self._incident_angle = math.radians(incident_angle)
        self._beam_center = beam_center
        if detector is not None:
            self.detector = Detector(**detector)
        else:
            self.detector = Detector()


    @property
    def distance(self):
        return self._distance
    
    @property
    def wavelength(self):
        return self._wavelength
    
    @property
    def incident_angle(self):
        return self._incident_angle
    
    @property
    def beam_center(self):
        return self._beam_center
    

def build_instrument(instrument: dict = None, instrument_file: str = None) -> Instrument:

    if instrument is not None and isinstance(instrument, dict):
        return Instrument(**instrument)
    elif instrument_file is not None and isinstance(instrument_file, str):
        # check if string is a json file
        if instrument_file.endswith('.json'):
            if os.path.isfile(instrument_file):
                with open(instrument_file) as fp:
                    instrument = json.load(fp)
                    return Instrument(**instrument)
            else:
                raise OSError('Instrument file not found')
    elif instrument is None and instrument_file is None:
        if os.path.isfile('json/instrument.json'):
            with open('json/instrument.json') as fp:
                instrument = json.load(fp)
                return Instrument(**instrument)
        else:
            raise ValueError('Unable to build instrument from default file')
