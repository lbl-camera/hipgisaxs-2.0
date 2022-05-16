try:
    import cupy as xp
    from cupyx.scipy.special import j1
    array_type = xp._core.core.ndarray
except ImportError:
    import numpy as xp
    from scipy.special import j1
    array_type = xp.ndarray

def memcopy_to_device(host_pointers):

    for key, value in host_pointers.items(): 
        if type(value) is dict: 
            memcopy_to_host(value) #this handles dictionaries of dictionaries
        elif value is not None:
            host_pointers[key] = cp.asarray(value)

def memcopy_to_host(device_pointers):

    for key, value in device_pointers.items():
        if type(value) is dict: 
            memcopy_to_host(value) #this handles dictionaries of dictionaries
        elif value is not None:
            device_pointers[key] = cp.asnumpy(value)  


    

    
