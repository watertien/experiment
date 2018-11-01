import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import proton_mass
from scipy.optimize import curve_fit
from scipy.constants import Avogadro
from scipy.constants import atomic_mass as m_atom
__author__ = 'Tian'
plt.style.use("experiment")


def plot1():
    ax = plt.gca()
    markers = ['*', 's', '^']
    resolution = [1.40, 1.46, 1.22]
    time = [5, 30, 90]
    for i in range(3):
        data = np.genfromtxt("../data/241Am_100V_{0}s_1024.txt" .format(time[i]),
                             delimiter=r'\n')
        data = normalization(data)
        ax.scatter(np.arange(data.size), data, marker=markers[i],
                   s=2, alpha=0.8,
                   label="T={0}s, Energy Resolution={1}%" .format(time[i], resolution[i]))
    ax.set_title("Different Measure Interval")
    ax.set_xlabel("Channel Address")
    ax.set_ylabel("Particle Count")
    ax.set_xlim(0, 1024)
    ax.set_ylim(0, 0.07)
    ax.legend(markerscale=3)
    plt.savefig("../figure/da4_1.png")


def normalization(a):
    return a/np.sum(a)


def plot2(a):
    title = ["Voltage-Channel Graph", "Voltage-Resolution Graph"]
    ytitle = ["Peak Channel", "Resolution/%"]
    name = ["Peak", "Resolution"]
    data = np.genfromtxt("../data/d4-offset-address-resolution.csv", delimiter=',')
    popt, prov = curve_fit(my_fit, data[:, 0], data[:, 2])
    foo = my_fit(data[:, 0], *popt)
    print(popt)
    # ax = plt.gca()
    # ax.scatter(data[:, 0], data[:, a+1], marker='o', s=10, alpha=0.8, label="Original Data")
    # ax.plot(data[:, 0], foo, linewidth=2, alpha=0.5,
    #         label=r"Curve Fit: $y={:.0f}-{:.0f}log({:.0f}+{:.2f}x)$" .format(*popt))
    # ax.set_xlabel("Offset Voltage/V")
    # ax.set_ylabel(ytitle[a])
    # ax.set_title(title[a])
    # ax.legend()
    # plt.savefig("../figure/d4_2_{0}_fit.png" .format(name[a]))
    # plt.show()


def calibration():
    x = [871.55, 923.01]
    y = np.array([5.155, 5.486]) * 10**3   # Energy Unit: keV
    p1 = np.polyfit(x, y, 1)
    p = np.poly1d(p1)
    return p


def thickness(a):
    # Input energy unit: keV
    p = calibration()
    init_energy = p(923.01)  # Energy Unit: keV
    penetrated_energy = p(np.array([561.75, 689.50]))
    print("Incident Energy: {}\nPenetrate Energy: {}  {}" .format(init_energy, *penetrated_energy))
    d_energy = init_energy - penetrated_energy
    coefficient = np.array([[2.5, 0.625, 45.7, 0.1, 4.359],  # Al
                           [4.232, 0.3877, 22.99, 35, 7.993],   # C
                           [0.9661, 0.4126, 6.92, 8.831, 2.582],  # H
                           [1.776, 0.5261, 37.11, 15.24, 2.804]])  # O
    rho = np.array([2.7, 1.38])
    atomic_mass = np.array([12, 1, 16])
    mylar_chemistry = np.array([10, 8, 4])
    molecule_mass = np.array([27, np.sum(atomic_mass*mylar_chemistry)])
    n_density = rho/(m_atom * 10**3 * molecule_mass)/10**15  # Unit: 10^15/cm3
    print("Density: {:e}" .format(n_density[a]))
    mylar_density = np.array([1.136, 5.376, 5.376]) * 10**(23-15)
    de = 0  # The substance dE/dx value, unit: eV/cm
    if a == 1:
        a_c = np.sum(atomic_mass * mylar_chemistry)
        atom_sigma = np.array([mylar_chemistry[i] * atomic_mass[i] * sigma2de(coefficient[i+1],
                                                                              mylar_density[i], energy=init_energy)
                               for i in range(3)])
        de = 1/a_c * np.sum(atom_sigma)  # dE/dx Mylar
    elif a == 0:
        de = sigma2de(coefficient[0], n_density[a], energy=init_energy)  # dE/dx Aluminum
    print("dE/dx = {:e}" .format(de))
    return d_energy[a] * 10**3 / de   # Unit: cm


def rho2n(density):
    # The density unit is g/cm3
    # return unit is 10^15 atoms/cm2
    return density/(m_atom * 27)/10**15


def sigma2de(arr, n, energy=5*10**3):
    # energy unit: keV
    c1 = arr[0] * energy**arr[1]
    c2 = arr[2]/(energy/1000)
    c3 = np.log(1 + arr[3]/(energy/1000) + arr[4]*energy/1000)
    print("Sigma_e = {0}" .format(c1 * c2 * c3 / (c1 + c2*c3)))
    sigma_e = c1 * c2 * c3 / (c1 + c2*c3)  # Unit: ev/10^15(atoms) cm2
    return sigma_e * n  # return unit: eV/cm


def my_fit(x, a, b, c, d):
    return a - b * np.log(c + d * x)


def guassian_fit(filename, fit_function):
    data = np.genfromtxt(filename, delimiter=',')
    fit_data = data[np.nonzero(data)]
    x = np.arange(fit_data.size)
    y_sigma = 1/fit_data
    propt, prov = curve_fit(fit_function, x, fit_data, sigma=y_sigma, absolute_sigma=False)
    print("The fitting parameters are:\n{:.2f} exp(-(x-{:.2f})^2/{:.2f})" .format(*propt))
    foo = gaussian(x, *propt)
    plt.title("Gaussian Curve Fit")
    plt.xlabel("Channel Address")
    plt.ylabel("Particle Count")
    plt.scatter(x, fit_data, label="Data", s=2.5)
    plt.plot(x, foo, label="Curve Fit", linewidth=1, alpha=0.7)
    plt.text(50, 200, r"{:.2f} exp(-(x-{:.2f})^2/{:.2f})" .format(*propt), fontsize=14)
    plt.legend(loc="best")
    # plt.savefig("../figure/d6_GaussianFit_2.png")
    plt.show()


def gaussian(x, a, b, c):
    return a * np.exp(-(x-b)**2/c)


if __name__ == "__main__":
    # plot1()
    # plot2(1)
    # p = calibration()
    # print(p)
    # print("initial: {}, end: {}" .format(p(923.01), p(561.75)))
    thickness1 = thickness(0)
    print("Thickness = {:E}" .format(thickness1))
    # guassian_fit("../data/241Am_80V_103s_1024.txt", gaussian)
