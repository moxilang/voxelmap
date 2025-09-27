import numpy as np
from voxelmap import Model

array = np.ones((3, 3, 3))        # simple 3×3×3 cube
model = Model(array)
model.set_color(1, "red")         # assign color to voxel value
model.draw_mpl(coloring="custom") # display with Matplotlib

