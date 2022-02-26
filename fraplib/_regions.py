def get_roi(md):
    """
    gets the regions of interest from the metadata
    
    Parameters
    ----------
    md : dict
        metadata
    
    Returns
    -------
    roi : list or dict
    """
    
    test = md['ImageDocument']['Metadata']['Layers']['Layer']
    
    if isinstance(test, list):
        
        roi = []
        
        for i in range(len(test)):
            
            x = md['ImageDocument']['Metadata']['Layers']['Layer'][i]['Elements']['Circle']['Geometry']['CenterX']
            y = md['ImageDocument']['Metadata']['Layers']['Layer'][i]['Elements']['Circle']['Geometry']['CenterY']
            r = md['ImageDocument']['Metadata']['Layers']['Layer'][i]['Elements']['Circle']['Geometry']['Radius']
            
            roi.append({'X': x, 'Y': y, 'R': r})
            
    else:
        
        x = md['ImageDocument']['Metadata']['Layers']['Layer']['Elements']['Circle']['Geometry']['CenterX']
        y = md['ImageDocument']['Metadata']['Layers']['Layer']['Elements']['Circle']['Geometry']['CenterY']
        r = md['ImageDocument']['Metadata']['Layers']['Layer']['Elements']['Circle']['Geometry']['Radius']
        
        roi = {'X': x, 'Y': y, 'R': r}
        
    return roi