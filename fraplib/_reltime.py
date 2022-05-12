import numpy as np


def relt(expt, relative_to_time=None):
    """
    creates an array of image acquisition times in seconds relative to the specified time.
    default is to bleach end (if bleach exists) or first image acquired (if bleach doesn't exist).

    Parameters
    ----------
    expt : dict
        output of load_data
    relative_to_time : float
        a particular time

    Returns
    -------
    times : np.ndarray
    """

    atch = expt['atch']

    timestamps = expt['atch']['TimeStamps']
    t = np.asarray(timestamps)

    if relative_to_time is None:
        if 'EventList' in atch and 'BLEACH_STOP' in atch['EventList']['event type']:
            time = atch['EventList']['event time'][
                atch['EventList']['event type'].index('BLEACH_STOP')
            ]
            times = t - time
        else:
            print(
                'warning: times not relative to bleach end because bleach not detected in Event List.'
            )
            relative_to_index = 0
            times = t - t[relative_to_index]
    else:
        t2 = t - t[0]
        times = t2 - relative_to_time

    return times


def get_postbleach_t(expt, relative_to_time=None):
    """
    creates an array containing the subset of image acquisition timestamps after bleach end in an experiment that includes bleaching.

    Parameters
    ----------
    experiment : dict
        output of load_data
    relative_to_time : float
        a particular time

    Returns
    -------
    use_times : np.ndarray
    """

    times = relt(expt, relative_to_time)

    use_times = times[times >= 0]

    return use_times


def get_prebleach_t(expt, relative_to_time=None):
    """
    creates an array containing the subset of image acquisition timestamps before bleach end in an experiment that includes bleaching.

    Parameters
    ----------
    experiment : dict
        output of load_data
    relative_to_time : float
        a particular time

    Returns
    -------
    use_times : np.ndarray
    """

    times = relt(expt, relative_to_time)

    use_times = times[times < 0]

    return use_times
