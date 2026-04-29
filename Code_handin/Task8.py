from os.path import join
import sys
import numpy as np
from numba import jit
from numba import cuda
import matplotlib.pyplot as plt
import time

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask


@cuda.jit
def jacobi_cuda_kernel(u, u_new, interior_mask):
    # Create grid
    i, j = cuda.grid(2)
    if 1 <= i < u.shape[0] - 1 and 1 <= j < u.shape[1] - 1: # Make sure that we are not out of bounds
        if interior_mask[i-1,j-1]: # Do it only for the mask
            u_new[i, j] = 0.25 * (
                    u[i, j - 1] +  
                    u[i, j + 1] +  
                    u[i - 1, j] +  
                    u[i + 1, j]    
                )
        else:
            u_new[i, j] = u[i, j] 

def jacobi_helper(u,interior_mask,iter):

    # define tpb and bpg
    tpb = (32,32)
    bpg = (u.shape[0]// tpb[0], 
           u.shape[1] // tpb[1])

    # copy to GPU
    d_u = cuda.to_device(u)
    d_u_new = cuda.device_array_like(d_u)
    d_mask = cuda.to_device(interior_mask)

    # Do iterations
    for i in range(iter):
        jacobi_cuda_kernel[bpg, tpb](d_u, d_u_new, d_mask)
        d_u, d_u_new = d_u_new, d_u
    

    return d_u.copy_to_host() 

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

#### Have to compile kernel 1 time before timing - so we need to load building ID's etc to compile 

LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
    building_ids = f.read().splitlines()
building_ids = building_ids[:1]

# Load only one floor plan
all_u0 = np.empty((1, 514, 514))
all_interior_mask = np.empty((1, 512, 512), dtype='bool')
for i, bid in enumerate(building_ids):
    u0, interior_mask = load_data(LOAD_DIR, bid)
    all_u0[i] = u0
    all_interior_mask[i] = interior_mask

# Run jacobi iterations for each floor plan
ITER = 5000

all_u = np.empty_like(all_u0)
for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
    u = jacobi_helper(u0, interior_mask, ITER)
    all_u[i] = u


if __name__ == '__main__':
    # Load data - we also time this to accurately compare to reference. 
    
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
    start_time = time.time()
    # Run jacobi iterations for each floor plan
    ITER = 20_000
    start_time = time.time()
    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi_helper(u0, interior_mask, ITER)
        all_u[i] = u
    
    print(f"Time for {N} is {time.time()-start_time}")

    # Print summary statistics in CSV format
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))

# Plot first 4 to make sure that functions are correct
fig, axs = plt.subplots(1, 4, figsize=(16, 6), constrained_layout=True)

for i in range(4):
    axs[i].imshow(all_u[i])
    axs[i].set_title(f"Building {building_ids[i]}\nSimulation Results", fontsize=10, pad=6)
    axs[i].axis("off")
fig.suptitle("Visualization of First Four Buildings", fontsize=14)
path_save = join('figures',"Task8_evn2026.png")
plt.savefig(path_save,dpi=300, bbox_inches="tight")