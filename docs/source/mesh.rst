Mesh Functions
==============

VoxelMap provides optional **mesh reconstruction** utilities.  
Install with:

.. code-block:: bash

   pip install voxelmap[mesh]

These tools use `scipy`, `scikit-image`, and `pyvista` for meshing and interactive viewing.

---

ImageMesh
---------

`ImageMesh` converts 2D image arrays into convex-hull meshes.

.. code-block:: python

   import cv2
   from voxelmap.mesh import ImageMesh, MeshView

   img = cv2.imread("land.png", 0)  # grayscale
   ImageMesh(img, out_file="land.obj", L_sectors=15)
   MeshView("land.obj", color="white", alpha=0.8)

➡ Produces `land.obj` and opens a 3D PyVista window.

---

MarchingMesh
------------

`MarchingMesh` converts voxel arrays into detailed triangle meshes using the Marching Cubes algorithm.

.. code-block:: python

   import numpy as np
   from voxelmap import Model
   from voxelmap.mesh import MarchingMesh, MeshView  # 👈 import from voxelmap.mesh

   arr = np.random.randint(0, 2, (20, 20, 20))  # random voxel array
   model = Model(arr)

   MarchingMesh(model.array, "random.obj")
   MeshView("random.obj")

➡ Produces `random.obj` and displays it.

---

MeshView
--------

`MeshView` is a lightweight wrapper around PyVista for visualizing `.obj` meshes.  
It can be used after `ImageMesh` or `MarchingMesh`.

.. code-block:: python

   from voxelmap.mesh import MeshView

   MeshView("random.obj", wireframe=True, color="white")

Options:
- `wireframe=True` → show mesh edges  
- `color="red"` → set solid fill color  
- `alpha=0.8` → transparency  
- `viewport=(800, 800)` → window size

---

When to use which?
------------------

- **ImageMesh** → fast, low-poly meshes from 2D images (good for landscapes, textures).  
- **MarchingMesh** → high-resolution meshes from 3D voxel data.  
- **MeshView** → universal visualization of `.obj` meshes.


