API Reference
=============

This page lists the main functions and classes in **VoxelMap v5.0.0**.

---

Global Functions
----------------

.. autofunction:: voxelmap.objcast

Mesh (requires `[mesh]`)
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: voxelmap.MarchingMesh
.. autofunction:: voxelmap.MeshView
.. autofunction:: voxelmap.ImageMesh

I/O (requires `[io]`)
^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: voxelmap.save_array
.. autofunction:: voxelmap.load_array
.. autofunction:: voxelmap.tojson
.. autofunction:: voxelmap.load_from_json

---

Model Class
-----------

.. autoclass:: voxelmap.Model
   :members:
   :undoc-members:
   :show-inheritance:

Key methods include:
- ``set_color`` — assign a color to a voxel value.  
- ``draw_mpl`` — render voxels with Matplotlib.  
- ``draw`` — interactive rendering (PyVista, requires `[mesh]`).  
- ``save`` / ``load`` — persist models as JSON or TXT.  
- ``ImageMap`` — map 2D images to voxel arrays.  

---

Autosummary Index
-----------------

.. autosummary::
   :toctree: generated

   voxelmap
   voxelmap.Model
   voxelmap.objcast
   voxelmap.ImageMesh
   voxelmap.MarchingMesh
   voxelmap.MeshView

