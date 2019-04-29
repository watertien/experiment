# -*- encoding: utf8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

__author__ = 'Tian'

fname = "../data/E1_chi_0G.xls"
col_name = ['R', 'temp', 'B', 'X', 'Y', 'theta', 'freq', 'noise']
data = pd.read_csv(fname, delimiter='\t', names=col_name, skiprows=[0, 1])

# Background phase difference
bg_phase = -155.48 * np.pi / 180 # Unit: radian
bg_phase_right = (-155.48 + 90) * np.pi / 180 # Unit: radian
bg_x = [np.cos(bg_phase), -np.cos(bg_phase)]
bg_y = [np.sin(bg_phase), -np.sin(bg_phase)]
bg_x_right = [np.cos(bg_phase_right), -np.cos(bg_phase_right)]
bg_y_right = [np.sin(bg_phase_right), -np.sin(bg_phase_right)]

# Caused by non-ideal and non-symmetry coils
non_ideal_coils = np.copy(np.mean(data[["X", "Y"]][data.temp == max(data.temp)]))
# Remove non-ideal term
points_offset = data[["X", "Y"]] - non_ideal_coils
# Get Re and Im parts
points_re = np.sum(points_offset * np.array([bg_x_right[0], bg_y_right[0]]), axis=1)
points_im = np.sum(points_offset * np.array([bg_x[0], bg_y[0]]), axis=1)

fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)

axs[0].plot(data.temp, points_im ,'ro', alpha=.4, markersize=3)
axs[0].set_ylabel(r"$K\cdot Im(\chi)$")
axs[0].set_title(r"$\chi$-T")
axs[0].ticklabel_format(axis='y', style='sci', scilimits=(-7, -6))

axs[1].plot(data.temp, points_re ,'bo', alpha=.4, markersize=3)
axs[1].ticklabel_format(axis='y', style='sci', scilimits=(-7, -6))
axs[1].set_ylabel(r"$K\cdot Re(\chi)$")
axs[1].set_xlabel("Temperature/K")

fig.subplots_adjust(hspace=0)
plt.savefig(r"../figure/E1_chi_temp.png", dpi=450, transparent=True)
plt.show()
