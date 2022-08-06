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
    
    """
    
    x, y = variables('x, y')
    
    # _ , _ , radius = np.asarray(get_regions(file, units = 'microns')[0])/1E-6 # in microns
    r = Parameter('r', value = radius, fixed = True) # radius of region in microns
    amt = Parameter('amt', value = guesses[0]) # amount of bleaching
    D = Parameter('D', value = guesses[1]) # diffusion coefficient
    immobile = Parameter('immobile', value = guesses[2]) # immobile fraction

    thalf = (
        0.224 * (r ** 2) * (D ** -1)
    )
    A = (
        amt - immobile
    )
    yoff = (
        1 - immobile
    )
    model = {
        y: yoff - (A * 2**(-x/(0.224 * (r ** 2) * (D ** -1))))
    }

    fit = Fit(model, xdata, ydata)
    fit_result = fit.execute()

    curve = fit.model(x = xdata, **fit_result.params).output[0]
    
    return curve, fit_result.params, fit_result

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
    y : array
        calculated f(x) values
    """
    
    A, thalf, yoff = guesses # unpack
    
    x, y = variables('x, y')
    A = Parameter('A', value = A)
    thalf = Parameter('thalf', value = thalf)
    yoff = Parameter('yoff', value = yoff)
    
    model = { y: yoff - (A * 2**(-x/thalf)) }
    
    fit = Fit(model, xdata, ydata)
    fit_result = fit.execute()
    
    curve = fit.model(x = xdata, **fit_result.params).output[0]
    
    return curve, fit_result.params