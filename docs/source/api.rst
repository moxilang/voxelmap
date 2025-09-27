API Reference
=============

This page lists the main functions and classes in **VoxelMap v5.0.0**.

---

Global Functions
----------------

.. autofunction:: voxelmap.objcast
   :no-index:
   
Mesh (requires `[mesh]`)
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: voxelmap.mesh.MarchingMesh
   :no-index:

.. autofunction:: voxelmap.mesh.MeshView
   :no-index:

.. autofunction:: voxelmap.mesh.ImageMesh
   :no-index:




I/O (requires `[io]`)
^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: voxelmap.io.save_array
   :no-index:
.. autofunction:: voxelmap.io.load_array
   :no-index:
.. autofunction:: voxelmap.io.tojson
   :no-index:
.. autofunction:: voxelmap.io.load_from_json
   :no-index:


---

Model Class
-----------

.. autoclass:: voxelmap.Model
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

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
   voxelmap.io
   voxelmap.mesh

# 👇 add this section to include stub pages in the build
Generated API Docs
------------------

.. toctree::
   :maxdepth: 1
   :glob:

   generated/*
