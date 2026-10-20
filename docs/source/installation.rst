=============
Installation
=============

The easy way
~~~~~~~~~~~~

The recommended way to install BikeNetLib is using `conda <https://docs.conda.io/projects/conda/en/latest/index.html>`__ (or the faster `mamba <https://mamba.readthedocs.io/en/latest/index.html>`__) via the `conda-forge` channel:

::

   conda install bikenetlib -c conda-forge

For more installation options, see below.

With pip
~~~~~~~~

BikeNetLib can also be installed with pip, if all dependencies can be installed as well:

::

   pip install bikenetlib

.. warning::

    We do not recommend using pip, because you need to make sure that all dependencies of bikenetlib are installed correctly. Using conda, see `above <#the-easy-way>`__, avoids the need to compile the dependencies yourself.


Environment installations
~~~~~~~~~~~~~~~~~~~~~~~~~

Creating a new environment is not strictly necessary, but given that installing other geospatial packages from different channels may cause dependency conflicts, it can be good practice to install in a clean environment starting fresh.

The main step is to set up a virtual environment ``bnlenv`` in which to
install the package, and then to use or run the environment. Use either of the methods below.

With conda
^^^^^^^^^^

Installation with `conda <https://docs.conda.io/projects/conda/en/latest/index.html>`__ (or the faster `mamba <https://mamba.readthedocs.io/en/latest/index.html>`__). The following commands create the ``bnlenv`` environment, configures it to install packages always from conda-forge, and installs BikeNetLib in it:

::

   conda create -n bnlenv
   conda activate bnlenv
   conda config --env --add channels conda-forge
   conda config --env --set channel_priority strict
   conda install python=3 bikenetlib

With Pixi
^^^^^^^^^

The fastest and cleanest way to install BikeNetLib is via `Pixi <https://pixi.prefix.dev/latest/#installation>`__:

::

   pixi init
   pixi add bikenetlib

Then use the Pixi environment as so:

::

   pixi shell

.. note::

    The first time you run code with Pixi, it might take a minute longer, as Pixi resolves the environment’s dependencies only at this point.


Run bikenetlib in Jupyter lab
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After having set up the environment `above <#environment-installations>`__, if you wish to run
bikenetlib via `JupyterLab <https://pypi.org/project/jupyterlab/>`__,
follow the corresponding instructions below.

With conda
^^^^^^^^^^

Using `conda <https://docs.conda.io/projects/conda/en/latest/index.html>`__ (or the faster `mamba <https://mamba.readthedocs.io/en/latest/index.html>`__), run:

::

   conda activate bnlenv
   ipython kernel install --user --name=bnlenv
   conda deactivate
   jupyter lab

Once Jupyter lab opens, switch the kernel (Kernel > Change Kernel >
bnlenv)

With Pixi
^^^^^^^^^

Once you are in the Pixi shell, see `above <#with-pixi>`__, simply run jupyter lab:

::

   jupyter lab

With pip
^^^^^^^^

Using pip, run:

::

   pip install --user ipykernel
   python -m ipykernel install --user --name=bnlenv
   jupyter lab

Once Jupyter lab opens, switch the kernel (Kernel > Change Kernel >
bnlenv)

Development installation
~~~~~~~~~~~~~~~~~~~~~~~~

If you want to develop the project, `clone this
repository <https://github.com/BikeNetKit/bikenetlib/archive/refs/heads/main.zip>`__
and create the environment via `Pixi <https://pixi.prefix.dev/latest/>`__ and the
``environment-dev.yml`` file:

::

   pixi init --import environment-dev.yml

The development environment is called ``bnlenvdev``. At this point you can run bikenetlib in the environment, for example as
such:

::

   pixi run python examples/mwe.py

.. note::

    The first time you run code with Pixi, it might take a minute longer, as Pixi resolves the environment’s dependencies only at this point.

Alternatively, start a pixi shell:

::

   pixi shell

Make sure to also
read `our contribution
guidelines <https://github.com/BikeNetKit/BikeNetLib?tab=contributing-ov-file#contributing-to-bikenetkit>`__.
