from matplotlib import pyplot as plt
import matplotlib.patches as patches

def draw_circle(roi, ax = None, color = None, **kwargs):
    """
    adds a circle corresponding to roi onto an image

    Parameters
    ----------
    roi : tuple
        (centerX, centerY, radius)

    Returns
    -------
    circle : matplotlib.patches.Patch
    """
    
    if ax is None:
        ax = plt.gca()
    
    if color is None:
        color = next(ax._get_lines.prop_cycler)['color']
    
    x = roi[0]
    y = roi[1]
    r = roi[2]

    c = patches.Circle((x, y), r, facecolor='none', edgecolor=color, **kwargs)
    
    ax.add_patch(c)