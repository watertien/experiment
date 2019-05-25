import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

__author__ = 'Tian'

fname = "../data/E1_R_mean.csv"
names = ["temp", "B", "voltage", "current"] # Unit: K, kG, mV, A
data = pd.read_csv(fname, header=0, index_col=0, names=names)

fig, ax = plt.subplots()

magnetic = [0, 1, 2, 3, 4, 5]
for field in magnetic:
    forward = data[(abs(data.B - field) < 0.1) & (data.current > 0)].copy(deep=True)
    backward  = data[(abs(data.B - field) < 0.1) & (data.current < 0)].copy(deep=True)
    resistance = (forward.voltage - backward.voltage.values) / (forward.current - backward.current.values)
    ax.plot(forward.temp, resistance, \
                'o--', markersize=3, alpha=.7, label=f'B={field:.1f}kG')

ax.set_xlabel("Temperature/K")
ax.set_ylabel("Resistance/m$\Omega$")
ax.set_title("R-T Graph")
plt.legend()
plt.show()
