try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
__author__ = "Elizabeth May"
__email__ = "ejmay2012@gmail.com"

from ._loading import load_data

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "load_data"
]
