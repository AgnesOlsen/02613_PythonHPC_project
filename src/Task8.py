from os.path import join
import sys
import numpy as np
from numba import jit
from numba import cuda
import matplotlib.pyplot as plt

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

@cuda.jit
def jacobi_cuda_kernel(u, u_new, interior_mask):
    i, j = cuda.grid(2)
    # Interior indices (skip halo boundaries)
    if 1 <= i < u.shape[0] - 1 and 1 <= j < u.shape[1] - 1:
        u_new[i, j] = 0.25 * (
                u[i, j - 1] +  # left
                u[i, j + 1] +  # right
                u[i - 1, j] +  # up
                u[i + 1, j]    # down
            )

def jacobi_helper(u,interior_mask,iter):
    tpb = (32,32)
    bpg = (u.shape[0]// tpb[0], 
           u.shape[1] // tpb[1])

    u_new = np.zeros_like(u)
    for i in range(iter):
        jacobi_cuda_kernel[bpg, tpb](u, u_new, interior_mask)
        u[1:-1, 1:-1][interior_mask] = u_new[1:-1, 1:-1][interior_mask]
    return u

def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        'mean_temp': mean_temp,
        'std_temp': std_temp,
        'pct_above_18': pct_above_18,
        'pct_below_15': pct_below_15,
    }



if __name__ == '__main__':
    # Load data
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

    # Run jacobi iterations for each floor plan
    ITER = 10_000
    ABS_TOL = 1e-4

    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi_helper(u0, interior_mask, ITER)
        print(u)
        all_u[i] = u

    # Print summary statistics in CSV format
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))

    fig, axs = plt.subplots(1, 4, figsize=(16, 6), constrained_layout=True)

    for i in range(4):
        axs[i].imshow(all_u[i])
        axs[i].set_title(f"Building {building_ids[i]}\nSimulation Results", fontsize=10, pad=6)
        axs[i].axis("off")
    fig.suptitle("Visualization of First Four Buildings", fontsize=14)
    path_save = join('figures',"Task8_evn2026.png")
    plt.savefig(path_save,dpi=300, bbox_inches="tight")