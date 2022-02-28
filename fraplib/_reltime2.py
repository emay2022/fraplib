import numpy as np
import pandas as pd

def reltimes(expt, relative_to = 0):
    """
    creates an array of image acquisition times in seconds relative to the aquisition time of the first image acquired by default; relative to the n-th image acquired by specifiying the index of the n-th image in the 'relative_to' argument.
    
    Parameters
    ----------
    experiment: dict
        output of load_data
    relative_to: index
    
    Returns
    -------
    times : np.ndarray
    """
    
    data = expt['data']
    md = expt['md']
    sb = expt['sb']
    atch = expt['atch']
    
    # if subblock-specific metadata exists, use it to get time information. Otherwise, use attachment TimeStamps
    if sb['image_metadata'][0] is not None:
        t_list = [
            pd.to_datetime(elem['Tags']['AcquisitionTime'])
            for elem in sb['image_metadata']
        ]
        
        dt_tlist = pd.to_datetime(t_list)
        dt_reltot = pd.to_datetime(t_list[relative_to])

        times = (dt_tlist - dt_reltot) / pd.Timedelta(seconds=1)
        times = times.to_numpy()
        
    else:
        timestamps = expt['atch']['TimeStamps']
        t = np.asarray(timestamps)
        times = t - t[relative_to]
    
    return times

def bleach_time(expt):
    """
    
    """
        
    data = expt['data']
    md = expt['md']
    sb = expt['sb']
    atch = expt['atch']