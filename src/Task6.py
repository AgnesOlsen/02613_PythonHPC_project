import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from os.path import join
from time import time


print("starting paralellized script")

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

def jacobi(u, interior_mask, max_iter, atol=1e-6):
    u = np.copy(u)

    for i in range(max_iter):
        # Compute average of left, right, up and down neighbors, see eq. (1)
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])
        u_new_interior = u_new[interior_mask]
        delta = np.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max()
        u[1:-1, 1:-1][interior_mask] = u_new_interior

        if delta < atol:
            break
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

############

def processed(building_ids, LOAD_DIR):
    MAX_ITER = 20_000
    ABS_TOL = 1e-4
    N= len(building_ids)
    all_u0 = np.empty((N, 514, 514))
    all_u = np.empty((N, 514, 514 ))
    all_interior_mask = np.empty((N, 512, 512), dtype='bool')
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)

        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

        u = jacobi(u0, interior_mask, MAX_ITER, ABS_TOL)
        all_u[i] = u
    return all_u0, all_interior_mask, all_u

def parallelized_computations(building_ids, num_processes, LOAD_DIR):
    chunk_size = 1
    N = len(building_ids)//chunk_size + 1

    pool = multiprocessing.Pool(num_processes)
    result = [pool.apply_async(processed, 
                               (building_ids[i:min(len(building_ids), i+chunk_size)], LOAD_DIR)) 
                               for i in range(N)]
    loaded_buildings = [r.get() for r in result]

    loaded_buildings = tuple([item for sublist in group for item in sublist] for group in zip(*loaded_buildings))
    return loaded_buildings


##########


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

    num_processes = [1,2,4,8,16]
    time_list = []
    for num in num_processes:
        time_start = time()
        loaded_buildings = parallelized_computations(building_ids, num, LOAD_DIR)
        all_u0, all_interior_mask, all_u = loaded_buildings
        time_end = time()
        time_list.append([num, time_end - time_start])
    np.save("stats/dynamic_time_20.npy", time_list)