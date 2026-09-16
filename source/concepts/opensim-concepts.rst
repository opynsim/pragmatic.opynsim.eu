OpenSim Concepts
================

This page briefly outlines core concepts that are useful when working with
OpenSim. See :doc:`core-concepts` for a general explanation of musculoskeletal
modelling concepts.

Model & Component Architecture
------------------------------

In OpenSim, a ``Model`` is a top-level composite object composed of a tree of
``Component`` objects (e.g., bodies, joints, muscles, markers). Components contain
``Property`` objects, which store static parameters like mass, muscle optimal
fiber length, or geometry paths.

.. code-block:: python

   import opensim as os

   # Load a model specification from an .osim file
   model = os.Model("arm26.osim")

Object Lifecycle & Initialization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When creating or modifying an OpenSim model programmatically, changing a property
does **not** immediately update the underlying computational system. You must
pass the model through its lifecycle initialization sequence:

1. ``finalizeFromProperties()``: Updates internal component parameters
   after modifying properties.
2. ``finalizeConnections(model)``: Resolves topological linkages between
   components (e.g., connecting a muscle to a body frame).
3. ``buildSystem()`` / ``initSystem()``: Allocates the underlying physics
   system and generates an initial ``State`` object.

Model Assembly & Muscle Equilibration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before running analyses, models often require special initialization steps:

- **Model Assembly:** Moves coordinates ($q$) to satisfy kinematic assembly
  constraints (e.g., closed loop constraints).
- **Muscle Equilibration:** Solves for tendon strain and muscle fiber length to
  ensure the active/passive muscle forces balance at time $t=0$:

.. code-block:: python

   # Complete setup pipeline
   state = model.initSystem()
   model.equilibrateMuscles(state)


Component Tree Traversal & Modification
---------------------------------------

OpenSim structures objects in a hierarchical **Component Tree** using UNIX-style
path syntax (e.g., ``/jointset/elbow/elbow_coord_0``).

Traversing the Tree
^^^^^^^^^^^^^^^^^^^

You can inspect components or iterate through specific object types using
OpenSim's component list iterators:

.. code-block:: python

   # Print all muscle names in the model
   for muscle in model.getMuscleList():
       print(muscle.getName())

Modifying a Component
^^^^^^^^^^^^^^^^^^^^^

To modify an object deep in the tree—such as moving an attachment point for a
path muscle—retrieve the component, modify its property, and re-initialize the system:

.. code-block:: python

   # 1. Retrieve a muscle via path or getter
   biceps = model.getMuscleList().get("biceps")
   path = biceps.getGeometryPath()

   # 2. Modify an attachment point location (Vec3 in local frame)
   path.getPathPointSet().get(0).set_location(os.Vec3(0.01, -0.05, 0.0))

   # 3. Re-initialize the model lifecycle to apply changes
   model.finalizeFromProperties()
   state = model.initSystem()


State (``SimTK::State``)
------------------------

An OpenSim ``Model`` is strictly stateless and immutable during execution. All
dynamic variable data—time, coordinates, velocities, and muscle activations—are
stored inside a separate ``State`` object managed by the underlying SimTK engine.

Generating a State
^^^^^^^^^^^^^^^^^^

Calling ``model.initSystem()`` allocates the multibody system and returns a default
``State`` object:

.. code-block:: python

   state = model.initSystem()

State Vectors
^^^^^^^^^^^^^

The ``State`` encapsulates the continuous state variables of the system:

- **$q$ (Generalized Coordinates):** Joint angles and translations.
- **$u$ (Generalized Velocities):** Rate of change of coordinates ($\dot{q}$).
- **$z$ (Auxiliary States):** Non-mechanical variables, such as muscle activation
  levels ($a$) and muscle fiber lengths ($l_m$).
- **$y$:** The complete continuous state vector combining $[q, u, z]$.

Central Role in Execution
^^^^^^^^^^^^^^^^^^^^^^^^^

