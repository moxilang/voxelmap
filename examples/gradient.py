import numpy as np
from voxelmap import Model
from matplotlib import cm

array = np.ones((10, 3, 3))  # tall column
model = Model(array)

model.colormap = cm.viridis
model.alphacm = 0.9
model.draw_mpl(coloring="linear")

