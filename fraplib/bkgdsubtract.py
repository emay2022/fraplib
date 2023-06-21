import numpy as np
from scipy import ndimage

def bkgdsubtract(ims, labels):
    """
    Background-subtract a segmented image. For each position and channel, averages all the pixels that were not labeleled as cells during segmentation and subtracts that background value from all pixels in the image.
    
    Parameters
    ----------
    ims : numpy array
        image stack of shape (fovs, channels, Y, X)
    labels: array
        mask stack of shape (fovs, Y, X)
    
    Returns
    -------
    bgsub: numpy array
        background-subtracted image stack
    """
    bg = np.zeros_like(ims, dtype='f4')
    for j, fov in enumerate(ims):
        for k, im in enumerate(fov):
            bg[j,k].fill(ndimage.mean(im, labels = labels[j], index = 0))
    bgsub = ims - bg
    return bgsub