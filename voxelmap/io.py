"""
voxelmap.io
I/O utilities: save/load arrays, JSON, TXT, OBJ conversion
"""

import json
import pickle
import numpy as np
import pandas as pd


def save_array(array, filename):
    with open(filename, "wb") as f:
        pickle.dump(array, f)


def load_array(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def tojson(filename, array, hashblocks=None):
    if hashblocks is None:
        hashblocks = {}
    data = {"hashblocks": hashblocks, "size": list(array.shape),
            "coords": [], "val": []}
    Z, Y, X = array.shape
    for k in range(Z):
        for j in range(Y):
            for i in range(X):
                if array[k, j, i] != 0:
                    data["coords"].append([k, j, i])
                    data["val"].append(int(array[k, j, i]))
    with open(filename, "w") as f:
        json.dump(data, f)


def load_from_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def toTXT(filename, array, hashblocks=None):
    if hashblocks is None:
        hashblocks = {}
    Z, Y, X = array.shape
    header = ["# Goxel export\n", "# X Y Z RRGGBB\n"]
    with open(filename, "w") as f:
        f.writelines(header)
        for k in range(Z):
            for j in range(Y):
                for i in range(X):
                    if array[k, j, i] != 0:
                        color = hashblocks.get(array[k, j, i], ["#ffffff", 1])[0]
                        f.write(f"{i} {j} {k} {color[1:]} \n")


def wavefront_to_xyz(filename):
    """Parse OBJ into DataFrame"""
    verts = []
    with open(filename) as f:
        for line in f:
            if line.startswith("v "):
                _, x, y, z = line.strip().split()
                verts.append([float(z), float(y), float(x), "#ffffff"])
    return pd.DataFrame(verts, columns=["z", "y", "x", "rgb"])


def objcast(filename, spacing=1):
    df = wavefront_to_xyz(filename)
    Z, Y, X = (df["z"].max() + 1, df["y"].max() + 1, df["x"].max() + 1)
    array = np.zeros((int(Z), int(Y), int(X)))
    for _, row in df.iterrows():
        z, y, x = map(int, row[:3])
        array[z, y, x] = 1
    return array

