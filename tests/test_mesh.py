import pytest
import numpy as np
import os

pytest.importorskip("pyvista")
pytest.importorskip("skimage")

from voxelmap.mesh import MarchingMesh, ImageMap, ImageMesh


def test_marching_mesh_obj_output(tmp_path):
    arr = np.zeros((6, 6, 6))
    arr[2:4, 2:4, 2:4] = 1  # cube
    objfile = tmp_path / "mesh.obj"
    MarchingMesh(arr, out_file=str(objfile))
    assert objfile.exists()
    with open(objfile) as f:
        content = f.read()
    assert "v " in content
    assert "f " in content


def test_marching_mesh_mtl_output(tmp_path):
    """Ensure MTL palette file is written alongside OBJ."""
    arr = np.zeros((5, 5, 5))
    arr[1:3, 1:3, 1:3] = 2  # cube with label=2
    objfile = tmp_path / "colored.obj"
    MarchingMesh(arr, palette={2: ("#00ff00", 0.7)}, out_file=str(objfile))

    mtlfile = objfile.with_suffix(".mtl")
    assert mtlfile.exists()

    content = mtlfile.read_text()
    # Check that correct material is defined
    assert "newmtl mat2" in content
    assert "Kd " in content
    assert "d 0.700000" in content


def test_imagemap_shape():
    arr = np.ones((10, 10))
    depth = 5
    mapped = ImageMap(arr, depth=depth)
    assert mapped.shape == (depth, 10, 10)
    assert mapped.any()


def test_imagemesh_obj_output(tmp_path):
    arr = np.random.randint(0, 2, (20, 20))
    objfile = tmp_path / "imgmesh.obj"
    ImageMesh(arr, out_file=str(objfile), L_sectors=4)
    assert objfile.exists()
