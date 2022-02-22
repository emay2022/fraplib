import numpy as np
import czifile
import pandas as pd

def reltimes(file, relative_to = 0):
    """
    creates an array of image acquisition times in seconds relative to the aquisition time of the first image acquired by default; relative to the n-th image acquired by specifiying the index of the n-th image in the 'relative_to' argument.
    
    Parameters
    ----------
    file: CziFile
        output of load_data; dict with pixel data for each image under key "images" and other info for each image under key "image_metadata"
    relative_to: index
    
    Returns
    -------
    times : np.ndarray
    """
    
    subblocks = {
        "images": [
            segment.data()
            for segment in file.segments()
            if isinstance(segment, czifile.SubBlockSegment)
        ],
        "image_metadata": [
            segment.metadata()
            for segment in file.segments()
            if isinstance(segment, czifile.SubBlockSegment) 
        ],
    }
    
    # if subblock-specific metadata exists, use it to get time information. Otherwise, use attachment TimeStamps
    if subblocks['image_metadata'][0] is not None:
        t_list = [
            pd.to_datetime(elem['Tags']['AcquisitionTime'])
            for elem in subblocks['image_metadata']
        ]
        
        dt_tlist = pd.to_datetime(t_list)
        dt_reltot = pd.to_datetime(t_list[relative_to])

        times = (dt_tlist - dt_reltot) / pd.Timedelta(seconds=1)
        times = times.to_numpy()
        
    else:
        for segment in file.segments():
            if isinstance(segment, czifile.AttachmentSegment):
                if segment.attachment_entry.name == 'TimeStamps':
                    timestamps = segment.data()
        
        t = np.asarray(timestamps)
        
        times = t - t[relative_to]
    
    return times