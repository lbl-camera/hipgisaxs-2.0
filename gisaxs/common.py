try:
    import NOTWROKINGcupy as xp
    from cupyx.scipy.special import j1
    array_type = "cupy"
except ImportError:
    import numpy as xp
    from scipy.special import j1
    array_type = "numpy"

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


    

    
