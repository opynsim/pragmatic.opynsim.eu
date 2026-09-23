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

The ``opynsim.graphics`` module has ``render_model_in_state``, a function
that renders a model+state 3D scene to a ``Texture2D``, which has methods
for extracting raw pixel data. Below are some usage examples.

.. admonition:: How about video rendering?

   These examples only produce one image, but videos are just
   sequences of images - plus some nuance around frame rates
   and encoding. See :doc:`render-model-states-to-video` for
   more details.

Composite Texture Into Plots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have rendered the scene to a texture, you can then composite the
texture's pixels into a ``matplotlib`` plot using a variety of techniques.

Here is an example that uses matplotlib's ``imshow``. This  can be useful for quickly
putting annotations over plots (e.g. top-left corner), because it uses
ui-space coordinates (percentage of plot bounds):

.. code:: python

    # Example: render a `model` + `state` to `texture` and then composite
    # its pixels over a `matplotlib` plot at some percentage in ui-space.

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

Here is another example of using an ``OffsetImage`` and ``AnnotationBbox``. This
is useful for annotating a plot in data-space. E.g. if you know a peak/nadir is
somewhere in data-space and you would like a picture of the model at that
location.

.. code::

    # Example: render a `model` + `state` to `texture` and then create
    # an annotation with its pixels at some location in data-space.

    import matplotlib.pyplot as plt
    from matplotlib.offsetbox import AnnotationBbox, OffsetImage
    import numpy as np
    import opynsim as opyn
    import opynsim.graphics

    model = opyn.read_osim("pragmatic_resources/gait2354/subject01.osim").compile()
    state = model.initial_state(realized_to=opyn.STAGE_REPORT)
    texture = opyn.graphics.render_model_in_state(model, state)

    x = np.linspace(0, 2.0 * np.pi, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), label="sin(x)")
    ax.add_artist(AnnotationBbox(
        OffsetImage(texture.pixels_rgba32(), zoom=0.25),
        (np.pi/ 2, 1.0),  # (x, y) in data space - here, first peak of sin(x)
        xybox=(30, -30),  # Offset from the above
        frameon=False,    # Remove white background
        xycoords="data",
        boxcoords="offset points",
        pad=0.2,
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2"),
    ))
    ax.set_ylim(-1.5, 1.5)
    plt.show()


Write Textures to Image Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have rendered the scene to a texture, you can then pump its pixels
into a third-party imaging library. Here is an example that
uses `Pillow <https://pillow.readthedocs.io/en/stable/>`_ (install
with ``pip install pillow``) to write the texture as a PNG file:

.. code:: python

    import numpy as np
    import opynsim as opyn
    import opynsim.graphics
    from PIL import Image  # pip install pillow

    model = opyn.read_osim("pragmatic_resources/gait2354/subject01.osim").compile()
    state = model.initial_state(realized_to=opyn.STAGE_REPORT)
    texture = opyn.graphics.render_model_in_state(model, state)

    Image.fromarray(texture.pixels_rgba32(), mode="RGBA").save("model.png")

Alternatively, if you are already using the texture in a plot, you can use
the plot's ``savefig`` function to write an image file directly from the
plotter.


Customize Render (e.g. Camera, Dimensions)
------------------------------------------

``render_model_in_state`` also accepts ``camera`` and ``dimensions`` as
arguments, which let you adjust the model's framing in the 3D world and
the resulting texture's dimensions. Here is an example that uses both of
those options:

.. code:: python

    import matplotlib.pyplot as plt
    import numpy as np
    import opynsim as opyn
    import opynsim.graphics

    model = opyn.read_osim("pragmatic_resources/gait2354/subject01.osim").compile()
    state = model.initial_state(realized_to=opyn.STAGE_REPORT)
    camera = opyn.graphics.Camera()

    renders = []
    directions = [
        ([-1,  0,  0], [ 0, 1, 0], "along -x"),
        ([ 0, -1,  0], [-1, 0, 0], "along -y"),
        ([ 0,  0, -1], [ 0, 1, 0], "along -z"),
        ([-1, -1,  0], [ 0, 1, 0], "front diagonal"),
    ]
    dimensions = (480, 480)

    # Render each direction
    for direction, up, title in directions:
        camera.direction = np.array(direction)
        camera.up = np.array(up)
        camera.position = (-1.1 * camera.direction) + np.array([0, 1, 0])

        texture = opyn.graphics.render_model_in_state(
            model, state, camera=camera, dimensions=dimensions
        )
        renders.append((texture.pixels_rgba32(), title))

    fig, axes = plt.subplots(1, len(directions), figsize=(12, 4))
    for ax, (pixels, title) in zip(axes, renders):
        ax.imshow(pixels)
        ax.axis("off")
        ax.set_title(title, y=-0.15)  # Position title below image
    plt.tight_layout()
    plt.show()
