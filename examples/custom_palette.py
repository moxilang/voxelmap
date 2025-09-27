import numpy as np
from voxelmap import Model

array = np.indices((4, 4, 4)).sum(axis=0) % 4 + 1

model = Model(array)
model.palette = {1: "black", 2: "white", 3: "magenta", 4: "cyan"}
model.draw_mpl(coloring="custom")

