# -*- encoding: utf8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
import pandas as pd

__author__ = 'Tian'

fname = "../data/E1_chi_0G.xls"
col_name = ['R', 'temp', 'B', 'X', 'Y', 'theta', 'freq', 'noise']
data = pd.read_csv(fname, delimiter='\t', names=col_name, skiprows=[0, 1])
data = data.loc[:50000,:]

bg_phase = -155.48 * np.pi / 180 # Unit: radian
bg_phase_right = (-155.48 + 90) * np.pi / 180 # Unit: radian
bg_x = [np.cos(bg_phase), -np.cos(bg_phase)]
bg_y = [np.sin(bg_phase), -np.sin(bg_phase)]
bg_x_right = [np.cos(bg_phase_right), -np.cos(bg_phase_right)]
bg_y_right = [np.sin(bg_phase_right), -np.sin(bg_phase_right)]

fig, ax = plt.subplots(figsize=(8,8))
_norm = Normalize(vmin=60, vmax=94)
points = ax.scatter(data.X, data.Y, c=data.temp, cmap="hot", s=6, alpha=.4, norm=_norm)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_position(("data", 0))
ax.spines["bottom"].set_position(("data", 0))
ax.xaxis.set_major_locator(MaxNLocator(4))
ax.yaxis.set_major_locator(MaxNLocator(4))
ax.ticklabel_format(axis='x', style='sci', scilimits=(-6, -5))
ax.ticklabel_format(axis='y', style='sci', scilimits=(-6, -5))
ax.set_xlabel("X/V")
ax.set_ylabel("Y/V")
ax.set_title(r"$\Delta \epsilon$ on Phase-Plane", fontsize=15, pad=20)
ax.set_xlim(-4e-6, 2e-5)
ax.set_ylim(-3e-6, 2e-5)
ax.set_aspect("equal")

# Plot bg phase
# ax.plot(bg_x, bg_y, 'r--', bg_x_right, bg_y_right, 'b--')
# ax.text(8e-6, 3e-6, r"$\theta = \phi_1 - \phi_0$")

axins = zoomed_inset_axes(ax, zoom=2, loc=9)
axins.scatter(data.X, data.Y, alpha=0.7, s=10, c=data.temp, cmap="hot", norm=_norm)
x1, x2, y1, y2 = -1e-6, .3e-6, 12e-6, 17e-6
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.yaxis.set_ticks_position('right')
axins.xaxis.set_ticks_position('bottom')
axins.ticklabel_format(axis='y', style='sci', scilimits=(-6, -5))
axins.ticklabel_format(axis='x', style='sci', scilimits=(-5, -5))
# axins.spines["left"].set_position(("data", 0))

mark_inset(ax, axins, loc1=2, loc2=3, fc="none", ec="0.5")

cbar = fig.colorbar(points)
cbar.ax.set_ylabel("Temperature/K")
# plt.savefig("../figure/E1_chi_transition_0G.png", dpi=450, transparent=True)
plt.show()
