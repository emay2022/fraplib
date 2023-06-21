import numpy as np

def bkgdsubtract(ims):
    bgsub = np.zeros_like(ims, dtype='f4')
    for j, fov in enumerate(ims):
        for k, im in enumerate(fov):
            bgsub[j,k].fill(ndimage.mean(im, labels = labels[j], index = 0))
    return ims - bgsub