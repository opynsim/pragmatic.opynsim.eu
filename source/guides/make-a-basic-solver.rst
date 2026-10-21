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

"Solver" in musculoskeletal modelling communities usually refers to an
algorithm that bridges the gap between what you've measured (or specified)
and what your model requires. Do you have marker positions from motion
tracking and want to pose your model to match those markers as closely
as possible? You could use OpenSim's ``InverseKinematicSolver``. Got a
muscle path and want to know its moment arm with respect to a degree
of freedom? ``MomentArmSolver``. Perhaps your problem has no
off-the-shelf solver? Write one!

In this guide, we're going to write a custom solver for a specific
problem. **However**, this guide isn't just about implementing a
solver: it's about the *process* of identifying problems where a solver
is necessary, thinking through possible designs, and then implementing
one. Always remember:

    "A couple of months in the laboratory [writing code] can frequently save a couple of hours in the library."
    - `Frank Westheimer <https://en.wikipedia.org/wiki/Frank_Westheimer>`_ (`Wikiquote <https://en.wikiquote.org/wiki/Frank_Westheimer>`_)


Identify Problem
----------------

**Suppose you're designing a cabled robotic finger**. To keep your initial
design steps very simple, you have modelled a single finger segment (body)
joined to ground with a ``PinJoint`` and cabled with some ``BlankevoortLigament``\s.
Here's a schematic diagram:

TODO: a schematic/kinematic picture of the setup. One body at some horizontal
offset from a grounded/welded body, attached with a pin joint centered on the
ground connection - i.e. a sideways pendulum. The body should have redundancy:
e.g. the two ligaments that each pull in the same direction.

**To aid your design work, you would like to know resting position (static
equilibrium position) of the finger segment when no other forces are applied to it.**
At a high-level, you identify that it's dictated by a balance of torques in the
model: gravitational forces are acting on the segment's mass, tensile forces are
exerted by the cables. At a lower-level, you formalize the problem (a major part
of the process!): you need an algorithm that calculates (solves for) the pin joint
angle (:math:`\theta`) where the net generalized torque on the pin joint is zero.
Sadly, there isn't an off-the-shelf ``FindJointAnglesWhereTorquesAreZeroSolver``, so
you will need to write your own.

.. note::

   Mathematically, this is an example of a **forward problem**: you have parameters
   and want to predict an observation. :doc:`optimize-model-properties` presents an
   `inverse problem <https://en.wikipedia.org/wiki/Inverse_problem>`_: there, you have
   a (desired) observation and want to know which parameters would produce it.


Solution Ideas
--------------

This section is an illustrative example of the thought process behind designing
a solver. It's generally a good idea to go though a process like this before writing
(or generating 😉) any code. Below are two ideas.

----

**The first idea is to use a forward-dynamics solver**. In this case,
the solver would initially pose the model and then forward-integrate
it with respect to time, checking each timestep until it encounters one
where the pin joint's torque is close to zero (i.e. at-rest). The
tradeoffs of this solution are:

- ✅ It's easy to explain: "It forward-simulates the model until it's resting".
- ✅ It probably mimics how the resting position would be determined in a lab.
- ✅ Off-the-shelf forward dynamics solvers are available (e.g.
  ``opensim.Manager``).
- ❌ It's *usually* computationally expensive.
- ❌ It's *always* path-dependent. The model may have multiple, better, solutions
  that aren't visited.
- ❌ It only solves problems that can be solved with forward integration.

**The second idea is to use an optimizer**. In this case, the solver provides
an off-the-shelf optimizer with parameter(s) it can adjust and a function it
must minimize (e.g. ``calc_joint_torque(joint_angle)``). The tradeoffs of
this solution are:

- ❌ It's harder to explain: "It finds the minimum joint torque using [a rather complicated] optimizer".
- ❌ It probably doesn't mimic how the resting position would be determined in a lab.
- ✅ *Many* off-the-shelf optimizers are available (e.g. `scipy.optimize <https://docs.scipy.org/doc/scipy/tutorial/optimize.html>`_,
  `CasADi <https://web.casadi.org/>`_, `JAXopt <https://jaxopt.github.io/stable/>`_).
- ✅ It *may* be computationally cheap. It depends on the function's cost and shape.
- ✅ It's *never* path-dependent. Optimizers can explore many inputs, evaluations are independent.
- ✅ It solves any problem that can be formulated as "given these parameters, minimize this function".

----

Because optimizers are a very useful tool to be aware of, **this guide implements the second idea**. It
closely matches our problem definition ("Which joint angle (parameter) evaluates to a joint
torque of zero?").


Create Model
------------

TODO


Write Optimizable Function
--------------------------

TODO


Finish Solver
-------------

TODO
