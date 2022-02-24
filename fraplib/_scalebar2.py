from matplotlib import pyplot as plt
import matplotlib.patches as patches

def scalebar2(length, data, ax = None, color = None):
    """
    adds a scale bar to a plot
    
    Parameters
    ----------
    length : number
        desired scale bar length in image pixel units (typically microns)
    data : aicsimageio.aics_image.AICSImage
        source data of image on ax
    ax : matplotlib.axes._subplots.AxesSubplot
        axes object on which to put the scale bar
    color : str
    """
    
    pxsize = data.physical_pixel_sizes.X/10
    yheight = data.dims.Y
    xwidth = data.dims.X
    
    if ax is None:
        ax = plt.gca()
    
    if color is None:
        color = next(ax._get_lines.prop_cycler)['color']
    
    px_length = length/pxsize
    fractional = px_length/xwidth
    
    # build a rectangle in axes coords
    left, width = 0.9 - fractional, fractional
    bottom, height = 0.1, 0.02
    right = left + width
    top = bottom + height

    # axes coordinates: (0, 0) is bottom left and (1, 1) is upper right
    p = patches.Rectangle(
        (left, bottom), width, height,
        facecolor = color, edgecolor = None,
        transform=ax.transAxes
        )

    ax.add_patch(p)