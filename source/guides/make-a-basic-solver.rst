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


Problem Description
-------------------

TODO: describe a simple problem that can be solved with a custom solver. One idea
would be to figure out the resting position of ``bouncing_block.osim``, because it
isn't *so* simple that there's an obvious closed-form solution (there's a pivot, a
constraint, etc.), but it isn't so complicated that the guide becomes muddied with
extra details (muscle equilibrium, etc.). Only focus on the forward
solver ("what is the resting position of the head?"), don't focus on the
inverse problem ("what spring stiffness would produce a resting position Y?) because
the next guide (:doc:`optimize-model-properties`) is going to do that.


Introduction
------------

At its core, a solver is just a specialized algorithm that bridges the gap
between what you've measured (or specified) and what your model requires. While
an OpenSim model defines the rules of the physical world (e.g. how
joints connect, how segments are proportioned, how muscles wrap), the model
doesn't inherently know how to answer specific questions backwards or
forwards in time.