from voxelmap.core import Model, binarize
from voxelmap.io import (
    save_array, load_array,
    tojson, load_from_json,
    toTXT, objcast
)

__all__ = [
    "Model", "binarize",
    "save_array", "load_array",
    "tojson", "load_from_json",
    "toTXT", "objcast",
]

# Mesh extras (optional)
try:
    from voxelmap.mesh import MarchingMesh, MeshView, ImageMesh
except ImportError:
    # dependencies (pyvista, scipy, etc.) may be missing → just skip
    pass
else:
    # expose at top level
    globals().update({
        "MarchingMesh": MarchingMesh,
        "MeshView": MeshView,
        "ImageMesh": ImageMesh,
    })
    __all__.extend(["MarchingMesh", "MeshView", "ImageMesh"])
