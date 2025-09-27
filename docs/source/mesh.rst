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

`ImageMesh` creates a **low-poly mesh** directly from a 2D image.  
It partitions the image into sectors, maps pixel intensity to depth, and wraps each sector with a convex hull.

.. code-block:: python

   import voxelmap as vxm

   model = vxm.Model(file="docs/img/land.png")   # load image
   model.ImageMesh(out_file="land.obj", L_sectors=15)
   model.MeshView()  # interactive view

➡ Produces `land.obj` and opens a 3D PyVista window.

---

MarchingMesh
------------

`MarchingMesh` converts voxel arrays into detailed triangle meshes using the Marching Cubes algorithm.

.. code-block:: python

   import numpy as np
   from voxelmap import Model

   arr = np.random.randint(0, 2, (20, 20, 20))  # random voxel array
   model = Model(arr)

   model.MarchingMesh("random.obj")
   model.MeshView("random.obj")

➡ Produces `random.obj` and displays it.

---

MeshView
--------

`MeshView` is a lightweight wrapper around PyVista for visualizing `.obj` meshes.  
It can be used after `ImageMesh` or `MarchingMesh`.

.. code-block:: python

   model.MeshView("random.obj", wireframe=True, color="white")

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


