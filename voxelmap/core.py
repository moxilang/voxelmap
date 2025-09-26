"""
voxelmap.core
Lightweight core: minimal voxel model with numpy + matplotlib only
"""

import warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors, cm
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


def binarize(array, colorindex=1):
    """Convert array with integers into {0,1} array."""
    arrayv = np.zeros(array.shape, dtype=int)
    for i in np.argwhere(array != 0):
        arrayv[tuple(i)] = colorindex
    return arrayv


class Model:
    def __init__(self, array=None, file=""):
        self.file = file
        self.array = np.array(array) if array is not None else None

        # Preferred new API
        self._palette = {}
        self.colormap = cm.cool
        self.alphacm = 1
        self.objfile = "scene.obj"
        self.XYZ = []
        self.RGB = []
        self.sparsity = 10.0

    # -------------------------
    # New API
    # -------------------------
    @property
    def palette(self):
        """Voxel palette: maps voxel values → (color, alpha)."""
        return self._palette

    @palette.setter
    def palette(self, new_palette: dict):
        parsed = {}
        for key, val in new_palette.items():
            if isinstance(val, tuple):  # (color, alpha)
                parsed[key] = val
            else:  # just color string
                parsed[key] = (val, 1.0)
        self._palette = parsed

    def set_color(self, key: int, color: str, alpha: float = 1.0):
        """Set color for a voxel type."""
        self._palette[key] = (color, alpha)

    # -------------------------
    # Backward compatibility
    # -------------------------
    @property
    def hashblocks(self):
        warnings.warn(
            "hashblocks is deprecated. Use `palette` instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._palette

    @hashblocks.setter
    def hashblocks(self, value):
        warnings.warn(
            "hashblocks is deprecated. Use `palette` instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.palette = value

    def hashblocks_add(self, key, color, alpha=1.0):
        warnings.warn(
            "hashblocks_add is deprecated. Use `set_color` instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.set_color(key, color, alpha)

    # -------------------------
    # Core functionality
    # -------------------------
    def build(self):
        """Build voxel boolean mask from self.array"""
        binarray = binarize(self.array)
        Z, X, Y = self.array.shape
        voxels = np.zeros_like(binarray, dtype=bool)
        for k in range(Z):
            for i in range(X):
                for j in range(Y):
                    if binarray[k, i, j] == 1:
                        voxels[k, i, j] = True
        return voxels

    def draw_mpl(self, coloring="custom", edgecolors=None,
                figsize=(6.4, 4.8), axis3don=False):
        """Draw voxel model with matplotlib"""
        Z, X, Y = self.array.shape
        voxcolors = np.ones((Z, X, Y), dtype=object)

        if coloring == "linear":
            colormap = self.colormap
            alphaval = self.alphacm
            for i in range(X):
                for j in range(Y):
                    for k in range(Z):
                        voxcolors[k, i, j] = colormap((j + 0.5) / Y, alpha=alphaval)

        elif coloring == "nuclear":
            colormap = self.colormap
            alphaval = self.alphacm

            def center_color(a, L):
                return abs(1 - 2*((a+0.5)/L))

            for i in range(X):
                for j in range(Y):
                    for k in range(Z):
                        ic = center_color(i, X)
                        jc = center_color(j, Y)
                        kc = center_color(k, Z)
                        voxcolors[k, i, j] = colormap(max(ic, jc, kc)-0.12, alpha=alphaval)

        elif coloring.startswith("custom"):
            # single-color option
            if ":" in coloring:
                parts = coloring.split(":")
                color_all = parts[1].strip()
                alpha_all = float(parts[2]) if len(parts) > 2 else 1.0
                for val in np.unique(self.array[self.array != 0]):
                    self.set_color(val, color_all, alpha_all)

            voxel_colmap = self._palette
            for k in range(Z):
                for i in range(X):
                    for j in range(Y):
                        if self.array[k][i][j] in voxel_colmap:
                            c, a = voxel_colmap[self.array[k][i][j]]
                            voxcolors[k, i, j] = (*colors.to_rgb(c), a)

        # --- plotting ---
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(projection="3d")
        ax._axis3don = axis3don
        voxels = self.build()
        ax.voxels(voxels, facecolors=voxcolors, edgecolors=edgecolors)
        plt.show()


    def save(self, filename="scene.json"):
        """Save model (JSON or TXT)."""
        if filename.endswith(".json"):
            from voxelmap.io import tojson
            tojson(filename, self.array, self._palette)
        elif filename.endswith(".txt"):
            from voxelmap.io import toTXT
            toTXT(filename, self.array, self._palette)
        else:
            raise ValueError("Unsupported file format")

    def load(self, filename="scene.json"):
        """Load model from JSON only (core)."""
        if filename.endswith(".json"):
            from voxelmap.io import load_from_json
            data = load_from_json(filename)
            self._palette = {
                int(k): tuple(v) for k, v in data["hashblocks"].items()
            }
            Z, Y, X = data["size"]
            self.array = np.zeros((Z, Y, X))
            for (z, y, x), val in zip(data["coords"], data["val"]):
                self.array[z, y, x] = val
        else:
            raise ValueError("Only JSON supported in core")
