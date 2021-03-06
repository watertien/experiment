import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

__author__ = "Tian"


def reciprocal(x, x0, sigma, c, a):
    return c - a * np.exp( -(1/(x) - 1/(x0))**2 / (2 * sigma**2))


def doppler_aborption(x, x0, sigma, c, a):
    return c - a * np.exp( -((x) -(x0))**2 / (2 * sigma**2))


def cutter(event):
    """
    Remove a range of data given bounds
    """
    x0 = int(event.xdata)
    xs.append(x0)
    event.inaxes.axvline(x0, alpha=.1, linestyle='--')
    mask = np.zeros_like(foo, dtype="bool_")

    if(len(xs) == 4):
        # Curve fitting for doppler-absorption range
        mask[xs[-2]:xs[-1]] = True
        mask[xs[0]:xs[1]] = False

        # Calibration of ILD/Power (Baseline)
        baseline_k = (ch1[xs[-1]] - ch1[xs[-2]] ) / (xs[-1] - xs[-2]) # slope of baseline
        baseline_p = np.poly1d([baseline_k, ch1[xs[-1]] - baseline_k * xs[-1]])
        baseline_cali = baseline_p(foo[mask])
        
        # Gaussian curve fitting 
        fit_x = event.inaxes.lines[0].get_xdata()[mask]
        fit_y = event.inaxes.lines[0].get_ydata()[mask] / baseline_cali
        p0 = [273, 1e2, 1.2, 1e-1]
        popt, pcov = curve_fit(doppler_aborption, fit_x, fit_y, sigma=np.ones_like(fit_x) * yerr,\
                p0=p0, absolute_sigma=True, maxfev=2000)
        fitting_result = np.vstack((popt, pcov))

        # Create x data for plot fitting result
        _bar = np.linspace(xs[-2], xs[-1])
        bar = doppler_aborption(_bar, *popt)

        wls = k * (data[:,1] - data[int(popt[0]),1]) + center_wl
        wls = wls.flatten()
        # print(foo.shape, wls.shape)
        dwl = k * (data[int(popt[0]+popt[1]*1.17741)+1,1] - data[int(popt[0]-popt[1]*1.17741)-1,1])
        # print(wls, int(popt[0]+popt[1]/1.17741)+1, int(popt[0]-popt[1]/1.17741)-1,\
        #         data[int(popt[0]+popt[1]/1.17741)+1,1] - data[int(popt[0]-popt[1]/1.17741)-1,1])

        # event.inaxes.axvline(int(popt[0]), alpha=.1, c='g', linestyle='--')
        event.inaxes.plot(_bar, bar, color='blue', linewidth=4, alpha=.6, label="Gaussian Fitting")
        event.inaxes.text(0, 0.9, f"mean:{popt[0]:.4f} sigma:{abs(popt[1]):.4f}")
        event.inaxes.text(0, 0.8, r"$\Delta\nu=$"+f"{abs(3e8*dwl /center_wl**2):.4f}GHz")
        event.inaxes.plot(foo[mask], baseline_cali, color='grey', linewidth=2, ls='-.', alpha=.6, label="Baseline")
        event.inaxes.plot(fit_x, fit_y, color='black', linewidth=2, marker='s', ls=' ', alpha=.3, \
                markersize=2, label="With Baseline Calibration")
        event.inaxes.set_xticklabels(wls.astype("|U9"))
        event.inaxes.set_xlabel("Wavelength/nm")
        event.inaxes.set_xlim(auto=True)

        # with open("../data/fitting_result.csv", 'ab') as save:
        #     np.savetxt(save, xs, delimiter=',')
        plt.legend(loc='best')
        plt.savefig("../figure/E4_Li7D2_Fitting_wavelength.png", dpi=450, transparent=True)
    event.canvas.draw()
        

if __name__ == "__main__":
    fname = r"..\data\refined_670999_Li7D2.csv"
    xs = []
    data = np.loadtxt(fname, delimiter=',', )
    foo = np.arange(len(data[:,0]))
    yerr = 1.007 - 0.955 # A rough estimate of sigma_y
    ch1 = data[:,0]
    k = -1.08e-3
    center_wl = 670.951 # Wavelength for Li7D2

    fig, ax = plt.subplots(figsize=(13, 5))
    # ax.set_title("Select doppler-free range")
    ax.set_title("Li7D2 Doppler-Absorption Curve Fitting")
    ax.set_ylabel("Voltage/V")
    fig.canvas.set_window_title(fname)
    ax.plot(ch1, marker='o', markersize=3, alpha=.3, linestyle=' ', color='red', label="Experiment data")
    # ax.plot(data[:,1], marker='o', markersize=3, alpha=.3, linestyle=' ', color='black', label="PZT Volatge")
    cid = fig.canvas.mpl_connect("button_press_event", cutter)
    plt.show()    
    fig.canvas.mpl_disconnect(cid)

