OPynSim Concepts
================

This page briefly outlines core concepts that are useful when working with
`OPynSim <http://opynsim.eu>`_. See :doc:`core-concepts` for a general
explanation of musculoskeletal modelling concepts.

Most of this content is work-in-progress and based on OPynSim's current alpha
build. We recommend reading through `OPynSim's quickstart guide <https://docs.opynsim.eu/manual/en/latest/getting-started/quickstart.html>`_
for a clearer overview of the OPynSim API.

Model Specification
-------------------

An OPynSim `ModelSpecification <https://docs.opynsim.eu/manual/en/latest/api/opynsim.html#opynsim.ModelSpecification>`_
represents an **editable data structure that describes what a model is** (e.g., bodies,
joints, muscle paths, mass properties). In contrast to OpenSim, it does not have a
physics system and instead requires scripts to explicitly call ``.compile()`` when
the specification is complete:

.. code:: python

   import opynsim as opyn

   model_specification = opyn.read_osim("some.osim")  # editable specification
   model = model_specification.compile()              # compiled physics model
   state = model.initial_state()                      # model state


Model (+ ModelState)
--------------------

An OPynSim `Model <https://docs.opynsim.eu/manual/en/latest/api/opynsim.html#opynsim.Model>`_ represents
a **compiled, immutable (read-only) physics system** ready for computation. It can
produce, read, and modify `ModelState <https://docs.opynsim.eu/manual/en/latest/api/opynsim.html#opynsim.ModelState>`_
instances. It also provides access to outputs, coordinates, and other state readers/modifiers:

.. code:: python

   import opynsim as opyn

   model = opyn.read_osim("some.osim").compile()
   state = model.initial_state(realized_to=opyn.STAGE_REPORT)

   # These only modify `state`.
   output_value = model.get_output_value(state, "some/model/output")
   model.set_coordinate_value(state, "some/joint/coordinate", 5.0)
   model.realize(state, opyn.STAGE_REPORT)
   new_output_value = model.get_output_value(state, "some/model/output")


DataFrame
---------

An OPynSim `DataFrame <https://docs.opynsim.eu/manual/en/latest/api/opynsim.html#opynsim.DataFrame>`_ represents
a table containing rows and columns. OPynSim's ``DataFrame`` class mostly exists because
the OPynSim API must accept/emit *something* that isn't dependent on a particular dataframe
library (e.g. Pandas, Polars, or Arrow - there's many).

The pragmatic thing to keep in mind is that OPynSim implements the Arrow API, which means it
supports conversion to/from those common ``DataFrame`` types. This means you can (e.g.) load
OpenSim-specific data via OPynSim, convert it to a pandas dataframe, perform any data manipulation
or scaling in pandas, and then convert it back into an OPynSim dataframe passing it into OPynSim:

.. code:: python

   import opynsim as opyn

   opynsim_df = opyn.read_trc("some.trc")  # opynsim.DataFrame

   # Convert FROM an `opynsim.DataFrame` (e.g. for data manipulation, plotting, csv writing)
   pandas_df = opynsim_df.to_pandas()
   polars_df = opynsim_df.to_polars()
   arrow_df = opynsim_df.to_arrow()

   # Convert TO an `opynsim.DataFrame` (e.g. for use with OPynSim)
   opyn.DataFrame(pandas_df)
   opyn.DataFrame(polars_df)
   opyn.DataFrame(arrow_df)
