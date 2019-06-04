import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

__author__ = "Tian"


def doppler_free(x, x1, g1, a1, x2, g2, a2, x3, g3, a3, b):
    lorentz1 = a1 * (x - x1) / g1**2 * ( 8 / (1 + 4 * (x - x1)**2/g1**2))
    lorentz2 = a2 * (x - x2) / g2**2 * ( 8 / (1 + 4 * (x - x2)**2/g2**2))
    lorentz3 = a3 * (x - x3) / g3**2 * ( 8 / (1 + 4 * (x - x3)**2/g3**2))
    return b + (lorentz1 + lorentz2 + lorentz3)


def cutter(event):
    """
    Remove a range of data given bounds
    """
    x0 = int(event.xdata)
    xs.append(x0)
    event.inaxes.axvline(x0, alpha=.1, linestyle='--')
    mask = np.zeros_like(foo, dtype="bool_")

    if(len(xs) == 3):
        # Curve fitting for doppler-absorption range
        mask[:] = True
        # mask[xs[0]:xs[1]] = False

        """
        # Calibration of ILD/Power (Baseline)
        baseline_k = (ch1[xs[-1]] - ch1[xs[-2]] ) / (xs[-1] - xs[-2]) # slope of baseline
        baseline_p = np.poly1d([baseline_k, ch1[xs[-1]] - baseline_k * xs[-1]])
        baseline_cali = baseline_p(foo[mask])
        """
        
        # Gaussian curve fitting 
        fit_x = event.inaxes.lines[0].get_xdata()[mask]
        fit_y = event.inaxes.lines[0].get_ydata()[mask] 

        g_fit = 1
        p0 = np.array([xs[-3], g_fit, 1, xs[-2], g_fit, 10, xs[-1], g_fit, 1.0, .1])
        limits = np.array([[xs[-3]-10, 0, -5e-1, xs[-2]-10, 0, 0, xs[-1]-10, 0, -5e-1, -3],\
                            [xs[-3]+10, 10, 0, xs[-2]+10, 10, 5, xs[-1]+10, 10, 0, 3]])
        p0 = [xs[-3], g_fit, -2e-2, xs[-2], g_fit, 1, xs[-1], g_fit,  -2e-2, .1]

        popt, pcov = curve_fit(doppler_free, fit_x, fit_y, sigma=np.ones_like(fit_x) * yerr,\
                p0=p0, absolute_sigma=True, bounds=limits, maxfev=2000)
        print(popt)
        print(pcov)
        fitting_result = np.vstack((popt, pcov))

        # Create x data for plot fitting result
        _bar = np.linspace(foo[0], foo[-1], 1000)
        bar = doppler_free(_bar, *popt)

        x1, g1, a1, x2, g2, a2, x3, g3, a3, b = popt
        k = (wl1 - wl2) / (foo[int(x1)] - foo[int(x2)])
        wls = k * (data[:,0] - data[int(x1),1]) + wl1 # Unit: nm/samplingperiod
        wls = wls.flatten()
        # print(foo.shape, wls.shape)
        dwl = k * np.array([g1, g2, g3])
        # print(wls, int(popt[0]+popt[1]/1.17741)+1, int(popt[0]-popt[1]/1.17741)-1,\
        #         data[int(popt[0]+popt[1]/1.17741)+1,1] - data[int(popt[0]-popt[1]/1.17741)-1,1])

        # event.inaxes.axvline(int(popt[0]), alpha=.1, c='g', linestyle='--')
        event.inaxes.plot(_bar, bar, color='blue', linewidth=4, alpha=.6, label="Difference Lineshape Fitting")
        # event.inaxes.text(0, 0.9, f"mean:{popt[0]:.4f} sigma:{abs(popt[1]):.4f}")
        # event.inaxes.text(0.1, 0.6, r"$\Delta\nu=$"+f"{abs(3e8*dwl /center_wl**2):.4f}GHz", transform=ax.transAxes)
        # event.inaxes.plot(foo[mask], baseline_cali, color='grey', linewidth=2, ls='-.', alpha=.6, label="Baseline")
        # event.inaxes.plot(fit_x, fit_y, color='black', linewidth=2, marker='s', ls=' ', alpha=.3, \
        #         markersize=2, label="With Baseline Calibration")
        event.inaxes.set_xticklabels(wls.astype("|U9"))
        event.inaxes.set_xlabel("Wavelength/nm")
        # event.inaxes.set_xlim(auto=True)

        with open("../data/doppler_free_temp_fitting_result.csv", 'a') as save:
             save.write(fname[8:-4]+',')
             dnu = abs(3e8*dwl /center_wl**2).reshape((1,-1))
             sigma_nu = np.sqrt(np.diag(pcov))[1::3].reshape((1,-1)) * abs(k) * 3e8 / center_wl**2 
             _save = np.concatenate((dnu, sigma_nu), axis=1)
             np.savetxt(save, _save, delimiter=',', newline="\n")
        plt.legend(loc='best')
        # plt.savefig("../figure/E4_Doppler_free_Fitting_wavelength.png", dpi=450, transparent=True)
    event.canvas.draw()
        

if __name__ == "__main__":
    for i in [320, 326, 330, 340, 350, 371]:
        fname = r"..\data\refined_E4_temp_" + str(i) + ".csv"
        xs = []
        data = np.loadtxt(fname, delimiter=',', )
        foo = np.arange(len(data[:,0]))
        yerr = np.mean(data[:40,1]**2)**0.5 # A rough estimate of sigma_y
        ch1 = data[:,1]
        k = -1.08e-3
        center_wl = 670.951 # Wavelength for Li7D2
        wl2 = 670.9503971408603
        wl1 = 670.9516028602232

        fig, ax = plt.subplots(figsize=(13, 5))
        # ax.set_title("Select doppler-free range")
        ax.set_title("Li7D2 Doppler-Free Curve Fitting")
        ax.set_ylabel("Voltage/V")
        fig.canvas.set_window_title(fname)

        data_line = ax.plot(ch1, marker='o', markersize=3, alpha=.3, linestyle=' ', color='red', label="Experiment data")
        # ax.plot(data[:,0], marker='o', markersize=3, alpha=.3, linestyle=' ', color='black', label="PZT Volatge")
        cid = fig.canvas.mpl_connect("button_press_event", cutter)
        plt.show()    
        fig.canvas.mpl_disconnect(cid)
    """
    fname = r"..\data\refined_E4_temp_" + "350"  + ".csv"
    xs = []
    data = np.loadtxt(fname, delimiter=',', )
    # data[:,1] = -data[:,1]
    foo = np.arange(len(data[:,0]))
    yerr = np.mean(data[:40,1]**2)**0.5 # A rough estimate of sigma_y
    ch1 = data[:,1]
    k = -1.08e-3
    center_wl = 670.951 # Wavelength for Li7D2
    wl2 = 670.9503971408603
    wl1 = 670.9516028602232

    fig, ax = plt.subplots(figsize=(13, 5))
    # ax.set_title("Select doppler-free range")
    ax.set_title("Li7D2 Doppler-Free Curve Fitting")
    ax.set_ylabel("Voltage/V")
    fig.canvas.set_window_title(fname)

    data_line = ax.plot(ch1, marker='o', markersize=3, alpha=.3, linestyle=' ', color='red', label="Experiment data")
    # ax.plot(data[:,0], marker='o', markersize=3, alpha=.3, linestyle=' ', color='black', label="PZT Volatge")
    cid = fig.canvas.mpl_connect("button_press_event", cutter)
    plt.show()    
    fig.canvas.mpl_disconnect(cid)
    """
