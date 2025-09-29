import numpy as np
import pyvista

from ..core import Model

def _parse_face_labels_from_obj(objfile):
    """Parse OBJ to get a list of label IDs per face using 'usemtl mat<id>'."""
    face_labels, current = [], None
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


def MeshView(objfile="scene.obj", palette=None, alpha=1.0,
             mode="both", background_color="#000000", background_image=None,
             wireframe_color="white", flat_color="white"):
    """
    OBJ viewer with modes:
      - "solid": surfaces colored by palette
      - "wireframe": only edges, no fills
      - "both": filled faces + edges (with palette)
      - "flat": single solid color fill (ignores palette)
    """
    import matplotlib.pyplot as plt
    from matplotlib import colors as mcolors

    mesh = pyvista.read(objfile)

    # Theme setup
    if hasattr(pyvista.themes, "DefaultTheme"):
        theme = pyvista.themes.DefaultTheme()
    else:
        theme = pyvista.themes.Theme()
    theme.background = background_color
    theme.show_edges = (mode in ("wireframe", "both"))
    theme.edge_color = wireframe_color

    pl = pyvista.Plotter(theme=theme)
    if background_image is not None:
        pl.add_background_image(background_image)

    # --- Wireframe only ---
    if mode == "wireframe":
        pl.add_mesh(mesh, color=wireframe_color, style="wireframe")
        pl.show()
        return

    # --- Flat fill only ---
    if mode == "flat":
        pl.add_mesh(mesh, color=flat_color, opacity=alpha)
        pl.show()
        return

    # --- Solid or Both: split per label ---
    if palette is not None:
        face_labels = _parse_face_labels_from_obj(objfile)
        if len(face_labels) == mesh.n_cells:
            face_labels = np.array(face_labels)

            for lab in np.unique(face_labels):
                mask = np.where(face_labels == lab)[0]
                submesh = mesh.extract_cells(mask)

                if lab in palette:
                    c, a = palette[lab]
                    r, g, b = mcolors.to_rgb(c)
                    pl.add_mesh(
                        submesh,
                        color=(r, g, b),
                        opacity=a,
                        style="surface" if mode == "solid" else "surface",
                        show_edges=(mode == "both"),
                        edge_color=wireframe_color if mode == "both" else None
                    )
                else:
                    pl.add_mesh(submesh, color="gray", opacity=1.0)
        else:
            # fallback: whole mesh, global alpha
            pl.add_mesh(mesh, opacity=alpha)
    else:
        pl.add_mesh(mesh, opacity=alpha)

    pl.show()
