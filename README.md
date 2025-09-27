<!-- LOGO -->
<p align="center">
 <img src="voxelmap.png" width="160"></a>

</p>
<h1 align="center">voxelmap</h1>
<p align="center">
A lightweight Python library for building  <strong>voxel models</strong> from NumPy arrays.
</p>


[![License](http://img.shields.io/\:license-mit-blue.svg?style=flat-square)](https://raw.githubusercontent.com/andrewrgarcia/voxelmap/main/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/voxelmap/badge/?version=latest)](https://voxelmap.readthedocs.io/en/latest/?badge=latest)

Simple to start, modular when you need more.

<a href="https://voxelmap.vercel.app">

---

## 🚀 Installation

Minimal core (NumPy + Matplotlib only):

```bash
pip install voxelmap
```

Optional extras:

```bash
pip install voxelmap[io]     # for I/O helpers (pandas, txt/obj conversions)
pip install voxelmap[mesh]   # for meshing (scipy, scikit-image, pyvista)
pip install voxelmap[all]    # everything
```

We recommend using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install voxelmap
```

Deactivate with:

```bash
deactivate
```

---

## 🧩 Quickstart

### 1. Hello World (Matplotlib, core only)

```python
import numpy as np
from voxelmap import Model

# Simple 3×3×3 cube
array = np.ones((3, 3, 3))

model = Model(array)
model.set_color(1, "red")         # assign color
model.draw_mpl(coloring="custom") # static Matplotlib 3D plot
```

➡️ Produces a **solid red cube** in a Matplotlib 3D plot.

* Rotate = left mouse drag
* Pan = right mouse drag
* Zoom = scroll wheel

*(Works with the minimal install, no extras required.)*

---

### 2. Interactive 3D (PyVista, mesh extra)

For full **trackball-style zoom, pan, and rotate**, install with:

```bash
pip install voxelmap[mesh]
```

Then:

```python
import numpy as np
from voxelmap import Model

array = np.ones((3, 3, 3))  # same cube
model = Model(array)
model.set_color(1, "red")

# Interactive PyVista window
model.draw(coloring="custom")
```

➡️ Opens an interactive window:

* Rotate freely (trackball)
* Smooth zoom with scroll/drag
* Pan and adjust camera in real time

---

### 3. Custom Palette (checkerboard)

```python
import numpy as np
from voxelmap import Model

array = np.indices((3, 3, 3)).sum(axis=0) % 2 + 1

model = Model(array)
model.palette = {1: "black", 2: "white"}
model.draw_mpl(coloring="custom")
```

➡️ Produces a **black/white checkerboard cube**.

---

### 4. Gradient Coloring

```python
import numpy as np
from voxelmap import Model
from matplotlib import cm

array = np.ones((10, 3, 3))  # tall column
model = Model(array)

model.colormap = cm.viridis
model.alphacm = 0.9
model.draw_mpl(coloring="linear")
```

➡️ Produces a **column shaded with a viridis vertical gradient**.

---

## 📚 Documentation

Full usage and advanced examples can be found here:
👉 [VoxelMap Documentation](https://voxelmap.readthedocs.io/en/latest)

---

## ⚖️ License

This program is free software. It comes without any warranty, to the extent permitted by applicable law.
You can redistribute it and/or modify it under the terms of the **MIT LICENSE**.

**[MIT license](./LICENSE)** © 2022–present [Andrew Garcia](https://github.com/andrewrgarcia)

