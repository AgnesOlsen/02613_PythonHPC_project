import numpy as np
import matplotlib.pyplot as plt
import os
# Load data from Task5 npy file
numpy_load  = np.load("/zhome/4f/c/186668/Desktop/02613_HPC/02613_PythonHPC_project/stats/static_time_50_1to16_evn26.npy")
processes = numpy_load[:,0]
times = numpy_load[:,1]
speedup = times[0]/times 

# Ahmdals law - we play with fraction F.
F = np.array([0.84,0.86,0.88,0.9,0.907] )
speedup_ahmdahl = []
for i in range(len(F)):
    speedup_a = 1/((1-F[i])+F[i]/processes)
    speedup_ahmdahl.append(speedup_a)

print("last element in list:", speedup_ahmdahl[-1][-1])

# We plot
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
#figure_name='Task_5_speedup_32s_evn26.png'
save_path = os.path.join('..', 'figures', figure_name)
plt.savefig(save_path)

#### Theoretical speed up - We use S(oo)=1/(1-F), can only be found after F is found
para_fraction = 0.88 # chosen from the plot
theo_speed = 1/(1-para_fraction)
print(f"Theoretical speedup using F:0.88: {theo_speed}")

#### Theoretical speed up - We use S(oo)=1/(1-F), can only be found after F is found
para_fraction = 0.907 # chosen from the plot
theo_speed = 1/(1-para_fraction)
print(f"Theoretical speedup using F:0.907: {theo_speed}")


#### Time it takes to process all the floor plans using best parallelization
# Must be found by dividing our estimate for T(1) for all floorplans, see overleaf, by the speed up we have. 

print("speedup 32", speedup[-1])
print("speedup 28,",speedup[-2])
print("How much time it would take using 32 cores:", 51149.49/speedup[-1])  


print("How much time it would take using 28 cores:", 51149.49/speedup[-2])  


