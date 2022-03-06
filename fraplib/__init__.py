try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
__author__ = "Elizabeth May"
__email__ = "ejmay2012@gmail.com"

from ._loading import load_data
from ._reltime2 import reltimes
from ._falsecolor import make_colormap
from ._falsecolor import falsecolor
from ._scalebar import scalebar
from ._scalebar2 import scalebar2
from ._timestamp import timestamp
from ._regions import get_roi
from ._circular_mask import create_circular_mask
from ._regions import draw_circle
from ._calculations import _extract
from ._calculations import _sum_extract
from ._calculations import _mean_extract
from ._calculations import _norm_extract
from ._calculations import get_data_for_fit
from ._expfit import exp
from ._expfit import fit_params
from ._expfit import fit_curve
from ._expfit import rhalf
from ._expfit import thalf
from ._expfit import Dcoeff
from ._reltime3 import relt
from ._reltime3 import get_postbleach_t
from ._reltime3 import get_prebleach_t



__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "load_data",
    "reltimes",
    "make_colormap",
    "falsecolor",
    "scalebar",
    "scalebar2",
    "timestamp",
    "get_roi",
    "create_circular_mask",
    "draw_circle",
    "get_data_for_fit",
    "exp",
    "fit_params",
    "fit_curve",
    "rhalf",
    "thalf",
    "Dcoeff",
    "relt",
    "get_postbleach_t",
    "get_prebleach_t"
]