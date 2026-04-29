
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
# RUN from. src file
# From errorfile Task8_time
buildings = np.array([10,12,14,16,18,20])
time_real = np.array([9.496,11.224,13.105,14.960,16.741,18.635 ]) # DISSE SKAL OPDTAERES

# Linear fit with intercept = 0
slope = np.dot(buildings, time_real) / np.dot(buildings, buildings)
trendline = slope * buildings

#Plot
plt.figure(figsize=(8, 6))
plt.scatter(buildings, time_real, color='blue', label='Actual Data', zorder=5)
plt.plot(buildings, trendline, color='red', label=f'Linear Fit (y={slope:.2f}x)')
plt.xlabel('Number of Buildings')
plt.ylabel('Time (seconds)')
plt.title('Time vs Buildings')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# Save the image
figure_name='Task8_linear_regression_5points_evn2026.png'
save_path = os.path.join('figures', figure_name)
plt.savefig(save_path)

print(f"Plot saved successfully as '{figure_name}")
print(f"Regression Equation: Time = {slope:.2f} * Buildings ")