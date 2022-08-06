from pathlib import Path
import os
import czifile


def load_data(path):
    """
    loads the file and the metadata, including frame-specific metadata

    Parameters
    ----------
    path : str
        path to the file

    Returns
    -------
    file : CziFile
        original data file in CziFile format
    subblocks : dict
        { images : array, immd : str }
        # check if subblocks["images"] is really an array
        # check if subblocks["immd"] is really str
    """

    file = czifile.CziFile(str(Path(path).resolve()))

    subblocks = {
        "images": [
            segment.data()
            for segment in file.segments()
            if isinstance(segment, czifile.SubBlockSegment)
        ],
        "immd": [ # image-specific metadata
            segment.metadata()
            for segment in file.segments()
            if isinstance(segment, czifile.SubBlockSegment)
            # and segment.metadata() is not None
        ],
    }
    
    return file, subblocks

def batchread(directory):
    """
    Reads .czi files in directory into a data holder [holder].
    
    Parameters
    ----------
    directory : str
        path to directory containing files of interest
    
    Returns
    -------
    holder : dict
        keys correspond to a file name; values correspond to the data (type = CziFile)
    pathholder : dict
        keys correspond to a file name; values correspond to a path to the file (type = str)
    """
    
    # directory = input_dir
    
    extension = '.czi'
    
    holder = {}
    pathholder = {}
    
    for item in os.listdir(directory):
        
        f = os.path.join(directory, item)
        
        if os.path.isfile(f) and item[-4:] == extension:
            
            # print(item)
            file, _ = load_data(f)
            holder[item] = file
            pathholder[item] = f
    
    return holder, pathholder