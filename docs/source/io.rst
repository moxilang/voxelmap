I/O Helpers
===========

VoxelMap supports saving and loading models in lightweight formats.  
Install extras if you want I/O utilities:

.. code-block:: bash

   pip install voxelmap[io]

---

Saving and Loading JSON
-----------------------

The simplest way to persist a model is with JSON.

.. code-block:: python

   import numpy as np
   from voxelmap import Model

   arr = np.ones((3, 3, 3))
   model = Model(arr)
   model.set_color(1, "red")

   model.save("cube.json")   # saves array + palette
   loaded = Model()
   loaded.load("cube.json")

   loaded.draw_mpl("custom")

➡ This saves both the voxel array and its palette, so your colors are preserved.

---

Saving and Loading TXT
----------------------

VoxelMap can also export voxel arrays to a plain text format (`.txt`).  
This is useful for interoperability with voxel editors like Goxel.

.. code-block:: python

   model.save("cube.txt")   # export
   model2 = Model()
   model2.load("cube.txt")

---

OBJ Export (with Meshing)
-------------------------

VoxelMap does not directly save `.obj` from the core.  
Instead, use the **mesh** extras (`ImageMesh` or `MarchingMesh`) to create `.obj` files:

.. code-block:: python

   from voxelmap import Model
   import numpy as np

   arr = np.random.randint(0, 2, (10, 10, 10))
   model = Model(arr)

   model.MarchingMesh("random.obj")  # requires voxelmap[mesh]
   model.MeshView("random.obj")

---

When to use what?
-----------------

- **JSON** → best for full reproducibility (stores array + palette).  
- **TXT** → good for interchange with voxel editors.  
- **OBJ** → polygonal mesh, use when exporting to Blender / 3D tools.  


