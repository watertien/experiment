#! bin/python3
# -*- encoding: utf8 -*-
__author__ = 'Tian'
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

T = np.arange(40, 110, 10)
D = np.arange(150, 450, 50) - 45
Tm = []
Vm = []
for i in D:
    data = pd.read_excel("../data/{0}mm-100C-02sil.xlsx" .format(i), index_col=0)
    Tm.append(data.iloc[:, 0].mean())
    Vm.append(data.iloc[:, 2].mean())

np.savetxt("../data/cc1+.distance-voltage.02sil.csv", (D, Vm), delimiter=',')
