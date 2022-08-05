import czifile
import xml.etree.ElementTree as et

def channel_label(file):
    """
    Grabs the descriptive channel names from the metadata.
    
    Parameters
    ----------
    file : CziFile
        original data file
    
    Returns
    -------
    chlabels : list
        list of descriptive channel names (strings), in the same order as the channels in the image array.
    """
    
    md = et.fromstring(file.metadata())
    
    chlabels = []
    nTL = 0
    for ind, cm in enumerate(md.findall('.//Dimensions//ContrastMethod')):
        if cm.text == 'Fluorescence':
            desc = md.findall('.//Dimensions//Fluor')[ind-nTL].text
            chlabels.append(desc)
        else:
            chlabels.append('Transmitted Light')
            nTL += 1
    
    return chlabels

def get_gain(file):
    """
    Grabs the gain info for each channel, in the same order as the channels in the image
    
    Parameters
    ----------
    file : CziFile
        original data file
    
    Returns
    -------
    gains : list
        list of gain values
    """
    
    md = et.fromstring(file.metadata())
    gains = [round(float(elem.text)) for elem in md.findall('.//Dimensions//Gain')]
    
    return gains

def get_power(file):
    """
    Grabs the laser power info for each channel, in the same order as the channels in the image
    
    Parameters
    ----------
    file : CziFile
        original data file
    
    Returns
    -------
    powers : list
        list of power values; fractional
    """
    
    md = et.fromstring(file.metadata())
    powers = [
        round(1 - float(elem.text), 2) for 
        elem in 
        md.findall('.//LightSourceSettings/Attenuation')
    ]
    
    return powers

def get_objective(file):
    """
    Grabs the objectve info for the experiment
    
    Parameters
    ----------
    file : CziFile
        original data file
    
    Returns
    -------
    objective : str
        objective information
    """
    
    md = et.fromstring(file.metadata())
    objective = md.findall('.//Experiment//Objective')[0].text
    
    return objective

def get_em(file):
    """
    Grabs the emission wavelength range for each fluorescence channel in the experiment.
    
    Paramters
    ---------
    file : CziFile
        original data file
    
    Returns
    -------
    em : list of tuples
        (lower wavelength (nm), higher wavelength (nm))
    """
    
    md = et.fromstring(file.metadata())
    em = [
        (float(elem.text.split('-')[0]),float(elem.text.split('-')[1])) for
        elem in
        md.findall('.//Ranges')
    ]
    
    return em

def get_ex(file):
    """
    Grabs the excitation wavelength (nm) for each channel in the experiment.
    
    Parameters
    ----------
    file : CziFile
        original data file
    
    Returns
    -------
    ex : list of floats
    """
    
    md = et.fromstring(file.metadata())
    ex = [float(elem.text) for elem in md.findall('.//LightSourceSettings/Wavelength')]
    
    return ex

def get_scales(file):
    """
    """
    
    return

def get_regions(file, units = None):
    """
    Grabs the geometry of regions of interest specified during the experiment.
    
    Parameters
    ----------
    file : CziFile
        original data file
    
    Returns
    -------
    geom : list of tuples
        e.g. (cx, cy, r)
    """
    
    md = et.fromstring(file.metadata())
    shapes = [elem.tag for elem in md.findall('.//Geometry/..')]
    shape = shapes[::2]
    
    # [0] : position in pixels; # [1] : position in microns
    if units is None or units == 'px' or units == 'pix' or units == 'pixels':
        ind = 0
    else:
        ind = 1
    
    geom = []
    for region in shape:
        if 'Circle' in region:
            cx = float(md.findall('.//Circle//CenterX')[ind].text)
            cy = float(md.findall('.//Circle//CenterY')[ind].text)
            r = float(md.findall('.//Circle//Radius')[ind].text)
            geom.append(cx, cy, r)
    
    return geom

def get_dims(file):
    """
    Grabs the size of each dimension of the experiment.
    
    Parameters
    ----------
    file : CziFile
        original data file
    
    Returns
    -------
    dims : dict
        {dimension_name : size}
    """
    
    md = et.fromstring(file.metadata())
    names = ['Size'+letter for letter in file.axes] # list
    shape = file.asarray().shape # tuple
    
    dims = {name : size for name, size in zip(names, shape)}
    
    return dims