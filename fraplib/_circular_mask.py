import numpy as np

def create_circular_mask(h, w, center=None, radius=None):
    """
    create a circular mask
    
    Parameters
    ----------
    h: float
        image height in pixels
    w: float
        image width in pixels
    center: tuple
        (center x position in pixels, center y position in pixels)
    radius: float
        radius of the circle in pixels
        
    Returns
    -------
    mask : np.ndarray
    """
    
    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask