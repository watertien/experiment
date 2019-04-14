# -*- encoding: utf8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

__author__ = 'Tian'


def interference():
    data = np.genfromtxt(r"../data/e2_interference.csv", delimiter=',')
    a_polar = data[:, 1]
    a_polar_norm = data[:, 1] / np.linalg.norm(a_polar)
    a_nonpolar = data[:-2, 2]
    theta = (data[:, 0] - data[0, 0]) * 2
    bar = np.linspace(0, 180, 100)
    a_nonpolar_norm = data[:-2, 2] / np.linalg.norm(a_nonpolar)

    ax = plt.gca()
    ax.plot(theta, a_polar_norm, marker='s', alpha=.6, label="A with PP")
    ax.plot(bar, np.max(a_polar_norm) * cos_square(bar), label=r"$cos^2{\theta}$")
    # ax.plot(theta[:-2], a_nonpolar_norm , marker='o', alpha=.6, label="A without PP")
    ax.set_xlim(0,)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_position(("data", 0))
    ax.legend()
    ax.set_title("Angle-Count")
    ax.set_xlabel(r"$\theta/^{\circ}$")
    ax.set_ylabel("Normalized Photon Counts in 10s")
    ax.set_xticks(range(0, 181, 45))

    plt.show()


def cos_square(x):
    return np.cos(x * np.pi / 180)**2


def chsh():
    data = np.genfromtxt("../data/e2_chsh.csv", delimiter=',')
    total_count = np.sum(data)
    win_count = 2188 + 2038 + 1890 + 1893 + 2026 + 1999 + 1756 + 1290
    print(f"probability of winning: {win_count/total_count:.5F}")

if __name__ == "__main__":
    interference()
