# -*- encoding: utf8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.constants import Boltzmann

__author__ = 'Tian'

fname = r"../data/E1_thermal_noise_increasing.xls"
col_name = ['R', 'temp', 'B', 'X', 'Y', 'theta', 'freq', 'noise']
data = pd.read_csv(fname, delimiter='\t', names=col_name, skiprows=[0, 1], engine="python")

dT = 10
bins = np.arange(65, 200, dT)
noise_rms = np.zeros(len(bins)-1, dtype="float")
temps = np.arange(65 + dT/2, 200, dT)
inds = np.digitize(data.temp, bins=bins)

foo = np.linspace(0, 200)
ana = (4 * Boltzmann * foo * 10e3 * 5/ (64 * 0.3))**0.5 * 10**9

for i in range(1, bins.size):
    noise_rms[i-1] = np.sum(data.noise[inds == i]**2)

noise_rms = (noise_rms / np.bincount(inds)[1:-1])**0.5 * 10**9

fig, ax = plt.subplots()
ax.plot(temps[:len(noise_rms)], noise_rms, "ro", alpha=.7, markeredgecolor="red", label=f"Actual Measurement($\Delta T=${dT}K)")
ax.plot(foo, ana + 7, "k--", alpha=.5, label="Theory")
# ax.plot(data.temp, data.noise * 1e9, 'ro', alpha=.3, label='Raw Data')
ax.set_xlabel("Temperature/K")
ax.set_ylabel("Noise/nV")
ax.set_title("Thermal Noise of Resistor(10k)")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_position(("data", 0))
ax.spines["bottom"].set_position(("data", 0))
ax.set_xlim(0,)
ax.set_ylim(0,)
ax.legend(loc="best")
# plt.savefig(f"../figure/E1_thermal_noise_bin{dT}.png", dpi=450, transparent=True)
# plt.savefig(f"../figure/E1_thermal_noise_raw.png", dpi=450, transparent=True)
plt.show()
