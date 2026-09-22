Load Data into DataFrames
=========================

This guide goes through the process of using OPynSim to load various data files
in the OpenSim ecosystem (e.g. ``.trc``, ``.sto``) into Pandas dataframes so
that your Python code can easily manipulate and visualize the data.

The utility of dataframes is that they are standard across the Python ecosystem:
many libraries (e.g. plotters, statistical, machine learning) accept/emit
dataframes. Having a pathway between the data files emitted by platforms like
OpenSim/OPynSim and data frames increases the utility of that data.


Setup Example Data
------------------

If you want to run the Python code in this guide, you must first set up the
:doc:`../setup/example-data`.


Read Data into an OPynSim DataFrame
-----------------------------------

The ``opynsim`` module provides a variety of file readers. All are prefixed
with ``read_``. Here are some useful ones:

- ``opynsim.read_osim``: Read an OpenSim model file (``.osim``) into an ``opynsim.ModelSpecification``.
- ``opynsim.read_sto``: Read an OpenSim storage file (``.sto``) into an ``opynsim.DataFrame``.
- ``opynsim.read_trc``: Read a track-row-column OpenSim file (``.trc``) into an ``opynsim.DataFrame``.
- ``opynsim.read_vtp``: Read a VTP mesh file (``.vtp``) into an ``opynsim.Mesh``.

For example, say you wanted to read the ``.mot`` file that we used in the
previous :ref:`load-states-from-file` guide. You could do that with
``opynsim.read_mot``, which returns an ``opynsim.DataFrame``:

.. code:: python

    import opynsim as opyn

    # `df` is an `opynsim.DataFrame`
    df = opyn.read_mot("pragmatic_resources/gait2354/OutputReference/subject01_walk1_ik.mot")


Convert to Pandas DataFrame
---------------------------

OPynSim's ``DataFrame`` class is designed to be converted to/from ``DataFrame``\s
from the wider Python ecosystem using optimized conversion functions, which
lets you choose which data frame library you want to use in your
scripts. These conversion functions convert *to* common ``DataFrame``
implementations:

- ``df.to_pandas()``: Converts ``df`` into a `pandas.DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_ (requires the ``pyarrow`` Python package to also be installed).
- ``df.to_polars()``: Converts ``df`` into a `polars.DataFrame <https://docs.pola.rs/api/python/stable/reference/dataframe/index.html>`_.

For example, here is how you would load a ``.mot`` file into a ``pandas.DataFrame``:

.. code:: python

    import opynsim

    # An `opynsim.DataFrame`.
    odf = opyn.read_mot("pragmatic_resources/gait2354/OutputReference/subject01_walk1_ik.mot")

    # A `pandas.DataFrame`.
    pdf = opynsim_df.to_pandas()


Manipulate/Plot Pandas DataFrame
--------------------------------

Once you have a ``DataFrame`` in a data frame library of your choice, you can
then manipulate it, plot it, or export it to a different data format much
more easily.

For example, you could use ``matplotlib`` to plot columns in a ``pandas.DataFrame``:

.. code:: python

    # Reads a `.mot` file and plots a timeseries of some of its columns

    import opynsim
    import matplotlib.pyplot as plt

    # Using built-in Pandas plotting (usually easiest)
    pdf = opyn.read_mot("pragmatic_resources/gait2354/OutputReference/subject01_walk1_ik.mot").to_pandas()
    pdf.plot(x="time", y=["knee_angle_l", "knee_angle_r"], kind="line")
    plt.show()

    # Using matplotlib directly (more customizable)
    plt.plot(pdf["time"], pdf["knee_angle_l"], label="knee_angle_l")
    plt.plot(pdf["time"], pdf["knee_angle_r"], label="knee_angle_r")
    plt.xlabel("time")
    plt.legend()
    plt.show()

Or scaling things:

