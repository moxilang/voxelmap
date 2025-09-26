import numpy as np
import pytest
from voxelmap import Model


@pytest.mark.mesh
def test_draw_runs(monkeypatch):
    """Ensure interactive draw runs without errors when PyVista is available."""
    arr = np.ones((2, 2, 2))
    model = Model(arr)
    model.set_color(1, "blue")

    # Patch Plotter.show so no GUI opens
    import pyvista as pv
    monkeypatch.setattr(pv.Plotter, "show", lambda self, *a, **k: None)

    model.draw(coloring="custom")  # should not error


def test_draw_importerror(monkeypatch):
    """Ensure calling draw without PyVista installed raises ImportError."""
    import sys

    # Temporarily remove py

