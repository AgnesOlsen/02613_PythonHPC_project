
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
# RUN from. src file
# From errorfile Tast Task2_29094101
buildings = np.array([10,12,14,16,18,20])
time_real = np.array([92.631,124.263,158.257,175.721,201.489,233.251 ])

#Degree 1 = linear fit
slope, intercept = np.polyfit(buildings, time_real, 1)
trendline = slope * buildings + intercept

#Plot
plt.figure(figsize=(8, 6))
plt.scatter(buildings, time_real, color='blue', label='Actual Data', zorder=5)
plt.plot(buildings, trendline, color='red', label=f'Linear Fit (y={slope:.2f}x + {intercept:.2f})')
plt.xlabel('Number of Buildings')
plt.ylabel('Time (seconds)')
plt.title('Time vs Buildings')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# 5. Save the image
# You can change the filename here. 'dpi' makes it look sharper.
figure_name='linear_regression_5points.png'
save_path = os.path.join('..', 'figures', figure_name)
plt.savefig(save_path)

print(f"Plot saved successfully as '{figure_name}")
print(f"Regression Equation: Time = {slope:.2f} * Buildings + ({intercept:.2f})")