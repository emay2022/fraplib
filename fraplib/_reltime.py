import numpy as np
import czifile
import pandas as pd

def reltimes_fromAttach(file, relative_to = 0):
    """
    converts an array of image acquisition times in seconds to an array of times relative to the first aquisition time by default; relative to the n-th image acquired by specifiying the index of the n-th image in the 'relative_to' argument.
    
    Parameters
    ----------
    file : CziFile
    
    Returns
    -------
    times : np.ndarray
    
    """
    for segment in file.segments():
        if isinstance(segment, czifile.AttachmentSegment):
            if segment.attachment_entry.name == 'TimeStamps':
                timestamps = segment.data()
    
    t = np.asarray(timestamps)
    
    times = t - t[relative_to]
    
    return times

def reltimes_fromSubblocks(subblocks, relative_to = 0):
    """
    creates an array of image acquisition times in seconds relative to the aquisition time of the first image acquired by default; relative to the n-th image acquired by specifiying the index of the n-th image in the 'relative_to' argument.
    
    Parameters
    ----------
    subblocks: dict
        output of load_data; dict with pixel data for each image under key "images" and other info for each image under key "image_metadata"
    relative_to: index
    
    Returns
    -------
    times : np.ndarray
    """
    
    t_list = [
        pd.to_datetime(elem['Tags']['AcquisitionTime'])
        for elem in subblocks['image_metadata']
    ]
    
    dt_tlist = pd.to_datetime(t_list)
    dt_reltot = pd.to_datetime(t_list[relative_to])
    
    times = (dt_tlist - dt_reltot) / pd.Timedelta(seconds=1)
    times = times.to_numpy()
    
    return times