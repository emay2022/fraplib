import numpy as np
from .attachments import get_events, get_timepoints
from .metadatafunctions import get_regions
from .circular_mask import create_circular_mask

def evaluate(imageseries, datafile, background = None, mask = None, bleachequiv = None):
    """
    Raw data processing for FRAP timeseries.
    
    Workflow:
        background subtraction
        average pixels in bleached region at each timepoint (m)
        average signal for timepoints before bleach (normalization factor)
        normalize signal at each time point relative to normalization factor (n)
        
    Parameters
    ----------
    imageseries : array
    datafile : CziFile
    background : number
        value to use for background subtraction
    mask : bool
        same shape as images; True for pixels in bleach region
    bleachequiv : int
        number of frames to average for normalization when there is no bleach
    
    Returns
    -------
    tpost : array
        time points after bleach
    npost : array
        normalized signal for data points after bleach
    t : array
        all time points relative to t_0 which corresponds to t_bleach
    n : array
        all normalized data points
    traw : array
        all time points as extracted from the metadata
    bleach : float
        time point at which bleach occurred
    normfactor: float
        value to use for data normalization
    m : array
        average signal in bleach region
    bsim : array
        background subtracted image series
    mask : bool
        same shape as images; True for pixels in bleach region
    background : number
        value to use for background subtraction
    pre : bool
        same shape as t; True corresponding to t before bleach
    post : bool
        same shape as t; True corresponding to t after bleach
    """
    
    if background is None:
        background = 0
    
    # time and events
    if bleachequiv is None:
        bleach = get_events(datafile)['BLEACH_START']
    else:
        bleach = 0
        nnorm = bleachequiv # number of frames to average for normalization when there is no bleach
    
    t, traw = get_timepoints(datafile)
    pre = traw < bleach # bool
    post = traw > bleach # bool
    
    tpost = t[post]
    tpre = t[pre] - tpost.min()
    t -= tpost.min()
    tpost -= tpost.min()
    
    # background subtraction
    bsim = imageseries - background # background-subtracted image
    
    
    if mask is None:
        circle = get_regions(datafile)
        m = []
        normfactor = []
        n = []
        npost = []
        for counter, region in enumerate(circle):
            if isinstance(region, tuple):
                mask = create_circular_mask(imageseries, region)

                # averaging pixels in bleach region
                m.append(bsim[...,mask].mean(axis = -1)) # list of arrays; mean of px in each bleached region for each timepoint

                # normalization
                if bleachequiv is None:
                    normfactor.append(m[counter][pre].mean())
                else:
                    normfactor.append(m[counter][0:bleachequiv-1].mean())
                n.append(m[counter]/normfactor[counter]) # all the datapoints
                npost.append(m[counter][post]/normfactor[counter]) # just the datapoints after the bleach
    
    return t, n, traw, bleach, normfactor, m, bsim, mask, background