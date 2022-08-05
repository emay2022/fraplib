from matplotlib import pyplot as plt


def timestamp(frame, timestamps, fsize=6, t_units='sec', ax=None, color=None):
    """
    adds a time stamp to an image

    Parameters
    ----------
    frame : index
    timestamps : array
    fsize : int or float
    t_units : str
        'sec' or 'min'
    ax: matplotlib.axes._subplots.AxesSubplot
    """

    if ax is None:
        ax = plt.gca()

    if color is None:
        color = next(ax._get_lines.prop_cycler)['color']

    t = round(timestamps[frame])

    if t_units == 'sec':
        time = str(round(t))
        t_str = time + ' sec'
    elif t_units == 'min':
        time = str(round(t / 60))
        t_str = time + ' min'

    ax.annotate(t_str, (0.1, 0.1), xycoords='axes fraction', color=color, size=fsize)
