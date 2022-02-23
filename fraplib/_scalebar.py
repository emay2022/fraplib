def scale_bar(length, img, pxsize, cap_style = 'butt', lw = 5, color = None):
    
    xpx = img.shape[-1]
    ypx = img.shape[-2]

    if color is None:
        color = next(ax._get_lines.prop_cycler)['color']
    
    px_length = length/pxsize
    fractional = px_length/xpx
    
    plt.axhline(
        y = ypx*0.9, 
        xmin = 0.9 - fractional, 
        solid_capstyle = cap_style, 
        linewidth = lw, 
        xmax = 0.9, 
        color = color
    )