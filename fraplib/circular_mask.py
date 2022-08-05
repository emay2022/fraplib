import numpy as np


def create_circular_mask(expt, roi):
    """
    create a circular mask

    Parameters
    ----------
    data : aicsimageio.aics_image.AICSImage
    roi : dict

    Returns
    -------
    mask : np.ndarray
    """
    data = expt['data']

    h = data.dims.Y
    w = data.dims.X

    center = (roi['X'], roi['Y'])
    radius = roi['R']

    if center is None:  # use the middle of the image
        center = (int(w / 2), int(h / 2))
    if radius is None:  # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w - center[0], h - center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

    mask = dist_from_center <= radius
    return mask


def roi_mask(expt, specific_roi_key=None):
    """
    create a mask based on each roi in the experiment

    Parameters
    ----------
    expt : dict
        output of load_data

    Returns
    -------
    mask : np.ndarray
    """

    data = expt['data']
    roi_dict = expt['roi']

    if specific_roi_key is None:
        if len(roi_dict) > 1:
            mask = {}
            for key in roi_dict:
                h = data.dims.Y
                w = data.dims.X
                center = (roi_dict[key]['CenterX'], roi_dict[key]['CenterY'])
                radius = roi_dict[key]['Radius']

                Y, X = np.ogrid[:h, :w]
                dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

                mask[key] = dist_from_center <= radius
        elif len(roi_dict) == 1:
            for key in roi_dict:
                h = data.dims.Y
                w = data.dims.X
                center = (roi_dict[key]['CenterX'], roi_dict[key]['CenterY'])
                radius = roi_dict[key]['Radius']

                Y, X = np.ogrid[:h, :w]
                dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

                mask = dist_from_center <= radius
        else:
            print('warning: expt["roi"] has unexpected length. No mask created.')

    elif specific_roi_key in roi_dict:
        h = data.dims.Y
        w = data.dims.X
        center = (
            roi_dict[specific_roi_key]['CenterX'],
            roi_dict[specific_roi_key]['CenterY'],
        )
        radius = roi_dict[specific_roi_key]['Radius']

        Y, X = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

        mask = dist_from_center <= radius

    else:
        print('warning: specific_roi_key not in expt["roi"]. No mask created')

    return mask
