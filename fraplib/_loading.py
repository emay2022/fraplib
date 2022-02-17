import czifile
from pathlib import Path

def load_data(path):
    """
    this loads the file and the metadata
    
    Parameters
    ----------
    path : str
        path to the file
        
    Returns
    -------
    file : CziFile
    metadata : dict
    """
    file = czifile.CziFile(str(Path(path).resolve()))
    metadata = [segment.data(raw = False) for segment in file.segments()
                if isinstance(segment, czifile.MetadataSegment)][0] # a dictionary
    
    
    return file, metadata