3D Reconstruction from Images
=============================

VoxelMap provides two ways to go from **2D image → 3D model**:

- **ImageMap** → voxelized volume  
- **ImageMesh** → low-poly mesh (.obj)

---

Voxelized Image with ImageMap
-----------------------------

.. code-block:: python

   from voxelmap import Model
   import cv2, matplotlib.pyplot as plt

   # load an image (grayscale topography)
   model = Model(file="docs/img/land.png")

   # blur for smoother levels
   model.array = cv2.blur(model.array, (10, 10))

   # map to voxel depth
   model.array = model.ImageMap(depth=12)

   # gradient coloring
   from matplotlib import cm
   model.colormap = cm.terrain
   model.alphacm = 0.5
   model.draw_mpl("linear", figsize=(8, 6))

➡ Produces a voxelized terrain.

---

Low-Poly Mesh with ImageMesh
----------------------------

.. code-block:: python

   model.ImageMesh(out_file="land.obj", L_sectors=15)
   model.MeshView("land.obj", color="white", alpha=0.8)

➡ Produces a lightweight `.obj` mesh (interactive).

.. image:: ../../img/land_imagemesh.png
   :width: 400
   :alt: Low-poly terrain mesh

