PyCharm
=======

If you use `JetBrains PyCharm <https://www.jetbrains.com/pycharm/>`_, you can link your existing
project directory and virtual environment in a few steps.

1. **Open the Project Folder**: Launch PyCharm, select **Open**, and select the project
   directory where you created your ``.venv`` (or Conda environment) in :doc:`core-software`.

2. **Configure the Python Interpreter**: PyCharm usually auto-detects an existing ``.venv``
   folder and selects it automatically (visible in the bottom-right status bar
   as ``.venv [3.xx.yy]``). If it is not configured automatically:

   - Click the interpreter widget in the bottom-right corner of the window, or
     open **File > Settings** (Windows/Linux) / **PyCharm > Settings** (macOS).
   - Go to **Project: <your_project_name> > Python Interpreter**.
   - Click **Add Interpreter** and select **Add Local Interpreter...**.
   - Select **Existing**, then browse to the Python executable inside your ``.venv``:

     - **Windows:** ``.venv\Scripts\python.exe``
     - **macOS / Linux:** ``.venv/bin/python``
     - **For Conda**: Select **Conda Environment**, choose **Use existing environment**, and
       select your ``opensim-env`` from the drop-down menu.

3. **Verify OpenSim Import**: Open a new ``.py`` file or the built-in PyCharm Python
   Console (**View > Tool Windows > Python Console**) and run:

   .. code:: python

       import opensim
       import opynsim

       print(opensim.__file__)

For detailed documentation **including step-by-step UI references**, see the
official JetBrains documentation:

- `Configure a Python interpreter in PyCharm <https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html>`_
- `Connect to an existing virtual environment <https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#existing-environment>`_
