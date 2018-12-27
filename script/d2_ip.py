# -*- encoding: utf8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset

__author__ = 'Tian'

data = np.genfromtxt("../data/da2_ip.csv", delimiter=',')

current = data[1:, 0]
power = data[1:, 2]

p = np.polyfit(current[:-13:1], power[:-13:1], 1)

i = np.linspace(13, current[0]+1)
fit = np.polyval(p, i)

ith = -p[1]/p[0]

plt.style.use("classic")
ax = plt.gca()
ax.set_title("Current-Power Graph", fontsize=16)
ax.set_xlabel("current/mA", fontsize=14)
ax.set_ylabel("Power/W", fontsize=14)
ax.scatter(current, power, color='green', label="Data", alpha=0.7, s=10)
ax.plot(i, fit, linestyle='--', label="Linear Fit", linewidth=1)
ax.scatter(ith, 0, s=40, alpha=1.)
ax.set_xlim(xmin=0)
ax.set_ylim(ymin=0)
ax.legend()

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.ticklabel_format(axis='y', style='sci', scilimits=(-1, -2))

axins = zoomed_inset_axes(ax, zoom=14, loc=6)
axins.scatter(current, power, color='green', label="Data", alpha=0.7, s=10)
axins.plot(i, fit, linestyle='--', label="Linear Fit", linewidth=1)
axins.scatter(ith, 0, s=40, alpha=1.)
x1, x2, y1, y2 = 12.5, 14.4, 0, 0.0006
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.yaxis.set_ticks_position('right')
axins.xaxis.set_ticks_position('bottom')
axins.ticklabel_format(axis='y', style='sci', scilimits=(-3, -5))
axins.set_xticks([13, ith, 14])
axins.spines["bottom"].set_position("zero")

mark_inset(ax, axins, loc1=3, loc2=4, fc="none", ec="0.5")


plt.savefig('../figure/d2_ip_zoomed.eps')
plt.show()
