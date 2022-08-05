import czifile

def get_events(file):
    """
    Grabs experiment 'event' descriptions and affiliated timestamps.
    
    Parameters
    ----------
    file : CziFile
        original data file
    
    Returns
    -------
    eventlist : dict
        { description : timestamp }
    """
    
    eventlist = {}
    
    for atch in file.attachments():
        if 'Event' in atch.attachment_entry.name:
            evl = atch.data()
            for ind in range(len(evl)):
                event = str(evl[ind])
                desc = event.split()[0]
                tval = float(event.split('@')[1].split()[0])
                eventlist[desc] = tval
    
    return eventlist

def get_timepoints(file):
    """
    Grabs experiment frame timepoints.
    
    Parameters
    ----------
    file : CziFile
        original data file
    
    Returns
    -------
    t : array
        array of timepoints as floats
    traw : array
        non-zeroed array of timepoints as floats, for comparison with e.g. event timestamps
    """
    
    for atch in file.attachments():
        if 'Time' in atch.attachment_entry.name:
            traw = atch.data()
    t = traw - traw.min()
    
    return t, traw