from scipy.optimize import curve_fit
import numpy as np

def exp(x, a, tau, xoff = 0, yoff = 1):
    """
    exponential decay funtion
    
    Parameters
    ----------
    x: np.ndarray
        x-values
    a: float
        amplitude
    tau: float
        decay rate parameter
    xoff: float
        x-shift from x = 0 (yoff > 0 => right; y off < 0 => left)
    yoff: float
        y-shift from y = 0 (yoff > 0 => up; y off < 0 => down)
    """
    
    return a * np.exp(-(x-xoff)/tau) + yoff

def fit_params(data_x, data_y):
    """
    
    """
    
    function = exp
    
    ig = [-0.5, 0.125, 0, 1]
    
    popt, pcov = curve_fit(function, data_x, data_y, ig)
    
    return popt, pcov

def fit_curve(data_x, data_y):
    """
    
    """
    
    popt, pcov = fit_params(data_x, data_y)
    
    x = np.linspace(0, int(max(data_x)), num = 10000)
    y = exp(x, *popt)
    
    return x, y

def rhalf(data_x, data_y):
    """
    
    """
    
    popt, pcov = fit_params(data_x, data_y)
    
    a = popt[0]
    tau = popt[1]
    xoff = popt[2]
    yoff = popt[3]
    
    r_half = yoff + a/2
    
    return r_half

def thalf(data_x, data_y):
    """
    
    """
    
    popt, pcov = fit_params(data_x, data_y)
    
    a = popt[0]
    tau = popt[1]
    xoff = popt[2]
    yoff = popt[3]
    
    r_half = rhalf(data_x, data_y)
    
    t_half = -tau * np.log( (r_half - yoff) / a ) + xoff
    
    return t_half

def Dcoeff(data_x, data_y, radius_microns):
    """
    
    """
    
    t_half = thalf(data_x, data_y)
    
    D = 0.224 * radius_microns**2 / t_half
    
    return D