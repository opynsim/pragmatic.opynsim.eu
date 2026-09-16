Load Model (+States), Plot Stuff
================================

This guide goes through the process of using ``opensim`` to load a model from
an ``.osim`` file and (optionally) load states from a ``.sto`` file,
followed by plotting quantities of interest with ``matplotlib``. This is a
simple process that's extremely useful to master, because automating "open data
files and plot things" is a very common workflow.

Setup Example Data
------------------

If you want to run the Python code in this guide, you must first set up the
:doc:`../setup/example-data`.


Load a Model
------------

Loading an OpenSim model from an ``.osim`` file is achieved by passing
the file's path as a string to the ``opensim.Model`` constructor:

.. code:: python

    import opensim

    model = opensim.Model("pragmatic_resources/gait2354/gait2354.osim")

You can also use Python's in-built ``pathlib.Path`` to construct paths, which
can be useful certain tasks. Just remember to convert the ``pathlib.Path``
into a string (``str``) before passing it to OpenSim:

.. code:: python

    import opensim
    from pathlib import Path

    # Iterate over all `.osim` files in a directory
    models = {}
    for osim in Path("pragmatic_resources/gait2354").glob("*.osim"):
        models[osim.name] = opensim.Model(str(osim))  # note: `str`


Load States From a File
-----------------------

Some solvers, such as the forward dynamics and inverse kinematics solvers,
produce sequences of model states that are typically written to ``.sto`` or
``.mot`` files. You can load those files like this:

.. code:: python

    import opensim

    model = opensim.Model("pragmatic_resources/gait2354/subject01.osim")
    model.initSystem()

    # Load state data into a table
    states_table = opensim.TimeSeriesTable("pragmatic_resources/gait2354/OutputReference/subject01_walk1_ik.mot")

    # Ensure table data is in radians
    if opensim.TableUtilities.isInDegrees(states_table):
        model.getSimbodyEngine().convertDegreesToRadians(states_table)

    # Load data into states
    states = opensim.StatesTrajectory.createFromStatesTable(
        model,
        states_table,
        allowMissingColumns=True,  # Some solvers do not fill in all available states
        allowExtraColumns=True,    # Some data files in the wild contain extra columns
        assemble=False             # (your choice)
    ).getStateArray()

    # `states` can then be iterated over to yield each state.
    for state in states:
        print(state.getTime())

You can load the raw state data from data files without a model (``states_table``),
but a model (``model``) is required to convert the data into a usable state
trajectory (``states``). This is because the model contains contextual information
that's necessary to (e.g.) figure out which columns represent angular quantities.


Realize / Compute Derived State Quantities
------------------------------------------

States created from files/tables are only "filled in" with whatever
was in that data. This is because the "filling in" code doesn't
know, for example, that the calling code intends on modifying the states
by re-equilibrating muscles every step, or that it plans on extracting
outputs that depend on derived quantities in the states.

OpenSim models have methods that realize/compute things in its associated
state(s). For example, you could use ``model.realizePosition(state)``
to ensure any position-dependent outputs can be read from the state:

.. code:: python

    import opensim

    # Read model + states
    model = opensim.Model("pragmatic_resources/gait2354/subject01.osim")
    model.initSystem()
    states_table = opensim.TimeSeriesTable("pragmatic_resources/gait2354/OutputReference/subject01_walk1_ik.mot")
    if opensim.TableUtilities.isInDegrees(states_table):
        model.getSimbodyEngine().convertDegreesToRadians(states_table)
    states = opensim.StatesTrajectory.createFromStatesTable(model, states_table, True).getStateArray()

    # Realize each state to position stage
    for state in states:
        model.realizePosition(state)

The two most common state-update steps when loading data are:

``model.realizeX(state)``
    Realizes ``state`` to stage ``X``, making derived quantities
    that depend on ``X`` readable. If in doubt, use ``model.realizeReport(state)``.
    ``Report`` is the latest stage (`stage list <https://simbody.github.io/3.8.0/classSimTK_1_1Stage.html#ac3ebdb6f8942a72c65886e5286dd8a13>`_).

    **Beware**: "readable" does not mean "valid". Realizing a state that was
    partially filled-in can make derived/later stages invalid. For example,
    reading kinematics data (positions, rotations) from an ``.sto`` file
    into a state and using ``.realizeDynamics`` on it does not correctly
    calculate the state's dynamics. In that case, an Inverse Dynamics
    (ID) solver is required.

``model.equilibrateMuscles(state)``
   Updates ``state`` such that all of ``model``'s muscles are in equilibrium
   for that ``state``.

   **Beware**: this can be useful for getting equilibrium quantities (e.g.
   tendon lengths) from a freshly-loaded model, but muscles aren't always
   in equilibrium in a real experiment. To figure out actual muscle state(s),
   you need something like Computed Muscle Control (CMC) or Reduced Muscle
   Redundancy (RMR) solvers.


Extract Quantities from Model (+ States)
----------------------------------------

Once you have a model with prepared/realized states, you can then start
extracting state-dependent data from it.

