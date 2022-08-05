import matplotlib.patches as patches
from matplotlib import pyplot as plt


def scalebar(length, scales, dims, ax=None, color=None, label_on = False, **kwargs):
    """
    adds a scale bar to a plot

    Parameters
    ----------
    length : number
        desired scale bar length in image pixel units (typically microns)
    scales : list
        [x µm/px, y µm/px, z µm/px]
    dims : list
        [x px, y px]
    ax : matplotlib.axes._subplots.AxesSubplot
        axes object on which to put the scale bar
    color : str
        color of the scalebar
    label_on : bool
        text label under the scale bar on/off
    **kwargs : dict
        keyword arguments to pass to matplotlib.patches.Rectangle()
    
    Returns
    -------
    """

    pxsize = scales[0] # x µm/px
    xpx = dims[0]
    ypx = dims[1]

    if ax is None:
        ax = plt.gca()

    if color is None:
        color = next(ax._get_lines.prop_cycler)['color']

    px_length = length / pxsize
    fractional = px_length / xpx

    # build a rectangle in axes coords
    left, width = 0.9 - fractional, fractional
    bottom, height = 0.1, 0.02
    right = left + width
    top = bottom + height

    # axes coordinates: (0, 0) is bottom left and (1, 1) is upper right
    p = patches.Rectangle(
        (left, bottom),
        width,
        height,
        facecolor=color,
        edgecolor=None,
        transform=ax.transAxes,
    )

    ax.add_patch(p)
    
    if label_on:
        ax.text(left + fractional/2, bottom - bottom/2, r'$'+str(length)+'\ µm$',
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes,
                color = color
               )