Getting started
===============

Get Started in 4 Steps
----------------------

1. Install BikeNetLib by following the :doc:`installation` guide.

2. To check that the installation worked, run the :doc:`mwe`.

3. Walk through illustrative examples of BikeNetLib's features on our :doc:`usage` pages.

4. Consult the :doc:`reference_user` for complete details on using the package.

Also, if you're not already familiar with `OSMnx`_ and `GeoPandas`_, make sure you read their user guides as BikeNetLib uses their data structures.

.. _overview-of-bikenetlib:

Overview of BikeNetLib
----------------------

BikeNetLib is built on top of `OSMnx`_ and `GeoPandas`_. It is imported as ``bnl`` and comes with several building blocks:

- ``bnl.io`` – Input and output
- ``bnl.utils`` – Utilities
- ``bnl.viz`` – Visualization
- ``bnl.osm`` – OpenStreetMap constants


To try it out, run the:

.. toctree::
   :maxdepth: 1

   Minimum working example <mwe>


.. _GeoPandas: https://geopandas.org
.. _OSMnx: https://osmnx.readthedocs.io