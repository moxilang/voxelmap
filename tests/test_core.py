import numpy as np
import pytest
from voxelmap.core import Model, binarize

def test_binarize_basic():
    arr = np.array([[0, 1], [2, 0]])
    out = binarize(arr)
    assert out.tolist() == [[0, 1], [1, 0]]

def test_model_build_voxels():
    arr = np.zeros((3, 3, 3))
    arr[1, 1, 1] = 1
    model = Model(arr)
    voxels = model.build()
    assert voxels.shape == arr.shape
    assert voxels.any()

def test_model_save_load_json(tmp_path):
    arr = np.zeros((2, 2, 2))
    arr[0, 0, 0] = 1
    model = Model(arr)
    path = tmp_path / "test.json"
    model.save(str(path))

    loaded = Model()
    loaded.load(str(path))
    assert loaded.array.shape == arr.shape
    assert loaded.array[0, 0, 0] == 1

