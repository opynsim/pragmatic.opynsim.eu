Pragmatic Musculoskeletal Modelling
===================================

This handbook sets you up with an open-source software environment and
describes using it to do interesting things with musculoskeletal models.

The OPynSim team maintains this handbook's content `here <https://github.com/opynsim/pragmatic.opynsim.eu>`_
(contributions welcome). In contrast to `OPynSim's documentation <https://docs.opynsim.eu>`_,
this focuses on getting things done using any combination of open-source
projects from the wider ecosystem.
Therefore, while some tasks may indeed use `OPynSim <http://opynsim.eu>`_,
others may use `NumPy <https://numpy.org/>`_,
`OpenSim <https://opensim.stanford.edu/>`_,
`OpenSim Creator <https://opensimcreator.com/>`_, etc. when that's currently
the most pragmatic solution.


Handbook Structure
------------------

This handbook is structured into three sections:

- **Setup**: Installing/configuring a computer for musculoskeletal modelling.
- **Concepts**: General concepts/techniques that apply to many musculoskeletal modelling problems/tasks.
- **Guides**: Guides that focus on solving a specific problem/task.

**Are you new to Python scripting and/or musculoskeletal modelling?** We
recommend that you first set up :doc:`setup/core-software` and
configure an IDE such as :doc:`setup/pycharm` or :doc:`setup/vscode`
to use it. After that, read through :doc:`concepts/core-concepts` before
tackling a specific guide. This way, you will encounter fewer technical
issues and have a rough idea of what's going on.

.. toctree::
   :maxdepth: 2
   :caption: Setup
   :hidden:

   setup/core-software
   setup/pycharm
   setup/vscode
   setup/example-data

.. toctree::
   :maxdepth: 2
   :caption: Concepts
   :hidden:

   concepts/core-concepts
   concepts/opensim-concepts
   concepts/opynsim-concepts

.. toctree::
   :maxdepth: 2
   :caption: Guides
   :hidden:

   guides/load-model-state-plot-stuff
   guides/load-data-into-dataframes
   guides/render-model-state-to-image
   guides/render-model-states-to-video
   guides/make-a-pendulum
   guides/solve-forward-dynamics
   guides/solve-equilibrium-position
   guides/optimize-attachment-positions

.. toctree::
   :caption: Other Links
   :hidden:

   OPynSim GitHub <https://github.com/opynsim/opynsim>
   OpenSim Creator <https://opensimcreator.com>
