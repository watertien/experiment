#! bin/python3
# -*- encoding: utf8 -*-
__author__ = 'Tian'
import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("../data/cc3.csv", delimiter=',')
m1 = data[:2, :]
m2 = data[2:, :-1]
m2 = m2[:, np.argsort(m2[0, :])]


def n2A(n):
    n_theta = 100
    return n /(2 * n_theta)


m1[1:, ] = n2A(m1[1:, ])
m2[1:, ] = n2A(m2[1:, ])

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.set_xlabel("frequency/Hz", fontsize=14)
ax.set_ylabel("Amplitude/mm", fontsize=14)
ax.set_title("f-A Graph", fontsize=16)
line1 = ax.plot(m1[0, :], m1[1, :], marker='^', label="$m_1$")
line2 = ax.plot(m2[0, :], m2[1, :], marker='o', label="$m_2$")
ax.legend(prop={"size": 16})
plt.show()
