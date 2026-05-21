import pytest
import osmnx as ox
import pandas as pd
import geopandas as gpd
from pandas.testing import assert_frame_equal
from bikenetlib.io import (
    prepare_network,
    download_pois,
    save_to_file,
)
from shapely.geometry import Point, LineString, MultiLineString

# To do