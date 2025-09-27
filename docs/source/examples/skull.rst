Voxel Model → 3D Mesh
=====================

VoxelMap can transform a voxel model from **Goxel** (exported `.txt`) into a 3D mesh.

First, download the model file:

.. code-block:: bash

   wget https://raw.githubusercontent.com/andrewrgarcia/voxelmap/main/model_files/skull.txt

---

Loading the Voxel Model
-----------------------

.. code-block:: python

   from voxelmap import Model

   model = Model()
   model.load("skull.txt")

   # basic voxel view (Matplotlib)
   model.set_color(1, "white")
   model.draw_mpl("custom")

➡ Produces a solid voxel rendering of the skull.

---

Convert to Mesh
---------------

.. code-block:: python

   model.MarchingMesh("skull.obj")
   model.MeshView("skull.obj", wireframe=True, color="white")

➡ Produces a 3D mesh view (requires `[mesh]`).

.. image:: ../../img/skull_mesh.png
   :width: 400
   :alt: Skull mesh preview

