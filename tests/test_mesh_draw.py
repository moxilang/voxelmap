import numpy as np
import pytest
from voxelmap import Model

pytest.importorskip("pyvista")

from voxelmap.mesh import MeshView


@pytest.mark.mesh
def test_draw_runs(monkeypatch):
    """Ensure interactive draw runs without errors when PyVista is available."""
    arr = np.ones((2, 2, 2))
    model = Model(arr)
    model.set_color(1, "blue")

    # Patch Plotter.show so no GUI opens
    import pyvista as pv
    monkeypatch.setattr(pv.Plotter, "show", lambda self, *a, **k: None)

    # Should not raise
    model.draw(coloring="custom")


def test_draw_importerror(monkeypatch):
    """Ensure calling draw without PyVista installed raises ImportError."""
    import sys

    # Backup sys.modules and remove pyvista
    sys_modules_backup = sys.modules.copy()
    sys.modules["pyvista"] = None

    arr = np.ones((2, 2, 2))
    model = Model(arr)
    model.set_color(1, "blue")

    with pytest.raises(ImportError):
        model.draw()

    # Restore sys.modules
    sys.modules.clear()
    sys.modules.update(sys_modules_backup)


@pytest.mark.mesh
def test_meshview_flatcolor(tmp_path, monkeypatch):
    """Ensure MeshView runs with flat_color mode and doesn't open GUI."""
    import pyvista as pv

    # Minimal OBJ file
    objfile = tmp_path / "flat.obj"
    with open(objfile, "w") as f:
        f.write("v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n")

    # Prevent GUI from opening
    monkeypatch.setattr(pv.Plotter, "show", lambda self, *a, **k: None)

    # Should not raise
    MeshView(str(objfile), flat_color="red", mode="flat")
