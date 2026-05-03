import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

df = pd.read_csv("stats/summary_statistics_7.csv")

# histogram
plt.figure()
plt.hist(df['mean_temp'])
plt.title("Mean temperatures")
plt.xlabel("Temperature")
plt.savefig("figures/Task12_histograms.png")
plt.close()


print("Average mean temperature:",np.mean(df['mean_temp']))
print("Average std. of temperature:",np.mean(df['std_temp']))

print("Buildings with 50p area above 18deg",sum(df["pct_above_18"] > 50))
print("Buildings with 50p area below 15deg",sum(df["pct_below_15"] > 50))

