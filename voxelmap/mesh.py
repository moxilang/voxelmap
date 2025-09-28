"""
voxelmap.mesh
Heavy extras: PyVista, ConvexHull, Marching Cubes
"""
from scipy.spatial import ConvexHull
import numpy as np

try:
    import pyvista
    from skimage import measure
    import cv2
except ImportError as e:
    raise ImportError(
        "PyVista is required for voxelmap.mesh. "
        "Install with `pip install voxelmap[mesh]`."
    ) from e

from .core import Model


def _draw(self, coloring="custom", background_color="#cccccc",
          window_size=(1024, 768), len_voxel=1, show=True):
    """Interactive 3D voxel rendering with PyVista (voxel-drawn cubes)."""
    if self.array is None:
        raise ValueError("Model has no voxel array to draw.")

    xx, yy, zz = np.argwhere(self.array > 0).T
    centers = np.vstack((xx, yy, zz)).T

    pl = pyvista.Plotter(window_size=window_size)
    pl.set_background(background_color)

    import matplotlib.pyplot as plt
    from matplotlib import colors as mcolors

    if coloring.startswith("uniform:"):
        color_all = coloring.split(":")[1].strip()
        voxel_colors = {val: (color_all, 1.0) for val in np.unique(self.array)}
    elif coloring.startswith("colormap:"):
        cmap_name = coloring.split(":")[1].strip()
        cmap = getattr(plt.cm, cmap_name, plt.cm.viridis)
        norm = plt.Normalize(vmin=self.array.min(), vmax=self.array.max())
        voxel_colors = {val: (mcolors.to_hex(cmap(norm(val))), 1.0)
                        for val in np.unique(self.array)}
    else:  # "custom"
        voxel_colors = self.hashblocks  # deprecated alias → palette

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



def _write_mtl(mtlfile, palette):
    from matplotlib import colors as mcolors
    with open(mtlfile, "w") as m:
        for key, (c, a) in palette.items():
            r, g, b = mcolors.to_rgb(c)
            m.write(f"newmtl mat{int(key)}\n")
            m.write(f"Kd {r:.6f} {g:.6f} {b:.6f}\n")
            m.write(f"d {float(a):.6f}\n\n")


def MarchingMesh(array, palette=None, out_file="scene.obj",spacing=(1.0, 1.0, 1.0), level=0.5, pad=1):
    """
    Marching-cubes per label (1,2,3,...) with OBJ+MTL export.
    - per-label binary masks avoid label mixing and color loss
    - padding prevents boundary clipping
    - level=0.5 robust for binary masks
    """
    objfile = out_file
    if not objfile.endswith(".obj"):
        objfile += ".obj"
    mtlfile = objfile[:-4] + ".mtl"

    labels = [int(v) for v in np.unique(array) if v != 0]
    labels.sort()
    if palette is None:
        palette = {v: ("#ffffff", 1.0) for v in labels}

    # MTL first (only for labels we actually find geometry for)
    found_labels = []

    # Prepare OBJ
    vert_offset = 0
    with open(objfile, "w") as f:
        f.write(f"# voxelmap OBJ (per-label marching cubes)\n")
        f.write(f"mtllib {mtlfile.split('/')[-1]}\n")

        for lab in labels:
            mask = (array == lab).astype(np.uint8)
            if pad > 0:
                mask = np.pad(mask, pad, mode="constant", constant_values=0)

            # run marching cubes on this label's mask
            # note: faces are triangles; verts are float coords in (z,y,x)-like order
            verts, faces, normals, _ = measure.marching_cubes(
                mask, level=level, spacing=spacing, allow_degenerate=False, step_size=1
            )
            if verts.size == 0 or faces.size == 0:
                continue

            # shift coordinates back to original (remove padding)
            shift = np.array([pad * spacing[0], pad * spacing[1], pad * spacing[2]], dtype=float)
            verts = verts - shift

            # write vertices
            f.write(f"o label_{lab}\nusemtl mat{lab}\n")
            for v in verts:
                f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

            # write faces (1-indexed, offset by previous vertex count)
            for tri in faces:
                a, b, c = tri.astype(int) + 1 + vert_offset
                f.write(f"f {a} {b} {c}\n")

            vert_offset += verts.shape[0]
            found_labels.append(lab)

    # write .mtl only for found labels (some labels may have produced no surface)
    if found_labels:
        filtered_palette = {k: palette[k] for k in found_labels if k in palette}
        _write_mtl(mtlfile, filtered_palette)
    else:
        # empty geometry: still create an empty MTL to avoid loader complaints
        with open(mtlfile, "w") as m:
            m.write("# empty material file (no surfaces found)\n")


