import numpy as np

def _extract(data, mask):
    """
    defines pixels within the roi
    
    Parameters
    ----------
    data: aicsimageio.aics_image.AICSImage
    mask: np.ndarray
    
    Returns
    -------
    extract: np.ndarray
    
    """
    
    images = data.data # np.ndarray
    
    extract = images*mask # np.ndarray; same shape as images
    
    return extract

def _sum_extract(data, mask):
    """
    sums roi pixel values across x and y for all T, C, Z
    
    Parameters
    ----------
    data: aicsimageio.aics_image.AICSImage
    mask: np.ndarray
    
    Returns
    -------
    sum_inside: np.ndarray
    """
    
    extract = _extract(data, mask)
    
    sum_inside = extract.sum(axis = (-1,-2))
    
    return sum_inside

def _mean_extract(data, mask):
    """
    gets average roi pixel value for all T, C, Z
    
    Parameters
    ----------
    data: aicsimageio.aics_image.AICSImage
    mask: np.ndarray
    
    Returns
    -------
    mean_inside: np.ndarray
    """
    
    sum_inside = _sum_extract(data, mask)
    px_inside = np.sum(mask)
    mean_inside = sum_inside/px_inside
    
    return mean_inside

def _norm_extract(data, mask):
    """
    normalizes average roi pixel value all T, C, Z to average roi pixel value of pre-bleach frame (T[0])
    
    Parameters
    ----------
    data: aicsimageio.aics_image.AICSImage
    mask: np.ndarray
    
    Returns
    -------
    norm_inside: np.ndarray
    """
    
    mean_inside = _mean_extract(data, mask)
    norm_inside = mean_inside/mean_inside[0,:,:]
        
    return norm_inside

def get_data_for_fit(data, mask):
    """
    exlucdes pre-bleach frame (T[0]) from the array
    
    Parameters
    ----------
    data: aicsimageio.aics_image.AICSImage
    mask: np.ndarray
    
    Returns
    -------
    data_for_fit: np.ndarray
    """
    
    norm_inside = _norm_extract(data, mask)
    data_for_fit = norm_inside[1:,:,:]
    
    return data_for_fit