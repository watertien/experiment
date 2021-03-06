#! bin/python3
# -*- encoding: utf8 -*-
__author__ = 'Tian'
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as dates
myFmt = dates.DateFormatter("%H:%M")


data1 = pd.read_excel("../data/decrease.xlsx", index_col=0)
data1.columns = ["Temperature", "Actual Power", "Voltage", "Ni1000"]


#  Plot ax Temperature
ax = plt.gca()
line1 = ax.plot_date(data1.index, data1.iloc[:, 0], marker="o", color="red", label="Temperature")
ax.xaxis.set_major_formatter(myFmt)
ax.set_ylabel(r"Temperature/$^{\circ}$C", fontsize=14)
ax.set_title("Temperature Increase", fontsize=16)
ax.set_xlabel("Time", fontsize=14)

ax1 = ax.twinx()
ax1.set_ylabel("Power/W", fontsize=14)
line2 = ax1.plot_date(data1.index, data1.iloc[:, 1], color="blue",
                      marker="^", markersize=2, alpha=0.2, label="Supply Power")

lines_set = [line1[0], line2[0]]
ax.legend(lines_set, [i.get_label() for i in lines_set], prop={"size": 16})

plt.savefig("../figure/cc1+_pid_decrease.svg")
