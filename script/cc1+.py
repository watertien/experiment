#! bin/python3
# -*- encoding: utf8 -*-
__author__ = 'Tian'
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as dates
myFmt = dates.DateFormatter("%H:%M:%S")


data = pd.read_excel("../data/increase.xlsx", index_col=0)
data.columns = ["Temperature", "Actual Power", "Voltage", "Ni1000"]

#  Plot ax Temperature
ax = plt.gca()
line1 = ax.plot_date(data.index, data.iloc[:, 0], marker="o", color="red", label="Temperature")
ax.xaxis.set_major_formatter(myFmt)
ax.set_ylabel(r"Temperature/$^{\circ}$C", fontsize=14)
ax.set_title("Temperature Decrease", fontsize=14)
ax.set_xlabel("Time", fontsize=14)

ax1 = ax.twinx()
ax1.set_ylabel("Power/W", fontsize=14)
line2 = ax1.plot_date(data.index, data.iloc[:, 1], color="blue", marker="^", markersize=2, alpha=0.3, label="Supply Power")

lines_set = [line1[0], line2[0]]
ax.legend(lines_set, [i.get_label() for i in lines_set], prop={"size": 16})

plt.show()
