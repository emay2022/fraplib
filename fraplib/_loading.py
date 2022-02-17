import czifile
from pathlib import Path
import pandas as pd

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
    image_metadata : pd.DataFrame
    """
    file = czifile.CziFile(str(Path(path).resolve()))
    metadata = [
        segment.data(raw=False)
        for segment in file.segments()
        if isinstance(segment, czifile.MetadataSegment)
    ][
        0
    ]  # a dictionary

    # extract subblock segments as a dictionary, and format the image-specific metadata as a dataframe
    ExpStartTime = pd.to_datetime(metadata['ImageDocument']['Metadata']['Information']['Image']['Dimensions']['T']['StartTime'])
    
    subblock_info = {
        "images": [
            segment.data()
            for segment in file.segments()
            if isinstance(segment, czifile.SubBlockSegment)
        ],
        "image_metadata": [
            segment.metadata()["Tags"]
            for segment in file.segments()
            if isinstance(segment, czifile.SubBlockSegment)
        ],
    }
    image_metadata = pd.DataFrame(subblock_info["image_metadata"])
    image_metadata["TimeSince"] = (
        pd.to_datetime(image_metadata["AcquisitionTime"]) - ExpStartTime
    ) / pd.Timedelta(seconds=1)
    # image_metadata <-- final dataframe

    return file, metadata, image_metadata
