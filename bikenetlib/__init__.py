import contextlib
from importlib.metadata import PackageNotFoundError, version

from . import io
from . import utils
from . import viz

__author__ = "MS, AV, MK"
__author_email__ = "email@domain.com"

with contextlib.suppress(PackageNotFoundError):
    __version__ = version("bikenetlib")
