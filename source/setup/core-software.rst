Core Software
=============


This section guides the setup of the core software used throughout this handbook.

All code examples are written with `Python <https://www.python.org/>`_ and use the
following libraries extensively:

- `Matplotlib <https://matplotlib.org/>`_: For plotting and visualization
- `NumPy <https://numpy.org/>`_: For numerical computing (vectors, matrices)
- `Pandas <https://pandas.pydata.org/>`_: For tabular data manipulation (dataframes).
- `OpenSim <https://opensim.stanford.edu/>`_ + `OPynSim <http://opynsim.eu>`_: For musculoskeletal modelling.

This combination ensures good interoperability with the broader scientific
Python ecosystem. OpenSim is chosen because it has been used in musculoskeletal
modelling for 15+ years. OPynSim, developed by this handbook's maintainers,
streamlines data import, output extraction, and visualization.


Overview
--------

Setting up a musculoskeletal modelling environment involves four standard steps:

1. **Install Python**: Download and install a supported Python version
   (v3.12+).
2. **Create a Virtual Environment**: Setup a project directory with its
   own Python virtual environment.
3. **Install Libraries**: Install necessary libraries (dependencies) into
   the virtual environment.
4. **Develop/Run Python Scripts**: Use an IDE to open/edit/run Python
   scripts in the project directory.

**For a specific guide**, this page contains Python and library installation
walkthroughs based on these common combinations of technologies:

- :ref:`Windows + Python.org + Pip <win-pip>`
- :ref:`macOS + Python (Python.org) + Pip <mac-pip>`
- :ref:`Ubuntu + Python (apt) + Pip <ubuntu-pip>`

.. admonition:: What is a Virtual Environment? Why use one?

   A virtual environment is an isolated directory that contains a specific
   Python installation and its libraries. Using virtual environments prevents
   library conflicts between projects and avoids modifying your system-wide
   Python installation.

   Setup guides here call virtual environments ``.venv`` because it's standard
   practice and tools like :doc:`pycharm` and :doc:`vscode` automatically detect
   it.

.. _win-pip:

Windows Setup (Python.org, pip)
-------------------------------

1. **Install Python**: Download the latest Python installer (v3.12+)
   from `python.org <https://www.python.org/downloads/>`_. Run the installer and
   make sure to check **"Add python.exe to PATH"** before clicking Install.

.. note::

   OpenSim requires the Visual C++ Redistributable. If ``import opensim``
   later fails with a DLL error, download and run `vc_redist.x64.exe
   <https://aka.ms/vc14/vc_redist.x64.exe>`_ from Microsoft.

2. **Open PowerShell**: Open the project directory in Windows explorer and
   use your mouse to directly open a PowerShell window in it:
   ``Shift+RightClick > Open in Terminal (or Open PowerShell Window Here)``.

   Alternatively, you can manually open PowerShell from the start menu and
   then navigate to your project directory by running (e.g.) ``cd C:\Users\adam\Desktop\my-project``.

3. **Create Virtual Environment**: Create a virtual environment called
   ``.venv`` in the current (project) directory by running:

   .. code:: powershell

       python -m venv .venv

4. **Activate Virtual Environment**: Activate the virtual environment by running:

   .. code:: powershell

      .\.venv\Scripts\activate

   Virtual environment "activation" makes subsequent ``pip``/``python`` commands
   use the virtual environment, rather than the system-wide versions. It's
   temporary and only applies until the PowerShell window is closed.

   .. note::

      If script execution is disabled, you may need to run this:

      .. code:: powershell

         Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

5. **Install Libraries**: Use ``pip`` to install core libraries into the virtual
   environment:

   .. code:: powershell

       pip install matplotlib numpy pandas opensim opynsim

6. **Validate Installation (optional)**: Run ``python`` to open a Python shell:

   .. code:: powershell

      python

   Run these commands in the Python shell to ensure the core software works
   in the environment:

   .. code:: python

      import opensim     # try `import`ing `opensim`
      import opynsim     # try `import`ing `opynsim`
      import opynsim.ui  # try `import`ing `opynsim.ui`

      # should show a spinning torus, you must manually close the window
      opynsim.ui.show_hello_ui()

      quit()  # close the Python shell


