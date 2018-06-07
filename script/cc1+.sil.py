#! bin/python3
# -*- encoding: utf8 -*-
__author__ = 'Tian'
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

T = np.arange(40, 110, 10)
for i in T:
    data = pd.read_excel("../data/196mm-{0}C-02.xlsx" .format(i), index_col=0)
