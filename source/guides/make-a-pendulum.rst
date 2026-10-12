Make a Pendulum
===============

This guide goes through the process of making a simple pendulum
OpenSim model using the ``opensim`` Python package. The utility
of building a model programmatically is that you can automate
and parameterize how things are built.

This guide **roughly** mirrors OpenSim Creator's `Make a Pendulum Tutorial <https://docs.opensimcreator.com/manual/en/latest/make-a-pendulum.html>`_,
which explains building the same model, but through a GUI - and with
more explanations of OpenSim's coordinate systems. We recommend going
through that tutorial if you want multiple perspectives on this process.

When building a model, it's useful to keep OpenSim's :ref:`opensim_model_component_arch`
in mind, because building an OpenSim model is mostly about adding components to an
``opensim.Model``, setting their properties/sockets, and building a physics system of
the model.


Create a New Model
------------------

Models are built through the ``opensim.Model`` class. The first step is to make a
blank ``Model``:

.. code-block:: python

    import opensim as osim

    model = osim.Model()

This creates a model with nothing in it (effectively, it just creates a ground frame).


Sidenote: Saving/Visualizing Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**A useful thing to know for the rest of this guide** is you can usually save a model
during the construction process using ``Model.printToXML``, which lets you inspect
the resulting XML (``.osim``), open the osim file in other software, etc. to debug
what's happening:

.. code-block:: python

    import opensim as osim

    model = osim.Model()

    # Writes `model` to a file called `blank-model.osim`.
    model.finalizeConnections()  # Sometimes necessary (described below).
    model.printToXML("blank-model.osim")

    # Example: visualize `blank-model.osim` in its initial state.
    import opynsim as opyn
    import opynsim.ui
    opyn_model = opyn.read_osim("blank-model.osim").compile()
    opyn.ui.show_model_in_state(opyn_model, opyn_model.initial_state(realized_to=opyn.STAGE_REPORT))

    # Example: visualize `blank-model.osim` in OpenSim Creator.
    import subprocess
    subprocess.run(["osc", "blank-model.osim"])

Sometimes ``model.finalizeConnections()`` must be called before ``model.printToXML()`` to ensure
that the model's sockets are written to the file. This is a technical detail. When in doubt,
finalize them.


Add a Body with a WeldJoint
---------------------------

The next step is to add a body that the pendulum head swings on. We do this by
adding a ``WeldJoint`` and ``Body`` to the ``Model``:

.. code-block:: python

    import opensim as osim

    model = osim.Model()

    pendulum_base = osim.Body(          # Make pendulum base body
        "pendulum_base",                # Name (used for lookups)
        1.0,                            # Mass (in kg)
        osim.Vec3(0),                   # Center of Mass (w.r.t. body frame)
        osim.Inertia(1, 1, 1, 0, 0, 0)  # Inertia tensor (Ixx, Iyy, Izz, Ixy, Ixz, Iyz)
    )
    model.addBody(pendulum_base)        # Add pendulum base body to model

    brick = osim.Brick(                 # Make brick (optional: for visualization)
        osim.Vec3(0.1)                  # Brick half-lengths in each axis
    )
    pendulum_base.attachGeometry(brick) # Attach brick to pendulum base

    weld_joint = osim.WeldJoint(        # Make joint
        "base_weld",                    # Name (used for lookups)
        model.getGround(),              # Parent frame
        osim.Vec3(0, 1.0, 0),           # Offset in parent frame
        osim.Vec3(0),                   # Orientation in parent frame
        pendulum_base,                  # Child frame
        osim.Vec3(0),                   # Offset in child frame
        osim.Vec3(0),                   # Orientation in child frame
    )
    model.addJoint(weld_joint)          # Add joint to model


Typically, whenever a body is added to an OpenSim model, you should also add a joint
so that it's clear where the body should be placed and what degrees of freedom it
should have. Otherwise, when creating the physics system (described later), OpenSim
will automatically join the body to ground with a ``FreeJoint``, which may not be
what you want.


Add the Pendulum Head
---------------------

The next step is to add a ``pendulum_head`` body connected to pendulum_base via
an OpenSim PinJoint (``osim.PinJoint``).

