Solve Forward Dynamics
======================

Once a model has been :doc:`loaded <load-model-state-plot-stuff>` or
:doc:`made <make-a-pendulum>`, it can be used to solve things.

One thing to solve is the model's forward dynamics (FD), which calculates
the model's motion (accelerations, velocities, and positions) over time
from forces/torques applied to it. FD is what's
shown when you press the run/play button in
`OpenSim Creator <https://www.opensimcreator.com/>`_ and
`OpenSim <https://opensim.stanford.edu/>`_. It can be useful to diagnose how
models behave in motion.


Setup Example Data
------------------

If you want to run the Python code in this guide, you must first set up the
:doc:`../setup/example-data`.

Alternatively, because forward dynamics can be solved for any model, you can
use your own model file, or :doc:`make your own in Python <make-a-pendulum>`.


Load Model, Create Initial State
--------------------------------

Loading an OpenSim model and establishing an initial state is the first step
in running a forward dynamics simulation. When you call ``model.initSystem()``,
OpenSim allocates and initializes a default system state where coordinates and
speeds are set to their default values (dictated by the coordinates'
``default_value`` property).

However, the initial state does not have to remain at these default values. You
can modify the state programmatically before handing it over to a solver. This
lets you (e.g.) adjust joint coordinate values or initial speeds before starting
the simulation.

Here is a Python script that loads a model, initializes its state, modifies a
coordinate value, and prepares it for simulation:

.. code:: python

    import opensim

    # Load model from file
    model = opensim.Model("pragmatic_resources/gait2354/gait2354.osim")

    # Initialize the system to create a valid initial state
    state = model.initSystem()

    # (Optional) Modify the initial state before simulation
    # For example, set a knee angle coordinate to 0.5 radians
    coordinate = opensim.Coordinate.safeDownCast(model.getComponent("/jointset/knee_r/knee_angle_r"))
    coordinate.setValue(state, 0.5, enforceConstraints=True)

    # Realize the state to position stage so it's ready for integration
    model.realizePosition(state)


Create Integrator (Manager)
---------------------------

Once you have a model and a prepared initial state, you can use an
``opensim.Manager`` to numerically integrate the system forward in time.
The manager wraps SimTK's integration engine (such as Runge-Kutta or Verlet
integrators) to solve the governing differential equations of motion.

You can configure several options on the manager or its underlying integrator,
including integration accuracy, maximum step size, and the integrator method itself.

Here is a complete script that sets up a manager, configures simulation parameters,
and solves the forward dynamics for 2.0 seconds:

.. code:: python

    import opensim

    # Read model and initialize state
    model = opensim.Model("pragmatic_resources/gait2354/gait2354.osim")
    state = model.initSystem()

    # Create the simulation manager
    manager = opensim.Manager(model)

    # Initialize the manager with the starting state and time
    manager.initialize(state)
    initial_time = state.getTime()
    final_time = initial_time + 2.0

    # Run the forward dynamics simulation
    print(f"Running simulation from {initial_time}s to {final_time}s...")
    final_state = manager.integrate(final_time)
    print("Simulation complete!")


Save Resulting Trajectory
-------------------------

Once the forward dynamics simulation is finished, you will typically want to write
the resulting motion trajectory to disk so it can be inspected or analyzed later.
You can extract the states data from the manager as a ``TimeSeriesTable`` using
``manager.getStatesTable()``, and then save it using OpenSim's ``STOFileAdapter``.

The resulting ``.sto`` file can be loaded directly into visualization tools like
`OpenSim Creator <https://www.opensimcreator.com/>`_ or the OpenSim GUI,
or loaded programmatically via OPynSim.

Here is how you can extract and save the states table:

.. code:: python

    import opensim

    # Load model, initialize state, and run forward dynamics
    model = opensim.Model("pragmatic_resources/gait2354/gait2354.osim")
    state = model.initSystem()
    manager = opensim.Manager(model)
    manager.initialize(state)
    manager.integrate(2.0)

    # Extract the resulting states as a TimeSeriesTable
    states_table = manager.getStatesTable()

    # Save the table to an `.sto` file
    output_filepath = "gait2354_forward_dynamics_states.sto"
    opensim.STOFileAdapter.write(states_table, output_filepath)
    print(f"Saved trajectory to {output_filepath}")


Interoperability With OPynSim
-----------------------------

Model files, and the ``.sto`` files generated above, can be loaded via the
OPynSim API, which is handy for visualizing and plotting the results. See
:doc:`load-data-into-dataframes` and :doc:`render-model-states-to-video` for
information on how to do that.

Alternatively, you can perform the entire procedure using OPynSim's ``ForwardDynamicSolver``:

.. code:: python

    import matplotlib.pyplot as plt
    import numpy as np
    import opynsim as opyn
    from opynsim.solvers import ForwardDynamicsSolver

    # Load model, integrate it at 100 Hz to 2 seconds.
    model = opyn.read_osim("pragmatic_resources/gait2354/gait2354.osim").compile()
    states = [model.initial_state(realized_to=opyn.STAGE_ACCELERATION)]
    fd_solver = ForwardDynamicsSolver(model, states[0])
    rate = 1/10
    for t in np.arange(rate, 2 + rate, rate):
        print(f"Integrating to {t:.2f}s...")
        states.append(fd_solver.integrate_to(t, realized_to=opyn.STAGE_ACCELERATION))

    # Extract time series data across the accumulated states
    output_path = "/bodyset/tibia_r[position]"
    times = []
    output_values = []
    for state in states:
        times.append(state.time)
        output_values.append(model.get_output_value(state, output_path)[1])

    # Plot the time series using matplotlib
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(times, output_values, color="tab:blue", linewidth=1.5)
    ax.set_title(f"Forward Dynamics: {output_path}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Value (rad)")
    ax.grid(True, linestyle="--", alpha=0.6)
    plt.show()



