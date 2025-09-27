.. _installation:

Installation
============

Supported Python
----------------
``voxelmap`` supports **Python 3.8+** (tested on 3.8–3.12).

Quick install (core only)
-------------------------
The core library only requires **NumPy** and **Matplotlib**.

.. code-block:: bash

   pip install voxelmap

Optional extras
---------------
Install extras depending on what you need:

- **I/O helpers** (JSON/TXT utilities): ::

    pip install "voxelmap[io]"

- **Meshing & interactive 3D** (scipy, scikit-image, PyVista): ::

    pip install "voxelmap[mesh]"

- **Everything**: ::

    pip install "voxelmap[all]"

Virtual environment (recommended)
---------------------------------
Create and activate a virtual environment:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install "voxelmap[all]"

Deactivate anytime with ``deactivate``.

Developer install (editable)
----------------------------
If you’re working on the package locally:

.. code-block:: bash

   git clone https://github.com/andrewrgarcia/voxelmap.git
   cd voxelmap
   python -m venv venv
   source venv/bin/activate
   pip install -e ".[all]"         # or .[mesh], .[io], or just .

Upgrading / Uninstalling
------------------------
.. code-block:: bash

   pip install -U voxelmap
   pip uninstall voxelmap

Verify your install
-------------------
Run a quick smoke test:

.. code-block:: bash

   python - <<'PY'
   import numpy as np
   from voxelmap import Model
   a = np.ones((3,3,3))
   m = Model(a)
   m.set_color(1, "red")
   # Should render a red 3x3x3 cube in a Matplotlib window:
   m.draw_mpl(coloring="custom")
   print("voxelmap OK")
   PY

Notes for interactive 3D (PyVista)
----------------------------------
- Install the **mesh** extra: ``pip install "voxelmap[mesh]"``.
- On headless servers/CI, prefer Matplotlib renders or configure an offscreen VTK backend.
- Some Linux desktops may require system OpenGL/VTK packages for full PyVista interactivity.

Building the documentation (optional)
-------------------------------------
If you want to preview the docs locally:

.. code-block:: bash

   pip install sphinx sphinx-rtd-theme
   # (optional live reload) pip install sphinx-autobuild
   make -C docs html
   # open docs/build/html/index.html in your browser

   # Live preview:
   sphinx-autobuild docs/source docs/build/html  # visit http://127.0.0.1:8000

Troubleshooting
---------------
- **Matplotlib window doesn’t zoom/rotate**: basic 3D axes support is limited; install the ``mesh`` extra and use PyVista for fully interactive 3D viewers.
- **ImportError for optional deps**: install the appropriate extra (``[io]``, ``[mesh]``, or ``[all]``).
- **Editable install discovers extra folders**: ensure only package dirs are included (e.g., use a ``src/`` layout or restrict package discovery in ``pyproject.toml``).
