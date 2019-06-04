import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from scipy.optimize import curve_fit

def power_broadening(x, isat, nuh):
    return (1 + x / isat)**0.5 * nuh


fname = r"..\data\doppler_free_fitting_result.csv"

names = ['dv1', 'dv2', 'dv3', 'sigma1', 'sigma2', 'sigma3', 'power']
df = pd.read_csv(fname, names=names, comment='#')
df = df.sort_values("power")
# print(df)
foo = np.linspace(df.power[0], df.power[-1])

popt, pcov = curve_fit(power_broadening, df.power, df.dv1, p0=[0.5, 0.1], sigma=df.sigma1, maxfev=2000)
bar = power_broadening(foo, *popt)
print(popt)

fig, axs = plt.subplots(figsize=(7, 12), nrows=3, ncols=1, sharex=True, sharey=True)
axs[-1].set_xlabel("Laser Power/mW")
axs[-1].set_ylabel("FWHM/GHz")

axs[0].errorbar(df.power, df.dv1, yerr=df.sigma1, fmt='.r', ls=' ', capsize=5, label=r"$\Delta\nu_1$")
axs[0].plot(foo, bar)

axs[1].errorbar(df.power, df.dv2, yerr=df.sigma2, fmt='.b', ls=' ', capsize=5, label=r"$\Delta\nu_2$")

popt, pcov = curve_fit(power_broadening, df.power, df.dv3, p0=[0.5, 0.1], sigma=df.sigma3, maxfev=2000)
bar = power_broadening(foo, *popt)
print(popt)

axs[2].errorbar(df.power, df.dv3, yerr=df.sigma3, fmt='.k', ls=' ', capsize=5, label=r"$\Delta\nu_3$")
axs[2].plot(foo, bar)

fig.subplots_adjust(hspace=0)
fig.legend()
axs[0].set_title("Power Broadening")
plt.show()

