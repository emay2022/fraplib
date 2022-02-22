try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
__author__ = "Elizabeth May"
__email__ = "ejmay2012@gmail.com"

from ._loading import load_data
from ._reltime import reltimes_fromAttach
from ._reltime import reltimes_fromSubblocks
from ._reltime2 import reltimes

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "load_data",
    "frame_times",
    "reltimes_fromAttach",
    "reltimes_fromSubBlocks",
    "reltimes"
]