Almost every state-dependent method in OpenSim requires passing a ``State`` reference as
the first argument:

.. code-block:: python

   # Set coordinate value in the state
   coord = model.getCoordinateSet().get("elbow_flexion")
   coord.setValue(state, 1.57) # ~90 degrees in radians

   # Calculate total system mass center position given the current state
   com_pos = model.calcMassCenterPosition(state)


Frames & Spatial Transformations
--------------------------------

Every physical component in OpenSim exists within a ``Frame`` (e.g., ``Ground``,
``Body``, or ``PhysicalOffsetFrame``). Locations of points (such as muscle attachment
sites or marker locations) are defined locally within their parent frame.

Transforming Quantities Between Frames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To express a local position vector in another frame (e.g., transforming a muscle
attachment location into global ``Ground`` space), use the target frame's
spatial transformation methods:

.. code-block:: python

   # Get references to frames
   ground = model.getGround()
   femur = model.getBodySet().get("femur")

   # Point defined locally in the Femur frame
   local_point = os.Vec3(0.0, -0.2, 0.0)

   # Express the femur point in Ground coordinates given the current state
   ground_point = femur.findStationLocationInFrame(state, local_point, ground)


Outputs & Report Extraction
---------------------------

OpenSim components expose **Outputs**, which are calculated quantities that can be
evaluated for a given ``State``. Outputs allow you to extract data without manually
computing internal math.

Types of Outputs
^^^^^^^^^^^^^^^^

- **Single Value Outputs:** Single numbers or spatial vectors (e.g., muscle length,
  tendon force, frame origin position).
- **Output Lists:** Arrays of values evaluated over time.

Retrieving Output Values in Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can query an output directly by name from any component by passing the current
``State``:

.. code-block:: python

   biceps = model.getMuscles().get("biceps")

   # Obtain current muscle length (Output)
   length = biceps.getOutput("length").getValueAsString(state)

   # Obtain current muscle fiber force
   force = biceps.getOutput("fiber_force").getValueDouble(state)
   print(f"Biceps Fiber Force: {force} N")

Using `TableReporter`
^^^^^^^^^^^^^^^^^^^^^

For multi-step simulations or time-series data collection, connect component
Outputs to an OpenSim ``ConsoleReporter`` or ``TableReporter`` to automatically
aggregate data into a ``TimeSeriesTable`` for analysis in Pandas.


Useful Resources & External Links
---------------------------------

When developing custom scripts or pipeline tools in Python, these official documentation
repositories and code bases provide essential references and example code:

- `OpenSim API Doxygen Documentation <https://simtk.org/api_docs/opensim/api_docs/>`_: Essential for
  discovering available classes, inheritance trees, and component methods (e.g., checking what
  methods `Model`, `Muscle`, or `Coordinate` expose).
- `Simbody API Doxygen Documentation <https://simtk.org/api_docs/simbody/latest/>`_: Useful when working
  lower-level with vector algebra, spatial transforms (`SimTK::Transform`), numerical integrators, or
  `SimTK::State` internals.
- `OpenSim Core GitHub Repository <https://github.com/opensim-org/opensim-core>`_: The main C++ codebase. The `Bindings/Python/examples <https://github.com/opensim-org/opensim-core/tree/main/Bindings/Python/examples>`_ directory inside this repository contains official, working Python scripts demonstrating model building, inverse kinematics, and forward dynamics.
- `OpenSim Models Repository <https://github.com/opensim-org/opensim-models>`_: A repository containing standard, peer-reviewed musculoskeletal models (e.g., Rajagopal, Gait10dof18musc, Arm26) in `.osim` format, useful as starting points for custom workflows.
- `OpenSim Creator <https://github.com/scivision/opensim-creator>`_: An modern, alternative UI editor for building and inspecting `.osim` models, useful for visualizing component hierarchies and frame offsets.
