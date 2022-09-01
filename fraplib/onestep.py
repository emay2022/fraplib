from .calculations import evaluate
from .metadatafunctions import get_regions
from .expb2 import fit_expD
from .pretty_plot import pretty_plot

def analyze(czif, name = None):
    """
    One-step analysis of a FRAP experiment.
    
    Parameters
    ----------
    czif : CziFile
    
    Returns
    -------
    fig : matplotlib figure object
    axs : matplotlib axes object
    p : list
        contains ordered dicts of fit params for each region in the experiment
    """
    
    # step 1: get the images
    images = czif.asarray().squeeze()

    # step 2: do all the calculations
    t, n, _, _, _, _, _, _, _ = evaluate(images, czif)

    # step 3: fit post-bleach data to exponential decay with base 2
    xdata = t[t >= 0]
    # ydata = n[t >= 0]
    roi = get_regions(czif, units = 'microns')
    curves = []
    p = []
    fit_results = []
    fitxval = []
    for cnt, region in enumerate(roi):
        radius = region[-1]
        ydata = n[cnt][t >= 0]
        guesses = (0.5, 1, 0.1)
        fitxvals, curve, params, fit_result = fit_expD(xdata, ydata, radius, guesses)
        curves.append(curve)
        p.append(params)
        fit_results.append(fit_result)
        fitxval.append(fitxvals)

    # step 4: plot
    fig, axs = pretty_plot(
        images, 
        xdata = t, ydata = n, 
        fitx = fitxval, fity = curves, 
        experiment = czif,
        name = name
    )
    
    return fig, axs, p