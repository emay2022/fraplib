# this code snippet is taken directly from John C. Russell

import numpy as np
import pandas as pd
import xarray as xr

# __all__ = [
#     "check_labels_from_multiindex",
# ]


def check_labels_from_multiindex(
    labels: xr.DataArray, index: pd.MultiIndex, scene_character: str = "S"
) -> xr.DataArray:
    """
    Given a pd.MultiIndex Object which identifies particular cells, return a labels
    array which only shows the cells in the index.
    Parameters
    ----------
    labels: xr.DataArray
        Image like array containg integer labeled regions.
    index: pd.MultiIndex
        MultiIndex object with scene and cell labels to check.
        ***NOTE*** This follows the microutil convention that label values in the index
        are zero indexed - and hence off by one relative to the values in the labels
        array.
    scene_character: str - Default "S"
        Character that refers to the scene dimension of the labels DataArray and the
        scene level of the multiindex.
    """

    level = None
    for i in range(len(index.names)):
        if index.names[i] == scene_character:
            level = i
            break
    if level is None:
        raise KeyError(
            f"Name {scene_character} not found in index with levels {index.names}"
        )

    check_labels = xr.zeros_like(labels)

    for s in range(labels.sizes[scene_character]):
        try:
            # See ***NOTE*** in docstring regarding +1 here
            checks = index.get_loc_level(s, level)[1].values + 1
        except KeyError:
            continue

        mask = xr.DataArray(np.isin(labels.data[s], checks), dims=labels[s].dims)
        check_labels[s] = labels[s].where(mask)

    return check_labels