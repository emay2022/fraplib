def time_stamp(frame, timestamps, fsize = 16, t_units = 'sec', ax = None, color = None):
    
    if ax is None:
        ax = plt.gca()

    if color is None:
        color = next(ax._get_lines.prop_cycler)['color']
    
    t = round(timestamps[frame])
    
    if t_units == 'sec':
        time = str(round(t))
        t_str = 't = '+time+' sec'
    elif t_units == 'min':
        time = str(round(t/60))
        t_str = 't = '+time+' min'
    
    plt.annotate(
        t_str, 
        (0.1, 0.1), 
        xycoords = 'axes fraction', 
        color = color, 
        size = fsize
    )