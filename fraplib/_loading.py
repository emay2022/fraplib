import czifile
from pathlib import Path
import numpy as np
from aicsimageio.readers import CziReader # https://github.com/AllenCellModeling/aicsimageio

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
    
    if 'EventList' in attachments:
        evtype = [
            entry.EV_TYPE[entry.event_type] 
            for entry in attachments['EventList'] 
            if isinstance(entry, czifile.EventListEntry)
        ]
        evtime = [
            entry.time 
            for entry in attachments['EventList'] 
            if isinstance(entry, czifile.EventListEntry)
        ]
        evdesc = [
            entry.description 
            for entry in attachments['EventList'] 
            if isinstance(entry, czifile.EventListEntry)
        ]
        attachments['EventList'] = {
            'event type' : evtype, 
            'event time' : evtime, 
            'event description' : evdesc
        }
    try:
        data = CziReader(str(Path(path).resolve()), include_subblock_metadata=True)
        test = data.metadata
    except:
        data = CziReader(str(Path(path).resolve()), include_subblock_metadata=False)
        print('warning: due to exception, subblock metadata not appended.')
    
    ## regions
    roi = {}
    count = 1
    for element in data.metadata.findall(".//Elements/"):
        # print(element.tag)
        if count < 10:
            roi[element.tag+'_0'+str(count)] = {}
        else:
            roi[element.tag+'_'+str(count)] = {}

        for lement in element.findall(".//Geometry/"):
            if element.tag == 'Circle':
                tag_list = ['CenterX', 'CenterY', 'Radius']
            elif element.tag == 'Rectangle': # made-up example
                tag_list = ['CenterX', 'CenterY', 'Width', 'Height']
            elif element.tag == 'Other': # to fill in
                tag_list = ['other', 'tags', 'here']
            else:
                tag_list = [lement.tag]

            if lement.tag in tag_list:
                # print('\t', lement.tag, lement.attrib, lement.text)
                if count < 10:
                    roi[element.tag+'_0'+str(count)][lement.tag] = lement.text
                else:
                    roi[element.tag+'_'+str(count)][lement.tag] = lement.text
        count = count+1
    
    expt = {'data' : data,
            'md' : metadata,
            'sb' : subblocks,
            'atch' : attachments,
            'roi' : roi
           }

    return expt