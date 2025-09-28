import numpy as np
from skimage import measure


def _write_mtl(mtlfile, palette):
    from matplotlib import colors as mcolors
    with open(mtlfile, "w") as m:
        for key, (c, a) in palette.items():
            r, g, b = mcolors.to_rgb(c)
            m.write(f"newmtl mat{int(key)}\n")
            m.write(f"Kd {r:.6f} {g:.6f} {b:.6f}\n")
            m.write(f"d {float(a):.6f}\n\n")


def MarchingMesh(array, palette=None, out_file="scene.obj",
                 spacing=(1.0, 1.0, 1.0), level=0.5, pad=1):
    """Marching-cubes per label (1,2,3,...) with OBJ+MTL export."""
    objfile = out_file if out_file.endswith(".obj") else out_file + ".obj"
    mtlfile = objfile[:-4] + ".mtl"

    labels = [int(v) for v in np.unique(array) if v != 0]
    labels.sort()
    if palette is None:
        palette = {v: ("#ffffff", 1.0) for v in labels}

    found_labels = []
    vert_offset = 0
    with open(objfile, "w") as f:
        f.write(f"# voxelmap OBJ (per-label marching cubes)\n")
        f.write(f"mtllib {mtlfile.split('/')[-1]}\n")

        for lab in labels:
            mask = (array == lab).astype(np.uint8)
            if pad > 0:
                mask = np.pad(mask, pad, mode="constant", constant_values=0)

            verts, faces, _, _ = measure.marching_cubes(
                mask, level=level, spacing=spacing, allow_degenerate=False, step_size=1
            )
            if verts.size == 0 or faces.size == 0:
                continue

            shift = np.array([pad * s for s in spacing], dtype=float)
            verts = verts - shift

            f.write(f"o label_{lab}\nusemtl mat{lab}\n")
            for v in verts:
                f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            for tri in faces:
                a, b, c = tri.astype(int) + 1 + vert_offset
                f.write(f"f {a} {b} {c}\n")

            vert_offset += verts.shape[0]
            found_labels.append(lab)

    if found_labels:
        filtered_palette = {k: palette[k] for k in found_labels if k in palette}
        _write_mtl(mtlfile, filtered_palette)
    else:
        with open(mtlfile, "w") as m:
            m.write("# empty material file\n")

