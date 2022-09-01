import czifile
import xml.etree.ElementTree as et
import numpy as np


def version(file):
    """
    Get the CZI version from the metadata.
    
    Parameters
    ----------
    file : czifile
        original data file
    
    Returns
    -------
    version : str
    """
    md = file.metadata()
    mdt = et.fromstring(md)
    
    version = [elem.text for elem in mdt.findall('./Metadata/Version')]
    
    if version:
        version = version[0]
    else:
        version = [elem.get('Version') for elem in mdt.findall('./Metadata/Experiment')][0]
    
    return version


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
    for ind, cm in enumerate(md.findall(".//Dimensions//ContrastMethod")):
        if cm.text == "Fluorescence":
            desc = md.findall(".//Dimensions//Fluor")[ind - nTL].text
            chlabels.append(desc)
        else:
            chlabels.append("Transmitted Light")
            nTL += 1
    
    if len(chlabels) == 1:
        chlabels = chlabels[0]
    
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

    v = version(file)
    md = et.fromstring(file.metadata())
    
    if v == '1.0':
        gains = [float(elem.text) for elem in md.findall(".//Dimensions//Gain")]
    else:
        channel = channel_label(file)
        gains = []
        for elem in md.findall('.//DetectorGain/../..'):
            # print(elem.tag, elem.attrib)
            a = elem.attrib
            if 'Name' in a:
                if isinstance(channel, str):
                    if channel in a['Name']:
                        # print(a['Name'])
                        gains.append(float(elem.findall('.//DetectorGain')[0].text))
                elif isinstance(channel, list):
                    for chname in channel:
                        if chname in a['Name']:
                            # print(a['Name'])
                            gains.append(float(elem.findall('.//DetectorGain')[0].text))
    
    if len(gains) == 1:
        gains = gains[0]
    
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
        round(1 - float(elem.text), 2)
        for elem in md.findall(".//LightSourceSettings/Attenuation")
    ]
    
    if len(powers) == 1:
        powers = powers[0]
    
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
    v = version(file)
    if v == '1.0':
        objective = md.findall(".//Experiment//Objective")[0].text
    else:
        objective = [elem.attrib['Name'] for elem in md.findall('.//Objectives/Objective')][0]

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
        (float(elem.text.split("-")[0]), float(elem.text.split("-")[1]))
        for elem in md.findall(".//Ranges")
    ]
    
    if len(em) == 1:
        em = em[0]
    
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
    ex = [float(elem.text) for elem in md.findall(".//LightSourceSettings/Wavelength")]
    
    if len(ex) == 1:
        ex = ex[0]

    return ex


def get_scales(file):
    """
    Grab the scaling info in all dimensions, in units of microns.
    
    Parameters
    ----------
    file : CziFile
        original data file
    
    Returns
    -------
    scales : list
        [x-scale, y-scale] or [x-scale, y-scale, z-scale], values in units of microns
    """

    md = et.fromstring(file.metadata())
    scales = {
        each.attrib["Id"] : float(each.findall("./Value")[0].text) / 1e-6
        for each in md.findall(".//Scaling/Items/Distance")
    }

    
    lst = list(zip( list(scales.keys()), list(scales.values() ))) # key : value pairs as list of tuples
    def get_first(tup):
        return tup[0]
    lst.sort(key = get_first) # sort lst alphabetically by the first element of each tuple (the key from above); produces [('X', value), ('Y', value), ('Z', value)]
    scales = [tup[1] for tup in lst] # list of values in X, Y, Z order
    
    return scales


def get_regions(file, units=None):
    """
    Grabs the geometry of regions of interest specified during the experiment. Currenltly works only for circles.

    Parameters
    ----------
    file : CziFile
        original data file
    units : str

    Returns
    -------
    geom : list of tuples
        e.g. (cx, cy, r)
    """

    md = et.fromstring(file.metadata())
    shapes = [elem.tag for elem in md.findall(".//Circle")]
    
    v = version(file)
    
    if v == '1.0':
        shape = shapes[::2]
    else:
        shape = shapes

    xum = get_scales(file)[0] # microns
    yum = get_scales(file)[1] # microns
        
    geom = []
    ind = 0
    for region in shape:
        if "Circle" in region:
            cx = float(md.findall(".//Circle//CenterX")[ind].text)
            cy = float(md.findall(".//Circle//CenterY")[ind].text)
            r = float(md.findall(".//Circle//Radius")[ind].text)
            
            if units == 'microns' or units == 'micrometers':
                
                cx = cx * xum
                cy = cy * yum
                r = r * xum
            
            geom.append((cx, cy, r))
            ind += 1 

    # if len(geom) == 1:
    #     geom = geom[0]
    
    return geom


def get_dims(file, specific = None):
    """
    Grabs the size of each dimension of the experiment.

    Parameters
    ----------
    file : CziFile
        original data file
    specific : str
        e.g 'CZYX'

    Returns
    -------
    dims : list
    """

    md = et.fromstring(file.metadata())
    names = [letter for letter in file.axes]  # list
    shape = file.asarray().shape  # tuple

    dims = {name: size for name, size in zip(names, shape)}
    
    if specific is None:
        dims = [ dims[key] for key in dims if dims[key] > 1 ]
    else:
        dims = [dims[dim] for dim in specific]

    return dims
