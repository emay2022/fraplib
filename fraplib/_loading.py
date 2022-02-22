import czifile
from pathlib import Path
import pandas as pd
import numpy as np

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
    metadata : dict
    subblocks : dict
    attachments: dict
    """
    
    file = czifile.CziFile(str(Path(path).resolve()))
    
    metadata = [
        segment.data(raw=False)
        for segment in file.segments()
        if isinstance(segment, czifile.MetadataSegment)
    ][
        0
    ]  # a dictionary
    
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

    return file, metadata, subblocks, attachments