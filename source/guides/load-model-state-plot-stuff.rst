Load Model (+States), Plot Stuff
================================

This guide goes through the process of using ``opensim`` to load a model from
an ``.osim`` file and (optionally) load states from a ``.sto`` file,
followed by plotting quantities of interest with ``matplotlib``. This is a
simple process that's extremely useful to master, because automating "open data
files and plot things" is a very common workflow.


Load a Model
------------

Loading an OpenSim model from an ``.osim`` file is achieved by passing
the file's path as a string to the ``opensim.Model`` constructor:

.. code:: python

   import opensim

   model = opensim.Model("model.osim")

You can also use Python's in-built ``pathlib.Path`` to construct paths, which
can be useful certain tasks. Just remember to convert the ``pathlib.Path``
into a string (``str``) before passing it to OpenSim:

.. code:: python

   import opensim
   from pathlib import Path

   # Iterate over all `.osim` files in a directory
   for osim in Path("some-directory").glob("*.osim"):
       model = opensim.Model(str(osim))


Load States From a File
-----------------------

Some solvers, such as the forward dynamics and inverse kinematics solvers,
produce sequences of model states that are typically written to ``.sto`` files.
You can load an ``sto`` file like this:

.. code:: python

   import opensim

   model = opensim.Model("model.osim")
   model.initSystem()

   states_table = opensim.TimeSeriesTable("motion.sto")
   states = opensim.StatesTrajectory.createFromStatesTable(model, states_table)

You can load the raw state data from the ``.sto`` without a model (``states_table``),
but a model (``model``) is required to convert the data into a usable state
sequence (``states``). This is because the model has contextual information,
such as which columns in the raw data correspond to angular quantities.


Realize / Compute Derived State Quantities
------------------------------------------

States loaded from files are only "filled in" with whatever was in the file.
This is because the "filling in" code doesn't know, for example, that
the calling code intends on re-equilibrating muscles per-step, or that
it plans on extracting outputs that depend on derived quantities in
the states.

OpenSim models have methods that realize/compute things in its associated
state(s). For example, you could use ``model.realizePosition(state)``
to ensure any position-dependent outputs can be read from the state:

.. code:: python

   import opensim

   # Read model + states
   model = opensim.Model("model.osim")
   model.initSystem()
   states_table = opensim.TimeSeriesTable("motion.sto")
   states = opensim.StatesTrajectory.createFromStatesTable(model, states_table)

   # Realize each state to position stage
   for state in states:
       model.realizePosition(state)

The most common state-update steps are the following:

``model.realizeX(state)`` (e.g. ``model.realizeReport(state)``)
    These realize ``state`` to realization stage ``X``, making derived quantities
    that depend on that stage readable. ``Report`` is the latest stage (`stage list <https://simbody.github.io/3.8.0/classSimTK_1_1Stage.html#ac3ebdb6f8942a72c65886e5286dd8a13>`_).

    **Beware**: "readable" does not mean "valid". Realizing a state that was
    partially filled in can make derived/later stages invalid. For example,
    reading kinematics data (positions, rotations) from an ``.sto`` file
    into a state followed by using ``.realizeDynamics`` on it does not
    correctly calculate the dynamics for that state. A single state
    with only kinematic information is insufficient, an Inverse Dynamics
    (ID) solver is required to compute that.

``model.equilibrateMuscles(state)``
   Equilibrates muscles in the state.


Extract Quantities from Model (+ States)
----------------------------------------

TODO: once you have a model with fully-prepared states, you can then extract
useful information out of the model (e.g. the positions of things over the trajectory).
Convert the information into numpy arrays etc. so that your code can interact
with it easily.


Plot Quantities
---------------

TODO: once you have extracted lists/numpy arrays of numbers, you can then pump
them into ``matplotlib`` to create plots ready for analysis/presentation.
