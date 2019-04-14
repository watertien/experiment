# -*- encoding: utf8 -*-
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'Tian'


def laser_intensity(f, sigma=1):
    return 1 * np.exp(-(f-f0)**2/2/sigma**2)


def airy_dis(f, finesse=200):
    return 1 / (1 + finesse/2 * np.sin(2 * np.pi * f )**2)


f0 = 20 * 1.e3
df = f0/10.
laser_frequency = np.linspace(-df, df, 1000) + f0

plt.plot(laser_frequency, laser_intensity(laser_frequency, sigma=10) * airy_dis(laser_frequency))
plt.plot(laser_frequency, airy_dis(laser_frequency))
plt.show()