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


fig, axs = plt.subplots(2, 4, figsize=(16, 6), constrained_layout=True)

for i in range(4):
    axs[0, i].imshow(all_u0[i])
    axs[0, i].set_title(f"Building {building_ids[i]}\nInitial Conditions", fontsize=10, pad=6)
    axs[0, i].axis("off")
    axs[1, i].imshow(all_interior_mask[i])
    axs[1, i].set_title(f"Building {building_ids[i]}\nInterior Points", fontsize=10, pad=6)
    axs[1, i].axis("off")
fig.suptitle("Visualization of First Four Buildings", fontsize=14)
plt.savefig("Buildingplot.png", dpi=300, bbox_inches="tight")
