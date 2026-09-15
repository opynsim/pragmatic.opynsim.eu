Load Model (+States), Plot Stuff
================================

This guide goes through the process of using ``opensim`` to load a model from
an ``.osim`` file and (optionally) load states from a ``.sto`` file,
followed by plotting quantities of interest with ``matplotlib``. This is a
simple process that's extremely useful to master, because automating "open data
files and plot things" is a very common workflow.


Load the Model with OpenSim
---------------------------

Loading an OpenSim model from an ``.osim`` file is achieved by passing
the file's path as a string to the ``opensim.Model`` constructor:

.. code:: python

   import opensim

   model = opensim.Model("project-path-to.osim")

You can also use Python's in-built ``pathlib.Path`` to construct paths, which
can be useful certain tasks. Just remember to convert the ``pathlib.Path``
into a string (``str``) before passing it to OpenSim:

.. code:: python

   import opensim
   from pathlib import Path

   # Iterate over all `.osim` files in a directory
   for osim in Path("some-directory").glob("*.osim"):
       model = opensim.Model(str(osim))


Load States From a ``.sto`` File
--------------------------------

Some solvers, such as the forward dynamics and inverse kinematics solvers,
produce sequences of model states that are typically written to ``.sto`` files.
You can load an ``sto`` file like this:

TODO

The loaded states are "filled in" with the contents of the ``.sto`` file, but
may require further processing steps in order to be useful. For example, scripts
may need to realize the loaded states to an appropriate simulation stage in
order to read quantities of interest from the state:

TODO


Extract Quantities from Model (+ States)
----------------------------------------

TODO

Plot Quantities
---------------

TODO