def _parse_face_labels_from_obj(objfile):
    """Parse OBJ to get a list of label IDs per face using 'usemtl mat<id>'."""
    face_labels = []
    current = None
    with open(objfile, "r") as fh:
        for line in fh:
            if line.startswith("usemtl"):
                name = line.strip().split()[1]
                if name.startswith("mat"):
                    try:
                        current = int(name[3:])
                    except Exception:
                        current = None
            elif line.startswith("f "):
                face_labels.append(current)
    return face_labels


def MeshView(objfile="scene.obj", palette=None, alpha=1.0,
             mode="both", background_color="#000000", background_image=None,
             wireframe_color="white", flat_color="white"):
    """
    OBJ viewer with modes:
      - "solid": surfaces colored by palette
      - "wireframe": only edges, no fills
      - "both": filled faces + edges (with palette)
      - "flat": single solid color fill (ignores palette)

    Parameters
    ----------
    objfile : str
        Path to OBJ file.
    palette : dict, optional
        Mapping voxel_id -> (color, alpha). Used in "solid"/"both".
    alpha : float
        Opacity multiplier.
    mode : {"solid", "wireframe", "both", "flat"}
        Rendering mode.
    background_color : str
        Background color (hex or named).
    background_image : str, optional
        Path to PNG/JPG image for background.
    wireframe_color : str
        Color of the wireframe edges.
    flat_color : str
        Single fill color used in "flat" mode.
    """
    mesh = pyvista.read(objfile)

    # Theme setup
    if hasattr(pyvista.themes, "DefaultTheme"):
        theme = pyvista.themes.DefaultTheme()
    else:
        theme = pyvista.themes.Theme()
    theme.background = background_color
    theme.show_edges = (mode in ("wireframe", "both"))
    theme.edge_color = wireframe_color

    # Plotter (so we can set bg image)
    pl = pyvista.Plotter(theme=theme)
    if background_image is not None:
        pl.add_background_image(background_image)

    # --- Wireframe-only mode ---
    if mode == "wireframe":
        pl.add_mesh(mesh, color=wireframe_color, style="wireframe")
        pl.show()
        return

    # --- Flat mode (ignore palette) ---
    if mode == "flat":
        pl.add_mesh(mesh, color=flat_color, opacity=alpha)
        pl.show()
        return

    # --- Solid or Both (palette colors) ---
    if palette is not None:
        face_labels = _parse_face_labels_from_obj(objfile)
        if len(face_labels) == mesh.n_cells:
            from matplotlib import colors as mcolors
            colors_rgba = np.zeros((mesh.n_cells, 4), dtype=np.uint8)
            for i, lab in enumerate(face_labels):
                if lab in palette:
                    c, a = palette[lab]
                    r, g, b = mcolors.to_rgb(c)
                    colors_rgba[i] = [int(r*255), int(g*255), int(b*255), int(a*255)]
                else:
                    colors_rgba[i] = [200, 200, 200, 255]
            mesh.cell_data["colors"] = colors_rgba
            pl.add_mesh(mesh, scalars="colors", rgba=True, opacity=alpha)
        else:
            pl.add_mesh(mesh, opacity=alpha)
    else:
        pl.add_mesh(mesh, opacity=alpha)

    pl.show()


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
    """ConvexHull triangulation of 2D image sectors (geometry only)."""
    L, W = image_array.shape
    points, simplices = [], []
    num = 0
    for i in range(L_sectors):
        for j in range(L_sectors):
            sub = image_array[int(i*L/L_sectors):int((i+1)*L/L_sectors),
                              int(j*W/L_sectors):int((j+1)*W/L_sectors)]
            coords = np.argwhere(sub > 0)
            if len(coords) > 3:
                pts = np.column_stack([
                    coords[:, 0] + i*L//L_sectors,
                    coords[:, 1] + j*W//L_sectors,
                    rel_depth * np.ones(len(coords))
                ])
                hull = ConvexHull(pts, qhull_options="QJ")
                simplices.extend(hull.simplices + num)
                points.extend(pts)
                num += len(pts)

    with open(out_file, "w") as f:
        for p in points:
            f.write(f"v {p[0]} {p[1]} {p[2]}\n")
        for s in simplices:
            f.write(f"f {s[0]+1} {s[1]+1} {s[2]+1}\n")
