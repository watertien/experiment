#! bin/python3
# -*- encoding: utf8 -*-
__author__ = 'Tian'
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

increase = pd.read_excel("../data/increase.xlsx", index_col=0)
decrease = pd.read_excel("../data/decrease.xlsx", index_col=0)

plt.style.use("experiment")
ax = plt.gca()
line1, = ax.plot(increase.iloc[:, 0]+273.15, increase.iloc[:, 2]*10**5,
                 color='red', marker='s', markersize=2, alpha=0.5, label='Temperature Increase')
line2, = ax.plot(decrease.iloc[:, 0]+273.15, decrease.iloc[:, 2]*10**5,
                 color='blue', marker='o', markersize=2, alpha=0.5, label='Temperature Decrease')
diff = ax.annotate(r"$\Delta U \approx 1.6\times 10^{-5}$V", (316., 16.6), (317, 14.5), xycoords="data",
                   textcoords="data", arrowprops={"arrowstyle": "->"})
ax.legend(prop={"size": 14})
ax.set_xlabel("Temperature/K")
ax.set_ylabel("Sensor Output/$10^{-5}$V")
ax.set_title("Temperature-Voltage")
plt.savefig("../figure/cc1+two_compare.png")