Once installed and validated, your Python environment is then capable of running
scripts that use the core libraries from a terminal (e.g. by running
``python some_opensim_script.py``). This is useful for batch processing,
but is rather impractical for day-to-day development. Therefore, the next step
is to set up an IDE that uses the environment. See :doc:`pycharm` and
:doc:`vscode` for more information on that.

.. _mac-pip:

macOS Setup (Python.org, pip)
-----------------------------

1. **Install Python**: You can manually download and install Python
   from `Python.org <https://www.python.org>`_.

   .. note::

      After installation completes, open your ``Applications/Python 3.xx`` folder
      and double-click **"Install Certificates.command"**. This is required for
      ``pip`` to download packages over SSL without errors.

2. **Open Terminal in Project Directory**: All subsequent steps use a terminal. Open it
   with ``Cmd+Space -> Terminal -> Enter`` and navigate to your project directory by
   running ``cd your/project/directory``.

3. **Create Virtual Environment**: In the terminal window, create a
   virtual environment called ``.venv`` in the current (project) directory:

   .. code:: bash

       python3 -m venv .venv

4. **Activate Virtual Environment**: Activate the virtual environment in the
   terminal. This is temporary (it only applies to this instance of
   the terminal) and makes subsequent ``pip``/``python`` commands use
   the virtual environment:

   .. code:: bash

      source .venv/bin/activate

5. **Install Libraries**: Use ``pip`` to install this handbook's libraries
   into the virtual environment:

   .. code:: bash

       pip install matplotlib numpy pandas opensim opynsim

6. **Validate Installation (optional)**: Run ``python`` to open a Python shell in
   the terminal:

   .. code:: bash

      python

   And then run these commands to ensure the core software works in the environment:

   .. code:: python

      import opensim     # try `import`ing `opensim`
      import opynsim     # try `import`ing `opynsim`
      import opynsim.ui  # try `import`ing `opynsim.ui`

      # should show a spinning torus, you must manually close the window
      opynsim.ui.show_hello_ui()

      quit()  # close the Python shell

Once installed and validated, your Python environment is then capable of running
scripts that use the core libraries from a terminal (e.g. with
``python some_processing_script.py``). This is useful for batch processing,
but is rather impractical for day-to-day development. Therefore, the next step
is to set up an IDE that uses the environment. See :doc:`pycharm` and
:doc:`vscode` for more information on that.


.. _ubuntu-pip:

Ubuntu Setup (system Python, pip)
---------------------------------

1. **Install System Dependencies**: Open a terminal (``Ctrl+Alt+T``) and run
   the following command to install ``python3``, ``pip``, and the virtual
   environment module via ``apt``:

   .. code:: bash

       sudo apt update
       sudo apt install -y python3 python3-venv python3-pip

2. **Open Terminal in Project Directory**: All subsequent steps use the terminal.
   Navigate to your project directory by running:

   .. code:: bash

       cd path/to/your/project

3. **Create Virtual Environment**: In the terminal window, create a
   virtual environment called ``.venv`` in the current (project) directory:

   .. code:: bash

       python3 -m venv .venv

4. **Activate Virtual Environment**: Activate the virtual environment in the
   terminal. This is temporary (it only applies to this instance of
   the terminal) and makes subsequent ``pip``/``python`` commands use
   the virtual environment:

   .. code:: bash

       source .venv/bin/activate

5. **Install Libraries**: Use ``pip`` to install this handbook's libraries
   into the virtual environment:

   .. code:: bash

       pip install matplotlib numpy pandas opensim opynsim

6. **Validate Installation (optional)**: Run ``python`` to open a Python shell in
   the terminal:

   .. code:: bash

       python

   And then run these commands to ensure the core software works in the environment:

   .. code:: python

      import opensim     # try `import`ing `opensim`
      import opynsim     # try `import`ing `opynsim`
      import opynsim.ui  # try `import`ing `opynsim.ui`

      # should show a spinning torus, you must manually close the window
      opynsim.ui.show_hello_ui()

      quit()  # close the Python shell


Once installed and validated, your Python environment is then capable of running
scripts that use the core libraries from a terminal (e.g. with
``python some_processing_script.py``). This is useful for batch processing,
but is rather impractical for day-to-day development. Therefore, the next step
is to set up an IDE that uses the environment. See :doc:`pycharm` and
:doc:`vscode` for more information on that.
