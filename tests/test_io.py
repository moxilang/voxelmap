import numpy as np
import tempfile, os
from voxelmap.io import tojson, load_from_json, save_array, load_array, objcast, toTXT
from voxelmap import Model


def test_json_roundtrip(tmp_path):
    arr = np.zeros((2, 2, 2))
    arr[0, 0, 0] = 1
    filename = tmp_path / "scene.json"
    tojson(filename, arr, {1: ["#ffffff", 1]})
    data = load_from_json(filename)
    assert "coords" in data
    assert data["val"][0] == 1


def test_pickle_roundtrip(tmp_path):
    arr = np.random.randint(0, 10, (4, 4))
    filename = tmp_path / "arr.pkl"
    save_array(arr, filename)
    arr2 = load_array(filename)
    assert np.array_equal(arr, arr2)


def test_objcast_roundtrip(tmp_path):
    # Write a minimal OBJ file
    objfile = tmp_path / "cube.obj"
    with open(objfile, "w") as f:
        f.write("v 0 0 0\nv 1 0 0\nv 0 1 0\n")
    arr = objcast(str(objfile))
    assert arr.ndim == 3
    assert arr.any()


def test_txt_roundtrip(tmp_path):
    """Ensure saving and reading TXT via Model works (Goxel format)."""
    arr = np.zeros((3, 3, 3))
    arr[1, 1, 1] = 1
    model = Model(arr)
    model.set_color(1, "#ff0000")

    txtfile = tmp_path / "scene.txt"
    model.save(str(txtfile))

    # Verify file exists and has color entry
    content = txtfile.read_text()
    assert "ff0000" in content
    assert "1 1 1" in content
