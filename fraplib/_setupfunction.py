import os

def _setup(foldername):
    """
    Sets up the script with the input and output directorys corresponding to my data organization strategy.
    
    Parameters
    ----------
    foldername : str
        name of directory containing raw data

    Returns
    -------
    input_dir : str
        path to input directory
    output_dir : str
        path to ouput directory
    """
    
    # script_dir = '/Volumes/GoogleDrive/My Drive/RG Lab/Microscopy/analysis/'
    script_dir = './'
    if os.path.exists(script_dir+foldername):
        pass
    else:
        os.mkdir(foldername)
    
    input_dir = '../'+foldername
    output_dir = script_dir+foldername+'/'
    
    return input_dir, output_dir