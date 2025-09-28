Core Usage
==========


This page covers the **basics of VoxelMap v5.0.0**.

Voxel Arrays
------------

VoxelMap models are built from NumPy arrays.  
- `0` = empty space  
- non-zero integers = voxel types  

.. code-block:: python

   import numpy as np
   from voxelmap import Model

   arr = np.ones((3, 3, 3))   # simple cube
   model = Model(arr)

Drawing Voxels
--------------

The core drawing backend is **Matplotlib**.  
Use `draw_mpl` for quick static 3D voxel plots:

.. code-block:: python

   model.set_color(1, "red")
   model.draw_mpl("custom")

➡ Produces a solid red cube.

Custom Palettes
---------------

You can assign multiple voxel types different colors using `palette`:

.. code-block:: python

   arr = np.indices((3, 3, 3)).sum(axis=0) % 2 + 1
   model = Model(arr)
   model.palette = {1: "black", 2: "white"}
   model.draw_mpl("custom")

➡ Produces a black/white checkerboard cube.

Colormap Gradients
------------------

Models can be shaded with continuous colormaps (from Matplotlib):

.. code-block:: python

   from matplotlib import cm
   arr = np.ones((10, 3, 3))   # tall column
   model = Model(arr)

   model.colormap = cm.viridis
   model.alphacm = 0.8
   model.draw_mpl(coloring="linear")

➡ Produces a vertical viridis gradient.

Interactive 3D (Optional)
-------------------------

If you installed with `[mesh]`, you can use the **PyVista** backend for interactive zoom/rotate/pan:

.. code-block:: python

   model.draw("custom")

➡ Opens an interactive 3D window.

Saving and Loading
------------------

Save your model (array + palette) to JSON:

.. code-block:: python

   model.save("cube.json")

Reload it later:

.. code-block:: python

   blank = Model()
   blank.load("cube.json")
   blank.draw_mpl("custom")

➡ Reproducible and color-safe.

Summary
-------

- Use **NumPy arrays** as the backbone.  
- Assign colors via **palette** or **set_color**.  
- Visualize with **draw_mpl** (static) or **draw** (interactive).  
- Save/load with **JSON** for reproducibility.  
- Extend with `[mesh]` for advanced meshing and OBJ export.  


