def get_roi(expt):
    """
    gets the regions of interest from the metadata

    Parameters
    ----------
    md : dict
        metadata

    Returns
    -------
    roi : list or dict
    """

    md = expt['md']
    test = md['ImageDocument']['Metadata']['Layers']['Layer']

    if isinstance(test, list):

        roi = []

        for i in range(len(test)):

            x = md['ImageDocument']['Metadata']['Layers']['Layer'][i]['Elements'][
                'Circle'
            ]['Geometry']['CenterX']
            y = md['ImageDocument']['Metadata']['Layers']['Layer'][i]['Elements'][
                'Circle'
            ]['Geometry']['CenterY']
            r = md['ImageDocument']['Metadata']['Layers']['Layer'][i]['Elements'][
                'Circle'
            ]['Geometry']['Radius']

            roi.append({'X': x, 'Y': y, 'R': r})

    else:

        x = md['ImageDocument']['Metadata']['Layers']['Layer']['Elements']['Circle'][
            'Geometry'
        ]['CenterX']
        y = md['ImageDocument']['Metadata']['Layers']['Layer']['Elements']['Circle'][
            'Geometry'
        ]['CenterY']
        r = md['ImageDocument']['Metadata']['Layers']['Layer']['Elements']['Circle'][
            'Geometry'
        ]['Radius']

        roi = {'X': x, 'Y': y, 'R': r}

    return roi


from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse


def draw_circle(roi):
    """
    adds a circle corresponding to roi onto an image

    Parameters
    ----------
    roi: dict
        with keys: {'X': x, 'Y': y, 'R': r}

    Returns
    -------
    circle : matplotlib.patches.Patch
    """

    x = roi['X']
    y = roi['Y']
    r = roi['R']

    circle = plt.Circle((x, y), r, facecolor='none', edgecolor='y', linewidth=1)

    return circle
