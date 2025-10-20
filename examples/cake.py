import numpy as np
from voxelmap import Model

def export_to_js(tensor):

    # Convert to nested lists
    tensor_list = tensor.tolist()

    # Build JavaScript string
    js_code = f"const tensor_structure = {tensor_list}\n\nexport default tensor_structure;"

    # Save to file
    with open("tensor_structure.js", "w") as f:
        f.write(js_code)

    print("✅ Wrote tensor_structure.js")

# Create blank voxel grid
arr = np.zeros((12, 11, 11), dtype=int)

# Helper: add a cylinder layer of voxels
def add_cylinder(z_start, z_end, radius, label):
    cz, cy, cx = np.array(arr.shape) // 2
    for z in range(z_start, z_end):
        for y in range(arr.shape[1]):
            for x in range(arr.shape[2]):
                if (x - cx)**2 + (y - cy)**2 <= radius**2:
                    arr[z, y, x] = label

# 🍰 Cake layers
add_cylinder(0, 3, 5, 1)   # bottom
add_cylinder(3, 6, 4, 2)   # middle
add_cylinder(6, 8, 3, 3)   # top

# 🕯️ Candles
candles = [(5,5), (3,3), (3,7), (7,3), (7,7)]
for y, x in candles:
    arr[8:11, y, x] = 4  # stick
    arr[11, y, x] = 5    # flame

# Build and color model
m = Model(arr)
m.set_color(1, "sandybrown")
m.set_color(2, "wheat")
m.set_color(3, "mistyrose")
m.set_color(4, "blue")
m.set_color(5, "gold",0.25)

export_to_js(arr)

# 🎨 Draw voxelized cake
m.draw("custom")  # Requires voxelmap[mesh]


