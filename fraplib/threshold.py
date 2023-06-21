import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import xarray as xr

def threshold(avgs, channels, channel_control_samples, Q = 0.995):
    """
    Compute channel-wise thresholds.
    
    Parameters
    ----------
    avgs : pd Series
    channels: list
    channel_control_samples: list
    Q: float
    
    Returns
    -------
    threshold: pd Series
    """
    
    threshold = pd.Series(dtype='f4')
    fig, axs = plt.subplots(1,2,layout = 'constrained', figsize = (8, 3.5), sharey = True)

    chs = channels[:-1]
    
    chclr = {'Alexa Fluor 546' : 'm', 'Cy5' : 'm', 'EGFP' : 'c', 'mCherry' : 'r'}
    
    clrs = [chclr[ch] for ch in chs]
    
    sels = channel_control_samples
    # sels = [
    #     list(ximages.S.values[6:]), # samples with no AF546 fluorescence
    #     [s for s in ximages.S.values if 'noFP' in s] # samples with no EGFP fluorescence
    # ]

    for a, channel, sel, c in zip(np.arange(len(chs)), chs,sels,clrs):

        rangemin = avgs.loc[pd.IndexSlice[sel,channel]].min()
        rangemax = avgs.loc[pd.IndexSlice[sel,channel]].max()

        for s in sel:
            axs[a].hist(avgs.loc[pd.IndexSlice[s,channel]],
                        bins = 100,
                        range=(rangemin, rangemax),
                        alpha = 1/(3*len(sel)),
                        label = s,
                        color = c,)
                       # density = True)

        threshold[channel] = avgs.loc[pd.IndexSlice[sel,channel]].quantile(Q)

        axs[a].axvline(threshold[channel], color = 'k')
        axs[a].semilogy()
        # ax[a].legend()
        axs[a].set_title(f'{channel}')
        axs[a].set_xlabel(f'Mean cell intensity in {channel} channel')
        if a ==0:
            axs[a].set_ylabel('Number of cells\n(log scale)')
    plt.suptitle('Negative control histograms for thresholding')
    # plt.savefig(o+'thresholding.svg', dpi = 300)
    plt.show()
    
    return threshold