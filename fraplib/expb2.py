import numpy as np

def rhalf(data_x, data_y):
    """ """

    popt, pcov = fit_params(data_x, data_y)

    a = popt[0]
    tau = popt[1]
    xoff = popt[2]
    yoff = popt[3]

    r_half = yoff + a / 2

    return r_half


def thalf(data_x, data_y):
    """ """

    popt, pcov = fit_params(data_x, data_y)

    a = popt[0]
    tau = popt[1]
    xoff = popt[2]
    yoff = popt[3]

    r_half = rhalf(data_x, data_y)

    t_half = -tau * np.log((r_half - yoff) / a) + xoff

    return t_half


def Dcoeff(data_x, data_y, expt, roi):
    """ """
    um_per_px = (
        expt['md']['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][0][
            'Value'
        ]
        * 1e6
    )

    radius = roi['R']

    radius_microns = radius * um_per_px

    t_half = thalf(data_x, data_y)

    D = 0.224 * radius_microns ** 2 / t_half

    return D
