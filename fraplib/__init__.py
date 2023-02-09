try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
__author__ = "Elizabeth May"
__email__ = "ejmay2012@gmail.com"

from ._setupfunction import _setup
from .loading import load_data, batchread
from .metadatafunctions import (
    version,
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
from .calculations import evaluate, find_biggest_drop
from .circular_mask import create_circular_mask
from .expb2 import fit_expD, fit_expb2
from .falsecolor import falsecolor, make_colormap
from .regions import draw_circle
from .scalebar import scalebar
from .timestamp import timestamp
from .pretty_plot import pretty_plot
from .onestep import analyze
from .read_chromatogram import read_chromatogram

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "_setup",
    "load_data",
    "batchread",
    "channel_label",
    "evaluate",
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
    "find_biggest_drop",
    "fit_expD",
    "fit_expb2",
    "falsecolor",
    "make_colormap",
    "draw_circle",
    "scalebar",
    "timestamp",
    "pretty_plot",
    "analyze"
]
