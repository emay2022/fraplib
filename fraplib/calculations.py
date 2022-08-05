import numpy as np
from .attachments import get_events, get_timepoints
from .metadatafunctions import get_regions
from .circular_mask import create_circular_mask

def evaluate(imageseries, datafile, background = None, mask = None, bleachequiv = None):
    """
    """
    
    if background is None:
        background = 0
    
    if mask is None:
        circle = get_regions(datafile)[0]
        mask = create_circular_mask(imageseries, circle)
    
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
    tpost -= tpost.min()
    
    # background subtraction
    bsim = imageseries - background # background-subtracted image
    
    # averaging pixels in bleach region
    m = bsim[...,mask].mean(axis = -1) # mean of px in bleached region for each timepoint
    
    # normalization
    if bleachequiv is None:
        normfactor = m[pre].mean()
    else:
        normfactor = m[0:bleachequiv-1].mean()
    n = m/normfactor # all the datapoints
    npost = m[post]/normfactor # just the datapoints after the bleach
    
    return tpost, npost, tpre, t, n, normfactor, m, bsim