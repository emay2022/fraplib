from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np

def make_colormap(rgb):
    """
    creates a new color map from black to white through the specified RGB color
    
    Parameters
    ----------
    rgb : list
        [r = #, g = #, b = #] where # is between 0 and 256
    
    Returns
    -------
    new_cm : mpl.colors.ListedColormap
    """
    
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    N = 256
    vals = np.ones((N, 4))
    vals[:, 0] = np.linspace(0, r/256, N)
    vals[:, 1] = np.linspace(0, g/256, N)
    vals[:, 2] = np.linspace(0, b/256, N)
    ko = ListedColormap(vals)

    N = 256
    vals = np.ones((N, 4))
    vals[:, 0] = np.linspace(r/256, 1, N)
    vals[:, 1] = np.linspace(g/256, 1, N)
    vals[:, 2] = np.linspace(b/256, 1, N)
    ow = ListedColormap(vals)

    top = cm.get_cmap(ko, 128)
    bottom = cm.get_cmap(ow, 128)

    newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                           bottom(np.linspace(0, 1, 128))))
    
    new_cm = ListedColormap(newcolors)
    
    return new_cm

def falsecolor(im, cmap = None):
    
    fig, ax = plt.subplots()
    
    if cmap is not None:
        if isinstance(cmap, ListedColormap) or isinstance(cmap, LinearSegmentedColormap):
            plt.imshow(im, cmap=cmap)
        else:
            cmap = make_colormap(cmap)
            plt.imshow(im, cmap=cmap)
    else:
        plt.imshow(im)
        
    plt.axis("off")
    plt.show()
    plt.close()