Solve Inverse Kinematics
========================

Inverse kinematics (IK) is the process of determining the joint
angles (coordinates) of an OpenSim model that best reproduce a set of marker
trajectories over time. Because motion capture data, virtual markers
from markerless tracking systems (such as `Pose2Sim <https://github.com/perfanalytics/pose2sim>`_),
or machine learning pipelines tend to produce spatial tracking data rather
than joint kinematics, IK is arguably the most common and fundamental
problem solved in biomechanical workflows.

This guide walks through loading experimental marker data, configuring and
executing OpenSim's inverse kinematics solver programmatically in Python,
working with the resulting motion trajectories, and transitioning to downstream
dynamic analyses.

Setup Example Data
------------------

If you want to run the Python code in this guide, you must first set up the
:doc:`../setup/example-data`.

Load Model and Marker (.trc) Files
----------------------------------

To run inverse kinematics, OpenSim requires two primary inputs: an OpenSim
model file (``.osim``) and an experimental marker data file (typically in ``.trc`` format).

You can inspect and load these files in Python using OpenSim's ``Model``
and ``TimeSeriesTableVec3`` classes.

.. code:: python

    import opensim

    # Load model and initialize system.
    model = opensim.Model("pragmatic_resources/gait2354/subject01.osim")
    model.initSystem()

    # Load marker data (3D point trajectory over time).
    marker_table = opensim.TimeSeriesTableVec3("pragmatic_resources/gait2354/subject01_walk1.trc")

    print(f"Loaded marker table with {marker_table.getNumRows()} time frames.")
    print(f"Marker labels: {marker_table.getColumnLabels()}")

.. admonition:: Make sure your data is valid

    Before running IK, ensure that:

    1. **Units match**: OpenSim models universally use meters for spatial
       dimensions, whereas experimental marker data files are frequently exported
       in millimeters. If your marker data is in millimeters, you must scale the
       coordinate columns accordingly.
    2. **Marker names match**: The marker names defined in the model's ``MarkerSet``
       must correspond exactly to the column headers in the ``.trc`` file. Unmatched
       markers will be ignored or cause warnings.


Create and Use Inverse Kinematics Solver
----------------------------------------

OpenSim provides the ``InverseKinematicsTool`` class to track marker
positions frame-by-frame by minimizing marker displacement errors
subject to the model's kinematic constraints.

You can configure and run ``InverseKinematicsTool`` programmatically or via
an XML setup file. The setup file has identical content to the one produced by
`OpenSim GUI <https://opensim.stanford.edu/>`_ when you press ``Save`` in
the IK tool, so this guide is also a good way to automate an otherwise
GUI-centric workflow. Here is how you would load the configuration XML file:

.. code-block:: python

    import opensim

    # Load model
    model = opensim.Model("pragmatic_resources/gait2354/subject01.osim")
    model.initSystem()

    # Example: Load an existing IK tool XML file (e.g. from OpenSim GUI).
    # ik_tool = opensim.InverseKinematicsTool("pragmatic_resources/gait2354/subject01_Setup_IK.xml")

    ik_tool = opensim.InverseKinematicsTool()

    # Further customize the configuration file (if desired).
    ik_tool.setName("subject01_ik")
    ik_tool.setModel(model)
    # Note: this is relative to the config XML file if you initially loaded one
    ik_tool.setMarkerDataFileName("pragmatic_resources/gait2354/subject01_walk1.trc")
    ik_tool.setStartTime(0.0)
    ik_tool.setEndTime(1.2)
    ik_tool.setOutputMotionFileName("subject01_walk1_ik.mot")

    # Optional: Customize individual marker weights
    # weights = ik_tool.getMarkerWeightSet()
    # weights.get("R.ASIS").setWeight(10.0)

    # Run the inverse kinematics tool
    ik_tool.run()


Use Resulting State Trajectory
------------------------------

The output of an inverse kinematics run is a motion file (``.mot``) containing time-series coordinate values
(joint angles and translations). You can load this output back into OpenSim as a ``StatesTrajectory``
or ``TimeSeriesTable`` to extract kinematic outputs, compute velocities and accelerations, or visualize the motion.

.. code:: python

    import opensim

    # Load model and initialize
    model = opensim.Model("pragmatic_resources/gait2354/subject01.osim")
    model.initSystem()

    # Load the resulting IK motion into a states trajectory
    motion_file = "subject01_walk1_ik.mot"
    states_table = opensim.TimeSeriesTable(motion_file)

    if opensim.TableUtilities.isInDegrees(states_table):
        model.getSimbodyEngine().convertDegreesToRadians(states_table)

    states = opensim.StatesTrajectory.createFromStatesTable(
        model,
        states_table,
        allowMissingColumns=True,
        allowExtraColumns=True
    ).getStateArray()

    # Iterate and extract coordinate values
    for state in states:
        model.realizePosition(state)
        # e.g., extract knee angle value
        knee_coord = opensim.Coordinate.safeDownCast(model.getComponent("/jointset/knee_r/knee_angle_r"))
        print(f"Time: {state.getTime():.3f}s | Right Knee Angle: {knee_coord.getValue(state):.3f} rad")


Common Next Steps
-----------------

**Beware**: Inverse kinematics only solves for kinematics (positions and orientations). It does not solve
for forces, net joint moments, or muscle activations, because it ignores external ground reaction forces
and mass distribution properties.

Once kinematics are established, common next steps include:

* **Inverse Dynamics (ID)**: Combines kinematics, model mass properties, and experimental ground reaction forces
  (from force plates) to compute net internal joint moments.
* **Computed Muscle Control (CMC)** or **Static Optimization**: Solves muscle redundancy to estimate individual
  muscle forces and activations required to produce the movement.


FAQ
---

Why is the IK solver failing or reporting large marker errors?
    The most common pitfalls include:

    1. **Locked Coordinates**: If coordinates required to satisfy marker motion are accidentally locked in the model
       (e.g., knee flexion locked or joint degrees of freedom restricted), the solver cannot minimize marker errors.
       Ensure all relevant coordinates are unlocked.
    2. **Unit Mismatch**: If your marker errors are excessively large (e.g., hundreds of meters), your ``.trc`` file
       is likely recorded in millimeters while OpenSim expects meters.
    3. **Mismatched Marker Names or Zero Weights**: Check that your marker names in the ``.trc`` file match the model's
       ``MarkerSet`` and that active markers have positive weights assigned.
