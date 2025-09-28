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
   MeshView("land.obj", mode="flat", flat_color="white", alpha=0.8)

➡ Produces `land.obj` and opens a 3D PyVista window.

---

MarchingMesh
------------

`MarchingMesh` converts voxel arrays into detailed triangle meshes using the **Marching Cubes** algorithm.

.. code-block:: python

   import numpy as np
   from voxelmap import Model
   from voxelmap.mesh import MarchingMesh, MeshView

   arr = np.random.randint(0, 2, (20, 20, 20))  # random voxel array
   model = Model(arr)
   model.set_color(1, "blue")

   MarchingMesh(model.array, out_file="random.obj", palette=model.palette, pad=1)
   MeshView("random.obj", palette=model.palette, mode="solid")

➡ Produces `random.obj` with colors preserved and displays it interactively.

---

MeshView
--------

`MeshView` is a lightweight wrapper around **PyVista** for visualizing `.obj` meshes.  
It can be used after `ImageMesh` or `MarchingMesh`.

.. code-block:: python

   from voxelmap.mesh import MeshView

   # Wireframe only
   MeshView("random.obj", mode="wireframe", wireframe_color="green", background_color="black")

   # Solid + edges
   MeshView("random.obj", palette={1: "red"}, mode="both", wireframe_color="magenta")

Options:
- ``mode="solid"`` → surfaces colored by palette  
- ``mode="wireframe"`` → only edges  
- ``mode="both"`` → fill + edges  
- ``mode="flat"`` → single solid color (ignores palette)  
- ``palette={id: "color"}`` → map voxel labels to colors  
- ``background_color="black"`` → set viewer background  
- ``wireframe_color="green"`` → change edge color  
- ``alpha=0.8`` → transparency  

---

When to use which?
------------------

- **ImageMesh** → fast, low-poly meshes from 2D images (landscapes, silhouettes).  
- **MarchingMesh** → high-resolution meshes from 3D voxel data.  
- **MeshView** → universal visualization of `.obj` meshes with multiple viewing modes.
