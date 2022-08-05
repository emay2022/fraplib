import numpy as np


def create_circular_mask(image, circle_geom):
    """
    create a circular mask

    Parameters
    ----------
    image : array
    circle_geom : tuple
        (centerx, centery, radius)

    Returns
    -------
    mask : bool
    """
    w = image.squeeze().shape[-1]
    h = image.squeeze().shape[-2]

    center = (circle_geom[0], circle_geom[1])
    radius = circle_geom[2]

    if center is None:  # use the middle of the image
        center = (int(w / 2), int(h / 2))
    if radius is None:  # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w - center[0], h - center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

    mask = dist_from_center <= radius
    return mask