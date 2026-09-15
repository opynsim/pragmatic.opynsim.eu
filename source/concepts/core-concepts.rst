Core Concepts
=============

This page briefly outlines general core concepts that are frequently
referenced when working on musculoskeletal simulation projects,
irrespective of the simulator (e.g. OpenSim, OPynSim, MuJoCo). The
:doc:`opensim-concepts` and :doc:`opynsim-concepts` explain specific
concepts about those simulators.


Common Mathematical Datastructures
----------------------------------

At its foundation, musculoskeletal modeling relies on linear algebra
to describe spatial locations, orientations, and movements:

- **Vectors/Arrays:** Data structures that can be used to represent positions,
  velocities, accelerations, or force vectors in 3D space. This differs from
  mathematical literature, where a **point** defines a fixed location in space
  relative to an origin and a **vector** represents a direction and magnitude
  independent of location. Both are typically represented interchangeably
  by a vector/array (in Python, usually by a `NumPy array <https://numpy.org/doc/stable/reference/generated/numpy.array.html>`_).

- **Reference Frames (Transforms):** A **frame** defines an origin point and a
  set of orthogonal :math:`X, Y, Z` axes. Moving **vectors** or **points** between
  frames requires a **Transform**. The distinction between a **point** and a
  **vector** is that points translate and rotate, whereas vectors only rotate
  (i.e. the transform's translation is ignored for vectors). In the literature,
  and most software APIs, frames are often synonymously called **Transforms**,
  **Rigid Transforms**, **Pose**, or **Coordinate Systems**.

.. admonition:: Pragmatic Programming Takeaway

   TODO: explain how these are useful, what they pragmatically mean for
   Python programmers, etc.


Common Coordinate Systems
-------------------------

Musculoskeletal models contain multiple coexisting coordinate
systems to make local definitions intuitive. Here are some
commonly used coordinate system types:

- **Ground (World Frame):** The top-level inertial reference frame that serves
  as the immovable "universe" or origin :math:`(0,0,0)` of the simulation. Ground
  acts as the root node for the entire kinematic tree.

- **Body-Centered (Local) Frames:** Rigid bodies (e.g., Femur, Tibia) define
  their inertial properties, mass center relative to a local origin fixed to
  that specific body.

- **Custom/Offset Frames:** Musculoskeletal models may define frames *within*
  ground, body, or other custom frames. For example, a femur joint parent frame
  might be defined within the pelvis body frame.

- **Joint-Centered Frames:** Joints may define axes of rotation and translation
  by referencing frames relative to the connected parent and child bodies. For
  example, a hip joint may reference both a frame on the parent (pelvis) and
  child (femur) bodies, or custom frames defined within those.

- **Non-Cartesian Coordinate Systems:** While 3D spatial points use Cartesian
  coordinates :math:`(x, y, z)`, certain parts of a model may rely on
  alternative representations. For example, **cylindrical coordinates** $(\rho, \phi, z)$
  might be the best way to describe a muscle wrapping over a cylinder. **Spherical coordinates**
  may tbe the best representation of a ball-in-socket joint, and so on.

.. admonition:: Pragmatic Programming Takeaway

   Defining geometry in local body frames keeps models modular and
   reusable. However, during computational steps (such as inverse kinematics,
   collision detection, or equations of motion), physics engines transform
   local spatial vectors into the unified **Ground** frame to perform global
   calculations.


Kinematic Chains & Trees
------------------------

A **Kinematic Chain** refers to an assembly of rigid bodies connected by joints that constrain their relative motion. In musculoskeletal modeling:

1. **Topology:** Models form an open-loop or closed-loop **joint hierarchy (tree graph)** rooted at the **Ground** environment frame.
2. **Degrees of Freedom (DoFs):** Each joint specifies the permissible relative motion between a parent and child body (e.g., a Pin/Hinge joint allows 1 rotational DoF; a Free joint allows 6 DoFs). In OpenSim nomenclature, these DoFs are managed as individual **Coordinates** ($q$).

To construct a valid model, every body must attach to the root frame through a continuous kinematic chain. Unattached bodies cause singular system matrices during computation.


Physics Systems
---------------

A **Physics System** combines the structural kinematic tree with physical laws, forces, and mathematical constraints to evaluate or simulate physical movement:

- **Constraints:** Loop-closure constraints, coordinate couplings, or point-on-line constraints that further restrict motion beyond joint definitions.
- **Force Elements:** Passive forces (gravity, contact dynamics, spring-dampers) and active forces (actuators, Hill-type muscle models).
- **System Solvers:** Numerical engines that process state equations to solve key biomechanical problems:

  - **Forward Dynamics:** Integrates equations of motion forward in time given muscle activations to compute resulting accelerations and trajectories.
  - **Inverse Kinematics (IK):** Finds joint coordinates ($q$) that minimize the distance between experimental motion capture markers and model markers.
  - **Inverse Dynamics (ID):** Calculates net joint moments required to produce a given set of kinematically observed accelerations.


Model Specification
-------------------

A **Model Specification** is a static, declarative data structure—often serialized as a hierarchical XML, JSON, or `URDF <http://wiki.ros.org/urdf>`_ file—that defines the topology and properties of a physics system.

Regardless of the underlying software engine (`OpenSim .osim <https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53089012/OpenSim+Files>`_, `MuJoCo .xml <https://mujoco.readthedocs.io/en/stable/XML-reference.html>`_, or `OPynSim`), a model specification outlines:

- **Rigid Bodies:** Mass, center of mass location, inertia tensor, and attached geometry.
- **Joints:** Parent/child attachments, transform offsets, and coordinate limits.
- **Actuators & Path Objects:** Muscle origin/insertion sites, via-points, and force properties.

Crucially, the Model Specification is **static parameter storage**; it contains no runtime variable data (such as current velocities or time step states).


Model State
-----------

A **Model State** represents the instantaneous physical condition of a dynamic system at a specific time point $t$.

While the *Model Specification* defines what the system *is*, the *State* defines what the system *is currently doing*. A complete state vector usually contains:

- **Time ($t$):** The current timestamp of the system.
- **Generalized Positions ($q$):** Joint angle or translation values across all DoFs.
- **Generalized Velocities ($u$):** Rate of change of coordinates ($\dot{q}$).
- **Auxiliary States ($z$):** Non-mechanical variable states, such as muscle fiber lengths and physiological muscle activation levels.
