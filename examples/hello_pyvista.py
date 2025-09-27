import numpy as np
from voxelmap import Model

array = np.ones((3, 3, 3))  # same cube
model = Model(array)
model.set_color(1, "red")

# Interactive PyVista window
model.draw(coloring="custom")