OpenSim contains a huge amount of specialized extraction functions. OpenSim's
`Doxygen <https://simtk.org/api_docs/opensim/api_docs/>`_ documentation
outlines those methods (it's C++, but many methods are exported to Python) and
OpenSim's source code contains `example python scripts <https://github.com/opensim-org/opensim-core/tree/main/Bindings/Python/examples>`_.

Alternatively, you can use a combination of OpenSim's component API
(``model.getComponent(path)``, ``model.getComponentList()``) and its output
API (``component.getOutputNames()``, ``component.getOutput(name)``), which is
a general way of extracting some types of outputs.

The example below shows a few different ways of extracting data
from a model+states:

.. code:: python

    import opensim

    # Read and prepare model + states
    model = opensim.Model("pragmatic_resources/gait2354/subject01.osim")
    model.initSystem()
    states_table = opensim.TimeSeriesTable("pragmatic_resources/gait2354/OutputReference/subject01_walk1_ik.mot")
    if opensim.TableUtilities.isInDegrees(states_table):
        model.getSimbodyEngine().convertDegreesToRadians(states_table)
    states = opensim.StatesTrajectory.createFromStatesTable(model, states_table, allowMissingColumns=True).getStateArray()
    for state in states:
        model.realizeReport(state)

    # Collect data using specialized extraction functions (each component has
    # different functions).
    timepoints = []
    com_xy = []
    for state in states:
        timepoints.append(state.getTime())
        com_xy.append(model.calcMassCenterPosition(state).to_numpy()[0:2])

    # Collect Vec3 data as numpy arrays using generalized outputs (almost
    # all components have outputs).
    example_vec3_outputs = [
        ("/markerset/R.ASIS", "location"       ),
        ("/bodyset/femur_r",  "linear_velocity"),
    ]
    example_vec3_values = {}
    for component_path, output_name in example_vec3_outputs:
        component = model.getComponent(component_path)
        output = opensim.OutputVec3.safeDownCast(component.getOutput(output_name))
        values = []
        for state in states:
            values.append(output.getValue(state).to_numpy())
        example_vec3_values[f"{component_path}.{output_name}"] = values

    # Collect float data using generalized outputs (almost all
    # components have outputs).
    example_float_outputs = [
        ("/forceset/glut_med1_r/path",     "length"    ),
        ("/jointset/hip_r/hip_rotation_r", "value"     ),
        ("/forceset/intobl_l",             "activation"),
    ]
    example_float_values = {}
    for component_path, output_name in example_float_outputs:
        component = model.getComponent(component_path)
        output = opensim.OutputDouble.safeDownCast(component.getOutput(output_name))
        values = []
        for state in states:
            values.append(output.getValue(state))
        example_vec3_values[f"{component_path}.{output_name}"] = values

    # Specific example: collect a moment arm curve.
    initial_state = states[0]
    muscle_path = opensim.GeometryPath.safeDownCast(model.getComponent("/forceset/tfl_r/path"))
    coordinate = opensim.Coordinate.safeDownCast(model.getComponent("/jointset/knee_r/knee_angle_r"))
    num_sample_points = 64
    moment_arm_points = []
    for i in range(num_sample_points):
        x = coordinate.getRangeMin() + i/num_sample_points*coordinate.getRangeMax()
        coordinate.setValue(initial_state, x, enforceConstraints=False)
        y = muscle_path.computeMomentArm(states[0], coordinate)
        moment_arm_points.append((x, y))

    # ... and then do something with your collected lists/dictionaries
    #     of data (next section)...

GUI tools like `OpenSim Creator <https://opensimcreator.com>`_ can be useful
for figuring out things like the absolute component path and the available
outputs of components in a model file (e.g. by right-clicking a component).


Plot Quantities
---------------

Once you have extracted data from the model, you can then plot it with
``matplotlib``.

Here is an example of plotting two outputs against each
other over a trajectory, change ``x_component``/``x_output``/``y_component``/``y_output``
to change what's plotted:

.. code:: python

    import matplotlib.pyplot as plt
    import opensim

    # Read and prepare model + states
    model = opensim.Model("pragmatic_resources/gait2354/subject01.osim")
    model.initSystem()
    states_table = opensim.TimeSeriesTable("pragmatic_resources/gait2354/OutputReference/subject01_walk1_ik.mot")
    if opensim.TableUtilities.isInDegrees(states_table):
        model.getSimbodyEngine().convertDegreesToRadians(states_table)
    states = opensim.StatesTrajectory.createFromStatesTable(model, states_table, allowMissingColumns=True).getStateArray()
    for state in states:
        model.realizeReport(state)

    # Find appropriate outputs
    x_component = model.getComponent("/jointset/hip_r/hip_rotation_r")
    x_output = opensim.OutputDouble.safeDownCast(x_component.getOutput("value"))
    y_component = model.getComponent("/forceset/glut_med1_r/path")
    y_output = opensim.OutputDouble.safeDownCast(y_component.getOutput("length"))

    # Collect output values from each state
    points = []
    for state in states:
        x = x_output.getValue(state)
        y = y_output.getValue(state)
        points.append((x, y))

    # Plot
    x, y = zip(*points)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, color="tab:blue", linewidth=1.5)
    ax.set_title(f"{x_component.getName()}.{x_output.getName()} vs {y_component.getName()}.{y_output.getName()}")
    ax.set_xlabel(f"{x_component.getName()}.{x_output.getName()}")
    ax.set_ylabel(f"{y_component.getName()}.{y_output.getName()}")
    plt.show()
