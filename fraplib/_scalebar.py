from matplotlib import pyplot as plt

def scalebar(length, data, ax = None, color = None, lw = 1):
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
    lw : float
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
    
    ax.axhline(
        y = yheight*0.9, 
        xmin = 0.9 - fractional, 
        solid_capstyle = 'butt', 
        linewidth = lw, 
        xmax = 0.9, 
        color = color
    )