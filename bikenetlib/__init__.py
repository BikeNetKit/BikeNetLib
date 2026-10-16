"""
BikeNetLib is a Python package of core utility functions for bicycle network
analysis.

Full documentation at: https://docs.bikenetkit.org/BikeNetLib/
"""
import contextlib
from importlib.metadata import PackageNotFoundError, version

from . import constants
from . import io
from . import osm
from . import utils
from . import viz

__author__ = "BikeNetLib contributors"
__author_email__ = "contact@bikenetkit.org"

with contextlib.suppress(PackageNotFoundError):
    __version__ = version("bikenetlib")
