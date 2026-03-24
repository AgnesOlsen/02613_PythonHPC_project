import numpy as np
import matplotlib.pyplot as plt
import os
numpy_load  = np.array([(1,2),(2,4),(3,8)]) #Erstat med load af npy-fil
# Load data from Task5
processes = numpy_load[:,0]
speedup = numpy_load[:,1]

# Ahmdals law - we play with fraction F.
F = 0.8 # Ændre for at finde den rigtige
speedup_ahmdahl = 1/((1-F)+F/processes)

plt.figure(figsize=(8, 6))
plt.plot(processes, speedup, marker = 'o', label = "Actual data")
plt.plot(processes, speedup_ahmdahl, label = f"Fit using parallel fraction: {F}") # Udkommenter dette for kun speed up plot.
plt.xlabel('Number of Processes')
plt.ylabel('Speed up')
plt.title('Speedup vs Processes')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

figure_name='Parallelfraction_plot.png' # ændre navn for kun speedup plot
save_path = os.path.join('..', 'figures', figure_name)
plt.savefig(save_path)

#### Theoretical speed up - We use S(oo)=1/(1-F), can only be found after F is found
theo_speed = 1/(1-F)
print(f"Theoretical speedup: {theo_speed}")

#### Time it takes to process all the floor plans using best parallelization
# Must be found by dividing our estimate for T(1) by the speed up we have. 