.. code:: python

    # Reads a `.mot` file and scales `pelvis_tx` by 100x.

    import opynsim

    pdf = opyn.read_mot("pragmatic_resources/gait2354/OutputReference/subject01_walk1_ik.mot").to_pandas()
    pdf["pelvis_tx"] *= 100.0  # e.g. m -> cm


Or resampling the data to a fixed rate, which can be useful for plotting, animating,
signal processing, etc.:

.. code:: python

    # Reads a `.mot` file and resamples it to 120 Hz with linear interpolation.

    import numpy as np
    import opynsim as opyn
    import pandas as pd

    pdf = opyn.read_mot("pragmatic_resources/gait2354/OutputReference/subject01_walk1_ik.mot").to_pandas()
    pdf = pdf.set_index("time")
    t_120hz = np.arange(pdf.index.min(), pdf.index.max(), 1/120.0)
    pdf_120hz = (
        pdf.reindex(pdf.index.union(t_120hz))
            .interpolate(method="index")
            .loc[t_120hz]
    )

.. code:: python

    # Reads a `.mot` file and resamples it to 120 Hz with cubic splines.
    #
    # Requires installing `scipy` (e.g. `pip install scipy`).

    from scipy.interpolate import CubicSpline
    import pandas as pd
    import numpy as np
    import opynsim as opyn

    pdf = opyn.read_mot("pragmatic_resources/gait2354/OutputReference/subject01_walk1_ik.mot").to_pandas()
    pdf = pdf.set_index("time")
    t_120hz = np.arange(pdf.index.min(), pdf.index.max(), 1/120.0)
    pdf_120hz = pd.DataFrame(
        data=CubicSpline(pdf.index, pdf.to_numpy(), axis=0)(t_120hz),
        index=t_120hz,
        columns=pdf.columns
    )

Although beware: in this example's case we're actually upsampling with
interpolation (the original data is <120 Hz). Python can make things easier,
not sensible 🤡.


Convert to OPynSim DataFrame
----------------------------

Sometimes you'll want to get data *from* a third-party ``DataFrame`` *to* an
``opynsim.DataFrame``. Examples include loading cleaned-up ``DataFrame``\s
into ``opynsim.ModelStates``, loading motion data from an alternative file
formats (e.g. `.csv <https://en.wikipedia.org/wiki/Comma-separated_values>`_, `.parquet <https://en.wikipedia.org/wiki/Apache_Parquet>`_),
into OPynSim, or writing OpenSim-compatible from OPynSim's ``DataFrame``.

OPynSim's ``DataFrame`` class can be constructed from third-party ``DataFrame``\s,
provided they expose an `Arrow PyCapsule Interface <https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html>`_ (most do):

.. code:: python

    import opynsim as opyn

    # A `pandas.DataFrame`.
    pdf = opyn.read_mot("pragmatic_resources/gait2354/OutputReference/subject01_walk1_ik.mot").to_pandas()

    # An `opynsim.DataFrame`.
    df = opyn.DataFrame(pdf)


State Data Handling and Examples
--------------------------------

Once you have the ability to load data, convert it, manipulate it, and push it
back into OPynSim, you can then combine those techniques to do interesting
things with models.

For example, say you have some states from OpenSim's IK dynamic solver. You
would like to extract outputs from those states to plot alongside experimental
data. One problem is that OpenSim's forward dynamic solver may have a variable
step size, but your experimental data has a fixed step size.

TODO write up concrete example

.. warning::

   State files from OpenSim may encode angular columns in either degrees or radians. The
   header/metadata will have an ``inDegrees=yes`` entry when all applicable columns are
   in degrees. Otherwise, they're in radians. **It's recommended to always normalize
   angular columns to radians**, so that you don't have to constantly track the
   ``inDegrees`` flag.

   Unfortunately, state files (e.g. ``.sto``, ``.mot``) do not express *which* columns
   are angular. Therefore, both OPynSim and OpenSim must first load the associated model
   to figure that out; for example, with:

   - ``model.convert_data_frame_to_radians(df)``
   - ``model.getSimbodyEngine().convertDegreesToRadians(table)``

