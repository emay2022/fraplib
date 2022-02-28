import numpy as np

def relt(expt, relative_to_time = None):
    """
    creates an array of image acquisition times in seconds relative to the specified time.
    default is to bleach end (if bleach exists) or first image acquired.
    
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

    atch = expt['atch']
    
    timestamps = expt['atch']['TimeStamps']
    t = np.asarray(timestamps)
    
    if relative_to_time is None:
        if 'EventList' in atch and 'BLEACH_STOP' in atch['EventList']['event type']:
            time = atch['EventList']['event time'][
                atch['EventList']['event type'].index('BLEACH_STOP')
            ]
            times = t - time
        else:
            relative_to_index = 0
            times = t - t[relative_to_index]
    else:
        times = t - relative_to_time
    
    return times

def postbleach(expt):
    """
    """
    
    times = relt(expt)
    
    use_times = times[times >= 0]
    
    return use_times

def prebleach(expt):
    """
    """
    
    times = relt(expt)
    
    use_times = times[times < 0]
    
    return use_times