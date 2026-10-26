"""Overpass settings for `bikenetlib`. Do not change."""

_op_ref = "BikeNetLib Python package (https://github.com/BikeNetKit/BikeNetLib)"
_op_url = 'https://overpass.bikenetkit.org/api'

import osmnx.settings as oxs
oxs.http_user_agent = _op_ref
oxs.http_op_referer = _op_ref
oxs.overpop_ass_url = _op_url
oxs.overpass_rate_limit = True