To ensure the pendulum hangs with its base 1 m above ground and its head 0.5 m above
ground, we position the joint so that the parent frame is located at ``pendulum_base``
(zero offset when it's the parent) and the child frame is offset by 0.5 m along the
Y-axis (with respect to the ``pendulum_head``). We also attach a ``Sphere`` decoration
to the head:

.. code-block:: python

    import opensim as osim

    model = osim.Model()

    pendulum_base = osim.Body(          # Make pendulum base body
        "pendulum_base",                # Name (used for lookups)
        1.0,                            # Mass (in kg)
        osim.Vec3(0),                   # Center of Mass (w.r.t. body frame)
        osim.Inertia(1, 1, 1, 0, 0, 0)  # Inertia tensor (Ixx, Iyy, Izz, Ixy, Ixz, Iyz)
    )
    model.addBody(pendulum_base)        # Add pendulum base body to model

    brick = osim.Brick(                 # Make brick (optional: for visualization)
        osim.Vec3(0.1)                  # Brick half-lengths in each axis
    )
    pendulum_base.attachGeometry(brick) # Attach brick to pendulum base

    weld_joint = osim.WeldJoint(        # Make joint
        "base_weld",                    # Name (used for lookups)
        model.getGround(),              # Parent frame
        osim.Vec3(0, 1.0, 0),           # Offset in parent frame
        osim.Vec3(0),                   # Orientation in parent frame
        pendulum_base,                  # Child frame
        osim.Vec3(0),                   # Offset in child frame
        osim.Vec3(0),                   # Orientation in child frame
    )
    model.addJoint(weld_joint)          # Add joint to model

    pendulum_head = osim.Body(          # Make pendulum head body
        "pendulum_head",                # Name (used for lookups)
        1.0,                            # Mass (in kg)
        osim.Vec3(0),                   # Center of Mass (w.r.t. body frame)
        osim.Inertia(1, 1, 1, 0, 0, 0)  # Inertia tensor (Ixx, Iyy, Izz, Ixy, Ixz, Iyz)
    )
    model.addBody(pendulum_head)        # Add pendulum head body to model

    sphere = osim.Sphere(               # Make sphere (optional: for visualization)
        0.1                             # Sphere radius
    )
    pendulum_head.attachGeometry(sphere)  # Attach sphere to pendulum head

    pin_joint = osim.PinJoint(          # Make pin joint
        "head_pin",                     # Name (used for lookups)
        pendulum_base,                  # Parent frame
        osim.Vec3(0),                   # Offset in parent frame
        osim.Vec3(0),                   # Parent orientation
        pendulum_head,                  # Child frame
        osim.Vec3(0, 0.5, 0),           # Offset in child frame (joint is 0.5 m above head)
        osim.Vec3(0),                   # Child orientation
    )
    model.addJoint(pin_joint)           # Add joint to model


Build Pendulum's Physics System
-------------------------------

Up to this point, you have been defining the model specification (in OPynSim, referred
to as ModelSpecification). This describes the components, joints, and geometry of the
system, but does not yet instantiate the underlying multibody dynamics equations.

To build the physics system, call ``.initSystem()`` on the model:

.. code-block:: python

    # (assumes `model` has been built, as above)

    state = model.initSystem()  # Initialize the physics system

This assembles the model, allocates internal memory structures, and
populates a default state (where all coordinates are set to their default
values, typically zero). Once built, you can manipulate the state and
compute system-level kinematics and dynamics.


Plot Quantities of Interest
---------------------------

With the physics system built, you can manipulate the state to evaluate
quantities of interest across different configurations, such as the
acceleration of the pendulum head at various angles, without needing to
run a full time-stepping forward dynamics simulation.

Here is how you set a coordinate value, realize the state to acceleration, and
query the head's linear acceleration vector:

.. code-block:: python

    # (assumes `model` has been built and physics system built, as above)

    import matplotlib.pyplot as plt
    import numpy as np

    # Get pin joint coordinate
    coord = model.getCoordinateSet().get("head_pin_coord_0")

    # Define a sample grid (-π to π, 200 steps)
    angles = np.linspace(-np.pi, np.pi, 200)

    # Sample accelerations of the pendulum head for each angle
    accelerations_x = []
    for angle in angles:
      coord.setValue(state, angle)
      model.realizeAcceleration(state)
      accel_x = pendulum_head.getLinearAccelerationInGround(state).get(0)
      accelerations_x.append(accel_x)

    # Plot
    plt.plot(np.degrees(angles), accelerations_x)
    plt.xlabel("Pendulum Angle (degrees)")
    plt.ylabel("Head X-Acceleration ($m/s^2$)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()

Note: Because we manually set the coordinate value and realized the state
statically, the velocity and acceleration terms due to motion dynamics (like
initial velocities) are zero unless explicitly configured. Forward dynamics
simulations (covered separately) handle time-integration.


Make the Pendulum Look Nicer
----------------------------

To make the model visually polished, we can refine the dimensions of the base
and head decorations and introduce a cylinder representing the pendulum's neck.

The neck is added by defining an OffsetFrame on pendulum_head shifted
halfway up (0.25 m), and attaching a Cylinder to that offset frame:

.. code-block:: python

    import opensim as osim

    model = osim.Model()

    pendulum_base = osim.Body(          # Make pendulum base body
        "pendulum_base",                # Name (used for lookups)
        1.0,                            # Mass (in kg)
        osim.Vec3(0),                   # Center of Mass (w.r.t. body frame)
        osim.Inertia(1, 1, 1, 0, 0, 0)  # Inertia tensor (Ixx, Iyy, Izz, Ixy, Ixz, Iyz)
    )
    model.addBody(pendulum_base)        # Add pendulum base body to model

    brick = osim.Brick(                 # Make brick (optional: for visualization)
        osim.Vec3(0.1)                  # Brick half-lengths in each axis
    )
    pendulum_base.attachGeometry(brick) # Attach brick to pendulum base

    weld_joint = osim.WeldJoint(        # Make joint
        "base_weld",                    # Name (used for lookups)
        model.getGround(),              # Parent frame
        osim.Vec3(0, 1.0, 0),           # Offset in parent frame
        osim.Vec3(0),                   # Orientation in parent frame
        pendulum_base,                  # Child frame
        osim.Vec3(0),                   # Offset in child frame
        osim.Vec3(0),                   # Orientation in child frame
    )
    model.addJoint(weld_joint)          # Add joint to model

    pendulum_head = osim.Body(          # Make pendulum head body
        "pendulum_head",                # Name (used for lookups)
        1.0,                            # Mass (in kg)
        osim.Vec3(0),                   # Center of Mass (w.r.t. body frame)
        osim.Inertia(1, 1, 1, 0, 0, 0)  # Inertia tensor (Ixx, Iyy, Izz, Ixy, Ixz, Iyz)
    )
    model.addBody(pendulum_head)        # Add pendulum head body to model

    sphere = osim.Sphere(               # Make sphere (optional: for visualization)
        0.1                             # Sphere radius
    )
    pendulum_head.attachGeometry(sphere)  # Attach sphere to pendulum head

    neck_frame = osim.PhysicalOffsetFrame(  # NEW: add a frame for the pendulum's "neck"
        "neck_frame",                       # Name (used for lookups)
        pendulum_head,                      # Parent frame
        osim.Transform(osim.Vec3(0, -0.25, 0))  # Transform in parent frame
    )
    model.addComponent(neck_frame)          # Add neck frame to model
    cylinder = osim.Cylinder(               # Make Cylinder (neck geometry)
        0.01,                               # Cylinder radius
        0.25                                # Cylinder half-lengths along Y
    )
    neck_frame.attachGeometry(cylinder)     # Add cylinder to neck frame

    pin_joint = osim.PinJoint(          # Make pin joint
        "head_pin",                     # Name (used for lookups)
        pendulum_base,                  # Parent frame
        osim.Vec3(0),                   # Offset in parent frame
        osim.Vec3(0),                   # Parent orientation
        pendulum_head,                  # Child frame
        osim.Vec3(0, 0.5, 0),           # Offset in child frame (joint is 0.5 m above head)
        osim.Vec3(0),                   # Child orientation
    )
    model.addJoint(pin_joint)           # Add joint to model


Complete Script
---------------

Here is the complete, end-to-end script building the polished pendulum model
from scratch and saving it to disk:

.. code-block:: python

    import opensim as osim

    model = osim.Model()

    pendulum_base = osim.Body(          # Make pendulum base body
        "pendulum_base",                # Name (used for lookups)
        1.0,                            # Mass (in kg)
        osim.Vec3(0),                   # Center of Mass (w.r.t. body frame)
        osim.Inertia(1, 1, 1, 0, 0, 0)  # Inertia tensor (Ixx, Iyy, Izz, Ixy, Ixz, Iyz)
    )
    model.addBody(pendulum_base)        # Add pendulum base body to model

    brick = osim.Brick(                 # Make brick (optional: for visualization)
        osim.Vec3(0.1)                  # Brick half-lengths in each axis
    )
    pendulum_base.attachGeometry(brick) # Attach brick to pendulum base

    weld_joint = osim.WeldJoint(        # Make joint
        "base_weld",                    # Name (used for lookups)
        model.getGround(),              # Parent frame
        osim.Vec3(0, 1.0, 0),           # Offset in parent frame
        osim.Vec3(0),                   # Orientation in parent frame
        pendulum_base,                  # Child frame
        osim.Vec3(0),                   # Offset in child frame
        osim.Vec3(0),                   # Orientation in child frame
    )
    model.addJoint(weld_joint)          # Add joint to model

    pendulum_head = osim.Body(          # Make pendulum head body
        "pendulum_head",                # Name (used for lookups)
        1.0,                            # Mass (in kg)
        osim.Vec3(0),                   # Center of Mass (w.r.t. body frame)
        osim.Inertia(1, 1, 1, 0, 0, 0)  # Inertia tensor (Ixx, Iyy, Izz, Ixy, Ixz, Iyz)
    )
    model.addBody(pendulum_head)        # Add pendulum head body to model

    sphere = osim.Sphere(               # Make sphere (optional: for visualization)
        0.1                             # Sphere radius
    )
    pendulum_head.attachGeometry(sphere)  # Attach sphere to pendulum head

    neck_frame = osim.PhysicalOffsetFrame(  # NEW: add a frame for the pendulum's "neck"
        "neck_frame",                       # Name (used for lookups)
        pendulum_head,                      # Parent frame
        osim.Transform(osim.Vec3(0, -0.25, 0))  # Transform in parent frame
    )
    model.addComponent(neck_frame)          # Add neck frame to model
    cylinder = osim.Cylinder(               # Make Cylinder (neck geometry)
        0.01,                               # Cylinder radius
        0.25                                # Cylinder half-lengths along Y
    )
    neck_frame.attachGeometry(cylinder)     # Add cylinder to neck frame

    pin_joint = osim.PinJoint(          # Make pin joint
        "head_pin",                     # Name (used for lookups)
        pendulum_base,                  # Parent frame
        osim.Vec3(0),                   # Offset in parent frame
        osim.Vec3(0),                   # Parent orientation
        pendulum_head,                  # Child frame
        osim.Vec3(0, 0.5, 0),           # Offset in child frame (joint is 0.5 m above head)
        osim.Vec3(0),                   # Child orientation
    )
    model.addJoint(pin_joint)           # Add joint to model

    state = model.initSystem()          # Building finished: initialize physics system

    # --- plot quantities of interest ---

    import matplotlib.pyplot as plt
    import numpy as np

    # Get pin joint coordinate
    coord = model.getCoordinateSet().get("head_pin_coord_0")

    # Define a sample grid (-π to π, 200 steps)
    angles = np.linspace(-np.pi, np.pi, 200)

    # Sample accelerations of the pendulum head for each angle
    accelerations_x = []
    for angle in angles:
      coord.setValue(state, angle)
      model.realizeAcceleration(state)
      accel_x = pendulum_head.getLinearAccelerationInGround(state).get(0)
      accelerations_x.append(accel_x)

    # Plot
    plt.plot(np.degrees(angles), accelerations_x)
    plt.xlabel("Pendulum Angle (degrees)")
    plt.ylabel("Head X-Acceleration ($m/s^2$)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


    # --- save output ---
    model.finalizeConnections()
    model.printToXML("pendulum.osim")   # Output: save model to `pendulum.osim`
