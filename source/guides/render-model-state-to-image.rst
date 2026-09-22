Render Model+State to Image
===========================

A picture can say a thousand words - especially when presenting
research results.

This guide walks through the process of using OPynSim's in-built
rendering engine to automatically produce images of models.


Setup Example Data
------------------

If you want to run the Python code in this guide, you must first set up the
:doc:`../setup/example-data`.


Load a Model + State
--------------------

The first step is use OPynSim to compile an ``opynsim.Model`` and
associated ``opynsim.ModelState``. There are a few ways to do this
(see `OPynSim's documentation <https://docs.opynsim.eu>`_), but here
are the two most common ones:

.. code:: python

    # Load an `.osim`, show it in its initial (default) state, as-if
    # opening it in an editor like OpenSim Creator or OpenSim.

    import opynsim as opyn

    model_specification = opyn.read_osim("pragmatic_resources/gait2354/subject01.osim")
    model = model_specification.compile()
    state = model.initial_state(realized_to=opyn.STAGE_REPORT)

.. code:: python

    # Load an `.osim`, load an associated `.mot`, pluck a state out of
    # the `ModelStates` loaded from the motion.

    import opynsim as opyn

    model = opyn.read_osim("pragmatic_resources/gait2354/subject01.osim").compile()
    df = opyn.read_mot("pragmatic_resources/gait2354/OutputReference/subject01_walk1_ik.mot")
    state = model.states_from_data_frame(df, realized_to=opyn.STAGE_REPORT)[0]

Of course, you can get fancy - if you like. The only thing rendering
cares about is that you have an ``opynsim.Model`` and an ``opynsim.ModelState``:

.. code:: python

    # Load an `.osim`, solve its forward dynamics by integrating
    # forward in time 0.1s and use that state.

    import opynsim as opyn
    from opynsim.solvers import ForwardDynamicsSolver

    model = opyn.read_osim("pragmatic_resources/gait2354/subject01.osim").compile()
    solver = ForwardDynamicsSolver(model, model.initial_state())
    state = solver.integrate_to(0.1)


Render Model + State to a Texture2D
-----------------------------------

The ``opynsim.graphics`` module provides the ``render_model_in_state``
API, which returns a ``Texture2D``. This enables transferring raw pixel data
into other libraries (e.g. `Pillow <https://pypi.org/project/pillow/>`_), so
you can (e.g.) composite the pixels into things like plots:

.. code:: python

    # Example: render a `model` + `state` to `texture` and then
    # composite its pixels over a `matplotlib` plot.

    import matplotlib.pyplot as plt
    import numpy as np
    import opynsim as opyn
    import opynsim.graphics

    model = opyn.read_osim("pragmatic_resources/gait2354/subject01.osim").compile()
    state = model.initial_state(realized_to=opyn.STAGE_REPORT)
    texture = opyn.graphics.render_model_in_state(model, state)

    # Plot `sin(x)` and composite `texture` over it.
    x = np.linspace(0, 2 * np.pi, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x))
    ax_overlay = ax.inset_axes([0.52, 0.68, 0.3, 0.3])  # [x, y, w, h] %
    ax_overlay.imshow(texture.pixels_rgba32())
    ax_overlay.axis("off")

    plt.show()


Customize Render (e.g. Camera, Dimensions)
------------------------------------------

TODO: ``opynsim.graphics.Camera``, ``render_model_in_state(dimensions=)``.
