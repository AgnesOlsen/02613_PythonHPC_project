import numpy as np
import matplotlib.pyplot as plt
import os
# Load data from Task5
numpy_load  = np.load("/zhome/4f/c/186668/Desktop/02613_HPC/02613_PythonHPC_project/stats/static_time_50_1to16_evn26.npy")
processes = numpy_load[:,0]
times = numpy_load[:,1]
speedup = times[0]/times 

# Ahmdals law - we play with fraction F.
F = np.array([0.8,0.82,0.84,0.86,0.88,0.9] )
speedup_ahmdahl = []
for i in range(len(F)):
    speedup_a = 1/((1-F[i])+F[i]/processes)
    speedup_ahmdahl.append(speedup_a)


plt.figure(figsize=(8, 6))
plt.plot(processes, speedup, marker = 'o', label = "Speed-up")
for i in range(len(F)):
    plt.plot(processes, speedup_ahmdahl[i], label = f"Fit using parallel fraction: {F[i]}") # Udkommenter dette for kun speed-up plot.
plt.xlabel('Number of Workers')
plt.ylabel('Speed-up')
plt.title('Speedup vs Workers')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

figure_name='Task_5_estimationofparallelfraction_32s_evn26.png' # ændre navn for kun speedup plot
save_path = os.path.join('..', 'figures', figure_name)
plt.savefig(save_path)

#### Theoretical speed up - We use S(oo)=1/(1-F), can only be found after F is found
para_fraction = 0.84 # chosen from the plot
theo_speed = 1/(1-para_fraction)
print(f"Theoretical speedup: {theo_speed}")
## We reach 4.8 ish speed up at 14 cores. 

#### Time it takes to process all the floor plans using best parallelization
# Must be found by dividing our estimate for T(1) for all floorplans, see overleaf, by the speed up we have. 
print("How much time it would take using 14 cores:", 56681.07/speedup[7]) # This 3,27 hours 