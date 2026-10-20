Make a Basic Solver
===================

Once you have built a model (e.g. :doc:`make-a-pendulum`), you can then use it
to solve problems. In most cases, an off-the-shelf solver is used, e.g. as
described in :doc:`solve-forward-dynamics` and :doc:`solve-inverse-kinematics`. However,
sometimes you need to design your own solver, which is described here.


Setup Example Data
------------------

If you want to run the Python code in this guide, you must first set up the
:doc:`../setup/example-data`.


Introduction
------------

While an OpenSim model defines the rules of the physical world (e.g. how
joints connect, how segments are proportioned, how muscles wrap), the model
doesn't inherently know how to answer specific questions. This is where
solvers step in.

"Solver" is a general team for an algorithm that bridges the gap between what
you've measured (or specified) and what your model requires. Do
you have marker positions from motion tracking and want to pose your model to
match those markers as closely as possible? You could use
OpenSim's ``InverseKinematicSolver``. Got a muscle path and want to know its
moment arm with respect to a degree of freedom? ``MomentArmSolver``. A specific
problem that has no off-the-shelf solver? Write one!

In this guide, we're going to write a custom solver for a specific problem. However,
the main lesson isn't about the solver: it's about identifying problems where a
custom solver is necessary, and how to write one that uses an OpenSim model.


Problem Description
-------------------

**Suppose you want to design a cabled robotic finger**. To keep things simple,
you will start with a single finger segment (body) joined to ground with a ``PinJoint``
and cabled with some ``BlankevoortLigament``\s. Here's a schematic diagram:

TODO: a schematic/kinematic picture of the setup. One body at some horizontal
offset from a grounded/welded body, attached with a pin joint centered on the
ground connection - i.e. a sideways pendulum. The body should have redundancy:
e.g. the two ligaments that each pull in the same direction.

**To aid your work, you want to calculate the static equilibrium position (resting
position) of the finger segment.** This is dictated by a balance of torques:
gravitational forces acting on the segment's mass and center of mass, and
tensile forces exerted by the cables. Formally, you want to solve for the
pin joint angle :math:`\theta` where the net generalized force (torque) is zero.

.. note::

   This is an example of a *forward problem*: you have a model/parameters and want to
   predict an outcome. The next guide (:doc:`optimize-model-properties`) presents an
   *inverse problem*: there, you choose a desired outcome (rest position) and want to
   know which model/parameters would produce it.


Solution Ideas
~~~~~~~~~~~~~~

It's useful to think about how to solve this problem before going through
the actual implementation details. After all, this guide isn't about writing
a particular solver, it's about understanding/defining the problem and then
weighing up the options. Here are two solution ideas and their tradeoffs (**this guide
only implements the second**).

----

**The first idea is to use a forward-dynamics solver**. In this case, you
initially pose the model and then forward-integrate it with respect to
time, checking each timestep until you encounter one where the pin
joint's torque is close to zero (i.e. at-rest). The tradeoffs of this
solution are:

- ✅ It's easy to explain: "we forward-simulate the model until it's resting".
- ✅ It probably mimics how the resting position is determined in the lab.
- ✅ Off-the-shelf forward dynamics solvers are available (e.g.
  ``opensim.Manager``).
- ❌ It's *usually* computationally expensive. Performance can be important
  when a solver is called many times (e.g. :doc:`optimize-model-properties`).
- ❌ It's *always* path-dependent. Complicated models may have multiple,
  better, solutions that aren't visited during integration.
- ❌ It only solves problems that can be solved with forward integration.

If the computational cost is acceptable, and the solution doesn't appear to be
path-dependent, then a forward-dynamics-based solver can be a good, easy-to-explain,
choice.

----

**The second idea is to use an optimizer**. In this case, you provide the
optimizer with parameter(s) it can adjust and a function it must minimize
(e.g. ``calc_joint_torque(joint_angle)``). The tradeoffs of this solution
are:

- ❌ It's harder to explain: "we find the minimum joint torque by evaluating it with
  different joint angles, taking finite differences, perhaps using a little noise,
  the approach is optimizer-dependent, etc.".
- ❌ It probably doesn't mimic how the resting position is determined in the lab.
- ✅ Many off-the-shelf optimizers are available (e.g. `scipy.optimize <https://docs.scipy.org/doc/scipy/tutorial/optimize.html>`_,
  `CasADi <https://web.casadi.org/>`_, `JAXopt <https://jaxopt.github.io/stable/>`_). They can
  be interchanged to figure out which one works best for a particular problem.
- 🟡 It *may* be computationally cheap. Computational expense is dictated by the cost
  of a function evaluation and the shape of the function.
- ✅ It's *never* path-dependent. Optimizers assume function evaluations are independent.
  Optimizers   can be directed to explore the entire range of the input parameters, when necessary.
- ✅ It solves any problem that can be stated as "given these parameters, minimize the
  function".

Optimizers are an excellent choice when a problem can (be adjusted/restated to) fit them.

.. note::

   Interestingly, the other solution idea (forward dynamics) is an excellent counterexample: you
   can't use an optimizer to solve the forward dynamics of a model because each solution (timestep)
   depends on the previous one.

