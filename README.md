# <a href="https://docs.bikenetkit.org/BikeNetLib/"><img src="https://github.com/BikeNetKit/BikeNetLib/raw/main/docs/source/_static/logo_bikenetlib.svg" alt="BikeNetLib" width="255.93" height="59"></a>

[![Conda Version](https://img.shields.io/conda/vn/conda-forge/bikenetlib?color=10d249)](https://anaconda.org/conda-forge/bikenetlib)
[![PyPI Version](https://img.shields.io/pypi/v/bikenetlib?color=10d249)](https://pypi.org/project/BikeNetLib/)
[![Docs](https://github.com/BikeNetKit/BikeNetLib/actions/workflows/docs.yml/badge.svg)](https://docs.bikenetkit.org/BikeNetLib/)
[![Test](https://github.com/BikeNetKit/BikeNetLib/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/BikeNetKit/BikeNetLib/actions/workflows/test.yml)
[![Code coverage](https://codecov.io/gh/BikeNetKit/BikeNetLib/graph/badge.svg)](https://codecov.io/gh/BikeNetKit/BikeNetLib)
[![Mastodon Follow](https://img.shields.io/mastodon/follow/116693348622375119?domain=https%3A%2F%2Ffosstodon.org)](https://fosstodon.org/@BikeNetKit)

The Python package `bikenetlib` is BikeNetKit's Python core utility package. It offers general utilities for working with bicycle networks, which also forms the core of many upstream packages
in the [BikeNetKit family](https://github.com/BikeNetKit), like [GrowBikeNet](https://github.com/BikeNetKit/GrowBikeNet), [FixBikeNet](https://github.com/BikeNetKit/FixBikeNet), or [LinkBikeNet](https://github.com/BikeNetKit/LinkBikeNet).
 
BikeNetLib is imported as `bnl`. There are several building blocks:

- `bnl.io` – Input and output
- `bnl.osm` – OpenStreetMap constants
- `bnl.utils` – Utilities
- `bnl.viz` – Visualization

BikeNetLib mainly builds on [OSMnx](https://github.com/gboeing/osmnx) and [GeoPandas](https://github.com/geopandas/geopandas).

## Installation
The recommended way to install BikeNetLib is using [`conda`](https://docs.conda.io/projects/conda/en/latest/index.html):

```
conda install bikenetlib
```
### Advanced and development installations
For more installation options, see our [Installation docs](https://docs.bikenetkit.org/BikeNetLib/installation/).

## Usage
We provide a minimum working example:

- Jupyter notebook ([examples/mwe.ipynb](examples/mwe.ipynb))

For a walkthrough with illustrative examples, see our [Usage docs](https://docs.bikenetkit.org/BikeNetLib/usage/).

## Documentation
Find more information in our docs: [https://docs.bikenetkit.org/BikeNetLib/](https://docs.bikenetkit.org/BikeNetLib/)

## Supported by
Development of BikeNetKit/BikeNetLib is supported by the [Innovation Fund Denmark](https://innovationsfonden.dk/en) and the EU HORIZON project [JUST STREETS](https://www.just-streets.eu).

[![Innovation Fund Denmark](https://raw.githubusercontent.com/BikeNetKit/.github/refs/heads/main/profile/_static/logo_innovationfund.png)](https://innovationsfonden.dk/en) &emsp;&emsp; [![European Union](https://raw.githubusercontent.com/BikeNetKit/.github/refs/heads/main/profile/_static/logo_eu.png)](https://commission.europa.eu/index_en) &ensp; [![JUST STREETS](https://raw.githubusercontent.com/BikeNetKit/.github/refs/heads/main/profile/_static/logo_juststreets.png)](https://www.just-streets.eu/) 

Developed by  
<a href="https://nerds.itu.dk"><img src="https://raw.githubusercontent.com/BikeNetKit/.github/refs/heads/main/profile/_static/logo_nerds.png" alt="Networks, Data, and Society" width="280"></a>
