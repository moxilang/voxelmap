import numpy as np
from scipy.spatial import ConvexHull


def ImageMap(image_array, depth=5):
    """Map 2D array (image) into 3D voxel depth."""
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
    points, simplices, num = [], [], 0
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
