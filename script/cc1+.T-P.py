#! bin/python3
# -*- encoding: utf8 -*-
__author__ = 'Tian'
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_excel("../data/increase.xlsx", index_col=0)
data.columns = ["Temperature", "Actual Power", "Voltage", "Ni1000"]

T = data.iloc[:, 0]
P = data.iloc[:, 1]
V = data.iloc[:, 2]

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.plot(T, V * 10**5, marker='o', alpha=0.4, linewidth=4, color="#9932CC", label="Voltage Output")
ax.set_xlabel(r"Temperature/$^{\circ}$C", fontsize=14)
ax.set_ylabel(r"Sensor Output/$10^{-5}$V", fontsize=14)
ax.set_title(r"Temperature-Voltage", fontsize=16)
plt.show()
