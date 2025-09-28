"""
voxelmap.mesh
=============
Mesh generation and visualization utilities.

Public functions:
- MeshView     → view OBJ with palette, wireframe, flat, or background options
- MarchingMesh → convert voxel arrays to OBJ+MTL
- ImageMap     → map 2D image into voxel depth
- ImageMesh    → triangulate 2D image into 3D OBJ
"""

from .render import MeshView, _draw
from .meshgen import MarchingMesh
from .image import ImageMap, ImageMesh

__all__ = [
    "MeshView",
    "MarchingMesh",
    "ImageMap",
    "ImageMesh",
]
