import pytest

import osmnx as ox

from bikenetlib import osm

def test_useful_tags_way():
    """Ensure that all needed way tags are indeed in the `useful_tags_way`.
    """
    for tag in ["highway", "cycleway", "bicycle", "cycleway:right", "cycleway:left", "cycleway:both", "cyclestreet", "access", "area", "service", "motor_vehicle", "motorcar"]:
        assert tag in ox.settings.useful_tags_way