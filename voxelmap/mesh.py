"""
voxelmap.mesh
Heavy extras: PyVista, ConvexHull, Marching Cubes
"""
from scipy.spatial import ConvexHull
import numpy as np

try:
    import pyvista
    from scipy.spatial import ConvexHull
    from skimage import measure
    import cv2
except ImportError as e:
    raise ImportError(
        "PyVista is required for voxelmap.mesh. "
        "Install with `pip install voxelmap[mesh]`."
    ) from e

from voxelmap.core import Model


def _draw(self, coloring="custom", background_color="#cccccc",
          window_size=(1024, 768), len_voxel=1, show=True):
    """Interactive 3D voxel rendering with PyVista"""
    if self.array is None:
        raise ValueError("Model has no voxel array to draw.")

    xx, yy, zz = np.argwhere(self.array > 0).T
    centers = np.vstack((xx, yy, zz)).T

    pl = pyvista.Plotter(window_size=window_size)
    pl.set_background(background_color)

    # Handle coloring scheme
    import matplotlib.pyplot as plt
    from matplotlib import colors as mcolors

    if coloring.startswith("uniform:"):
        color_all = coloring.split(":")[1].strip()
        voxel_colors = {val: (color_all, 1.0) for val in np.unique(self.array)}
    elif coloring.startswith("colormap:"):
        cmap_name = coloring.split(":")[1].strip()
        cmap = getattr(plt.cm, cmap_name, plt.cm.viridis)
        norm = plt.Normalize(vmin=self.array.min(), vmax=self.array.max())
        voxel_colors = {
            val: (mcolors.to_hex(cmap(norm(val))), 1.0)
            for val in np.unique(self.array)
        }
    else:  # "custom"
        voxel_colors = self.hashblocks

    for center in centers:
        voxel = pyvista.Cube(center=center, x_length=len_voxel,
                        y_length=len_voxel, z_length=len_voxel)
        val = self.array[tuple(center)]
        if val in voxel_colors:
            color, alpha = voxel_colors[val]
            pl.add_mesh(voxel, color=color, opacity=alpha)
        else:
            pl.add_mesh(voxel, color="white", opacity=1.0)

    if show:
        pl.show()
    else:
        return pl



# Monkey-patch onto Model
setattr(Model, "draw", _draw)



def MarchingMesh(array, out_file="scene.obj", level=0, spacing=(1., 1., 1.)):
    verts, faces, normals, values = measure.marching_cubes(array, level=level, spacing=spacing)
    with open(out_file, "w") as f:
        for v in verts:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")


def MeshView(objfile="scene.obj", color="black", alpha=1.0,
             wireframe=True, background_color="#cccccc"):
    mesh = pyvista.read(objfile)
    theme = pyvista.themes.DefaultTheme()
    theme.color = color
    theme.show_edges = wireframe
    theme.background = background_color
    mesh.plot(theme=theme, opacity=alpha)


def ImageMap(image_array, depth=5):
    """Map 2D array (image) into 3D voxel depth"""
    L, W = image_array.shape
    low, high = np.min(image_array), np.max(image_array)
    intensities = np.linspace(low, high, depth).astype(int)
    model = np.zeros((depth, L, W))
    for j in range(L):
        for i in range(W):
            val = image_array[j, i]
            idx = (np.abs(intensities - val)).argmin()
            model[idx, j, i] = 1
    return model


def ImageMesh(image_array, out_file="scene.obj", L_sectors=4, rel_depth=1.0):
    """ConvexHull triangulation of 2D image sectors"""
    L, W = image_array.shape
    points = []
    simplices = []
    num = 0
    for i in range(L_sectors):
        for j in range(L_sectors):
            sub = image_array[int(i*L/L_sectors):int((i+1)*L/L_sectors),
                              int(j*W/L_sectors):int((j+1)*W/L_sectors)]
            coords = np.argwhere(sub > 0)
            if len(coords) > 3:
                pts = np.column_stack([
                    coords[:, 0] + i*L//L_sectors,   # y
                    coords[:, 1] + j*W//L_sectors,   # x
                    rel_depth * np.ones(len(coords)) # z
                ])
                hull = ConvexHull(pts, qhull_options="QJ")  # 👈 joggle fix
                simplices.extend(hull.simplices + num)
                points.extend(pts)
                num += len(pts)

    with open(out_file, "w") as f:
        for p in points:
            f.write(f"v {p[0]} {p[1]} {p[2]}\n")
        for s in simplices:
            f.write(f"f {s[0]+1} {s[1]+1} {s[2]+1}\n")
