import czifile
from pathlib import Path
import numpy as np
from aicsimageio import AICSImage # https://github.com/AllenCellModeling/aicsimageio

def load_data(path):
    """
    loads the file and the metadata, including frame-specific metadata

    Parameters
    ----------
    path : str
        path to the file

    Returns
    -------
    data : aicsimageio.aics_image.AICSImage
    file : czifile.CziFile
    metadata : dict
    subblocks : dict
    attachments: dict
    """
    
    file = czifile.CziFile(str(Path(path).resolve()))
    
    for segment in file.segments():
        if isinstance(segment, czifile.MetadataSegment):
            metadata = segment.data(raw=False) # a dictionary
    
    subblocks = {
        "images": [
            segment.data()
            for segment in file.segments()
            if isinstance(segment, czifile.SubBlockSegment)
        ],
        "image_metadata": [
            segment.metadata()
            for segment in file.segments()
            if isinstance(segment, czifile.SubBlockSegment) 
            # and segment.metadata() is not None
        ],
    }
    
    attachments = {
        segment.attachment_entry.name : segment.data()
        for segment in file.segments()
        if isinstance(segment, czifile.AttachmentSegment)
    }
    
    data = AICSImage(str(Path(path).resolve()))
    
    expt = {'data' : data,
            'md' : metadata,
            'sb' : subblocks,
            'atch' : attachments}

    return expt