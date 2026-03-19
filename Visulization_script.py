from os.path import join
import sys

import numpy as np
import matplotlib.pyplot as plt


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

if len(sys.argv) < 2:
    N = 1
else:
    N = int(sys.argv[1])
building_ids = building_ids[:N]

    # Load floor plans
all_u0 = np.empty((N, 514, 514))
all_interior_mask = np.empty((N, 512, 512), dtype='bool')
for i, bid in enumerate(building_ids):
    u0, interior_mask = load_data(LOAD_DIR, bid)
    all_u0[i] = u0
    all_interior_mask[i] = interior_mask


# Create figure and two subplots
fig, axs = plt.subplots(2, 1)

# First subplot
axs[0].imshow(all_u0[0])
axs[0].set_title("First building, initial conditions")

# Second subplot
axs[1].imshow(all_interior_mask[0])
axs[1].set_title("First building, interior points mask")

# Adjust layout
plt.tight_layout()
plt.savefig("Firstbuildingplot.png")