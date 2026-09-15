Visual Studio Code
==================

If you use `Visual Studio Code <https://code.visualstudio.com/>`_, you can connect your existing
workspace directory and virtual environment in a few quick steps.

1. **Install the Python Extension**: Open VS Code, go to the Extensions view (``Ctrl+Shift+X`` on
   Windows/Linux, ``Cmd+Shift+X`` on macOS), and install the official **Python** extension
   published by Microsoft.

2. **Open the Project Folder**: Select **File > Open Folder...** and select the project
   directory where you created your ``.venv`` (or Conda environment) in :doc:`core-software`.

3. **Select the Python Interpreter**: You can see which Python interpreter VS Code is
   currently using in the bottom-right of the main window. VS Code usually detects and
   selects an existing ``.venv`` folder automatically. To explicitly set or change the
   active environment:

   - Open the Command Palette using ``Ctrl+Shift+P`` (Windows/Linux) or ``Cmd+Shift+P`` (macOS).
   - Type and select **Python: Select Interpreter**.
   - Select your existing environment from the list:

     - **For venv**: Look for the recommended entry pointing to ``./.venv/Scripts/python.exe`` (Windows)
       or ``./.venv/bin/python`` (macOS/Linux). If it doesn't appear, select **Enter interpreter path...**
       and browse directly to the Python executable within ``.venv``.
     - **For Conda**: Select your named Conda environment (e.g., ``opensim-env``).

   .. note::

      Once selected, opening a new terminal in VS Code (``Ctrl+``) will automatically
      activate your virtual environment.

4. **Verify OpenSim Import**:
   Create a test script (e.g., ``test_env.py``) or open the Interactive Window, then run:

   .. code:: python

       import opensim
       import opynsim

       print(opensim.__file__)

For further setup details, refer to the official VS Code documentation:

- `Getting Started with Python in VS Code <https://code.visualstudio.com/docs/python/python-tutorial>`_
- `Python Environments in VS Code <https://code.visualstudio.com/docs/python/environments>`_
