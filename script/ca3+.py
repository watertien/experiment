#! bin/python3
# -*- encoding: utf8 -*-
__author__ = 'Tian'
import numpy as np
import matplotlib.pyplot as plt

#  plt.style.use("grayscale")
ax = plt.gca()
for i, j in enumerate([0, 0.02, 0.04, 0.06, 0.08, 0.1, 1]):
    filename = "../data/{0}g_withoutbackground.csv" .format(j)
    data = np.genfromtxt(filename, delimiter=',')
    ax.scatter(data[:-3, 0], data[:-3, 1], s=4, marker='o', alpha=0.4, label="{0}g/L" .format(j))

ax.set_ylim(0, 1500)
ax.set_xlabel("Wavelength/nm", fontsize=14)
ax.set_ylabel("Relative Intensity", fontsize=14)
ax.set_title("$\lambda$-Intensity", fontsize=16)
ax.legend(prop={"size": 16})
plt.show()
