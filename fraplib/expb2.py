from symfit import variables, Parameter, Fit
import numpy as np
from .metadatafunctions import get_regions

def fit_expD(xdata, ydata, radius, guesses):
    """
    fitting relevant diffusion parameters directly with inverse exponential decay function substituted with FRAP recovery equation
    
    Parameters
    ----------
    xdata : array
    ydata : array
    file : czifile
    guesses : list
        [amount of bleaching, diffusion coefficient, immobile fraction]
    
    Returns
    -------
    xvals : array
        x values for plotting fit
    curve : array
        y values for plotting fit
    fit_result.params : ordered dict
        estimates of model parameters
    fit_result
        output from symfit, including covariance matrix
    """
    
    x, y = variables('x, y')
    
    # _ , _ , radius = np.asarray(get_regions(file, units = 'microns')[0])/1E-6 # in microns
    r = Parameter('r', value = radius, fixed = True) # radius of region in microns
    amt = Parameter('amt', value = guesses[0]) # amount of bleaching
    D = Parameter('D', value = guesses[1]) # diffusion coefficient
    immfr = Parameter('immfr', value = guesses[2]) # immobile fraction

    thalf = (
        0.224 * (r ** 2) * (D ** -1)
    )
    A = (
        amt - immfr
    )
    yoff = (
        1 - immfr
    )
    model = {
        y: yoff - (A * 2**(-x/(0.224 * (r ** 2) * (D ** -1))))
    }

    fit = Fit(model, xdata, ydata)
    fit_result = fit.execute()
    
    xvals = np.linspace(xdata.min(), xdata.max(), num = 100*len(xdata))
    curve = fit.model(x = xvals, **fit_result.params).output[0]
    
    return xvals, curve, fit_result.params, fit_result

def fit_expb2(xdata, ydata, guesses):
    """
    inverse exponential decay function
    
    Parameters
    ----------
    xdata : array
    ydata : array
    guesses : list
        [A, thalf, yoff]
    
    Returns
    -------
    xvals : array
        x values for plotting fit
    curve : array
        y values for plotting fit
    fit_result.params : ordered dict
        estimates of model parameters
    fit_result
        output from symfit, including covariance matrix
    """
    
    A, thalf, yoff = guesses # unpack
    
    x, y = variables('x, y')
    A = Parameter('A', value = A)
    thalf = Parameter('thalf', value = thalf)
    yoff = Parameter('yoff', value = yoff)
    
    model = { y: yoff - (A * 2**(-x/thalf)) }
    
    fit = Fit(model, xdata, ydata)
    fit_result = fit.execute()
    
    xvals = np.linspace(xdata.min(), xdata.max(), num = 100*len(xdata))
    curve = fit.model(x = xvals, **fit_result.params).output[0]
    
    return xvals, curve, fit_result.params, fit_result