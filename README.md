<h1 align="center">
    <a href="https://pragmatic.opynsim.eu">
        <img src="source/_static/banner_horizontal.svg" alt="Banner" />
    </a>
</h1>

This is the source code behind the [Pragmatic Musculoskeletal Modelling](https://pragmatic.opynsim.eu)
ebook, which guides readers through the practical steps of setting up and using
open-source software for musculoskeletal modelling.


## Building the Handbook from Source

This is a Sphinx documentation project that also installs the simulation
libraries (e.g. `opynsim` and `opensim`) for testing and image-generation
purposes. Here is how you can build it with `uv`:

```bash
#!/usr/bin/env bash

uv venv --python 3.12
uv pip install -r requirements.txt
source .venv/bin/activate
uv run sphinx-build source/ build/
```

## License

This work is licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International</a>

## ❤️ Acknowledgements

We would like to thank [Open Science NL (NWO)](https://www.openscience.nl/), which
currently funds OPynSim's development through its "Open Science Infrastructure"
grant call ([grant](https://doi.org/10.61686/KYYRQ22856), [announcement](https://www.openscience.nl/en/news/45-projects-strengthen-dutch-open-science-infrastructure)). You can read OPynSim's
proposal on [Zenodo](https://doi.org/10.5281/zenodo.19493285).

We would also like to thank the [Department of Biomechanical Engineering at TU Delft](https://www.tudelft.nl/3me/over/afdelingen/biomechanical-engineering),
which provides the institutional support necessary to keep OPynSim's
development administered, supported, and stable.

<table align="center">
  <tr>
    <td colspan="2" align="center">Project Sponsors</td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://www.tudelft.nl/3me/over/afdelingen/biomechanical-engineering">
        <img src="source/_static/tudelft_logo.svg" alt="TUD logo" height="128" />
        <br />
        Biomechanical Engineering at TU Delft
      </a>
    </td>
    <td align="center">
      <a href="https://www.openscience.nl/en">
        <img src="source/_static/osnl_logo.svg" alt="Open Science NL logo" width="250" height="128" />
        <br />
        Open Science NL
      </a>
    </td>
  </tr>
</table>

