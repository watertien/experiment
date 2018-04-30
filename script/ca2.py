#! bin/python3
# -*- encoding: utf8 -*-
__author__ = 'Tian'
import numpy as np
import matplotlib.pyplot as plt

light_voltage = np.array([2.3, 2.5, 2.8, 2.9])
data = np.zeros(light_voltage.size)
fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.set_xlabel("$U_{G2K}/V$", fontsize=12)
ax.set_ylabel("$I/10^{-7}A$", fontsize=12)
ax.set_title("U-I Graph", fontsize=14)
for j in light_voltage:
    data = np.genfromtxt("../data/light_{0}.csv" .format(j), delimiter=',')
    ax.plot(data[1:, 0] * 100, data[1:, 1] , label=r"$V_l={0}V$" .format(j), marker='^')

plt.legend()
plt.show(fig)
