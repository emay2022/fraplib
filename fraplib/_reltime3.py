import numpy as np
import pandas as pd

def relt(expt, relative_to_time = None):
    """
    creates an array of image acquisition times in seconds relative to the specified time.
    default is to first image acquired.
    
    Parameters
    ----------
    experiment: dict
        output of load_data
    relative_to: float
        a particular time
    
    Returns
    -------
    times : np.ndarray    
    """
    
    sb = expt['sb']
    atch = expt['atch']
    
    # if subblock-specific metadata exists, use it to get time information. Otherwise, use attachment TimeStamps
    if sb['image_metadata'][0] is not None:
        t_list = [
            pd.to_datetime(elem['Tags']['AcquisitionTime'])
            for elem in sb['image_metadata']
        ]
        
        dt_tlist = pd.to_datetime(t_list)
        
        if relative_to_time is None:
            relative_to_index = 0
            dt_reltot = pd.to_datetime(t_list[relative_to_index])
        else:
            dt_reltot = pd.to_datetime(relative_to_time)
        
        times = (dt_tlist - dt_reltot) / pd.Timedelta(seconds=1)
        times = times.to_numpy()
        
    else:
        timestamps = expt['atch']['TimeStamps']
        t = np.asarray(timestamps)
        if relative_to_time is None:
            relative_to_index = 0
            times = t - t[relative_to_index]
        else:
            times = t - relative_to_time
    
    return times