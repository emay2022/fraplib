from matplotlib import pyplot as plt
from .metadatafunctions import get_regions, get_scales
from .regions import draw_circle
from .scalebar import scalebar


def pretty_plot(images, xdata, ydata, fitx, fity, experiment, name = None):
    """
    Plot the results of a FRAP experiment nicely
    
    Parameters
    ----------
    images : array
    xdata : array
        timepoints adjusted to t_0 = t_bleach
    ydata : array
        normalized fluorescence data for each timepoint
    fitx : array
        post-bleach timepoints used for fitting
    fity : array
        output curve datapoints from fitting
    experiment : CziFile
        original data file, for metadata
    name : str
        experiment name for figure
    """
    
    fig, axs = plt.subplots(1, 2, dpi=120, figsize=(6.5, 3), layout="constrained")

    left, right = axs
    cyan = (0,1,1)
    dcyan = (0,0.8, 0.8)
    gray = 3*(0.7,)

    for cnt, series in enumerate(ydata):
        right.scatter(xdata[xdata >= 0], series[xdata >= 0], label="data", color = cyan)
        right.plot(fitx[cnt], fity[cnt], label="fit", color = dcyan)
        right.scatter(xdata, series, label="normalization data", color=gray, zorder = 0)
        
    right.axhline(
        y=1, color='k', zorder=-1, label="normalization factor"
    )
    left.set_title("FRAP", color="gray")
    right.set_xlabel("time (seconds)")
    right.set_ylabel("normalized fluorescence")
    # right.legend(loc = 'lower right', frameon = False)

    limits = (images[xdata >= 0, ...][0].min(), images[xdata >= 0, ...][0].max())
    from mpl_interactions import hyperslicer
    ctrls = hyperslicer(
        images,
        ax=left,
        names=["frame"],
        play_buttons=True,
        cmap="gray",
        vmin=limits[0],
        vmax=limits[1],
    )
    left.set_axis_off()
    circle = get_regions(experiment)
    for region in circle:
        draw_circle(region, ax=left, color=cyan, linewidth=1)
    scales = get_scales(experiment)
    scalebar(20, images, scales, color="w", label_on=True, ax=left)
    if name is not None:
        left.set_title(name, color="gray")

    plt.show()
    
    return fig, axs