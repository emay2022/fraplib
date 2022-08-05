try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
__author__ = "Elizabeth May"
__email__ = "ejmay2012@gmail.com"

from ._setupfunction import _setup
from .loading import load_data, batchread
from .metadatafunctions import (
    channel_label,
    get_gain,
    get_power,
    get_objective,
    get_em,
    get_ex,
    get_scales,
    get_regions,
    get_dims,
)
from .attachments import get_events, get_timepoints
# from .calculations import (
#     _extract,
#     _sum_extract,
#     _mean_extract,
#     _norm_extract,
#     get_data_for_fit,
# )
from .circular_mask import create_circular_mask
from .expfit import Dcoeff, exp, fit_curve, fit_params, rhalf, thalf
from .falsecolor import falsecolor, make_colormap
from .relativetime import relt, get_postbleach_t, get_prebleach_t
from .regions import draw_circle
from .scalebar import scalebar
from .timestamp import timestamp

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "_setup",
    "load_data",
    "batchread",
    "channel_label",
    "get_gain",
    "get_power",
    "get_objective",
    "get_em",
    "get_ex",
    "get_scales",
    "get_regions",
    "get_dims",
    "get_events",
    "get_timepoints",
    "create_circular_mask",
    "Dcoeff",
    "exp",
    "fit_curve",
    "fit_params",
    "rhalf",
    "thalf",
    "falsecolor",
    "make_colormap",
    "relt",
    "get_postbleach_t",
    "get_prebleach_t",
    "draw_circle",
    "scalebar",
    "timestamp",
]
