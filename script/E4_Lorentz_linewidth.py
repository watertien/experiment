# -*- encoding: utf8 -*-
mport numpy as np
import matplotlib.pyplot as plt

__author__ = 'Tian'

nu0 = 100
gamma = 20
nu = np.linspace(-5, 5, 10000) * gamma + nu0


def lorentz_profile(frequency):
    return 1 / (1 + 4 * (frequency - nu0)**2 / gamma**2) # + 1 / (1 + 4 * (frequency - nu0/2)**2 / gamma**2)


def func_diff(f, x, h):
    return ( f(x + h / 2) - f(x - h / 2)) / h


def lorentz_differential(frequency):
    return 1 / (1 + 4 * (frequency - nu0)**2 / gamma**2)**2 * 8 / gamma**2 * (nu0 - frequency) 
#            + 1 / (1 + 4 * (frequency - nu0/2)**2 / gamma**2)**2 * 8 / gamma**2 * (nu0/2 - frequency)


def division(event):
    sub_range.append(event.xdata)

lineshape = lorentz_profile(nu)
sub_range = []
hm = max(lineshape) / 2 # Half maximum
fw = nu0 + np.array([-1,1]) * gamma/2 # Full width
extreme = nu0 + np.array([-1,1]) * gamma/12**0.5
fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 6))
axs[0].set_xlim(nu[0], nu[-1])
axs[0].plot(nu, lineshape, 'k-', label="Lorentz Linshape")
axs[0].plot(fw, [hm, hm], 'r--')
axs[1].plot(nu, lorentz_differential(nu), 'b-', label="Differential Line")
# axs[1].plot(fw, lorentz_differential(fw), 'ro', markersize=6)
axs[1].plot(extreme, lorentz_differential(extreme), 'yo', markersize=6)
axs[1].set(xlabel="Frequency/Hz", ylabel="Relative Intensity")
fig.legend()

fig.subplots_adjust(hspace=0)
cid = fig.canvas.mpl_connect("button_press_event", division)
plt.savefig("../figure/E4_Lorentz.png", dpi=450, transparent=True)
plt.show()


peakx = []
peaky = []
for i in range(len(sub_range) - 1):
    range_index = np.logical_and(nu > sub_range[i], nu < sub_range[i+1])
    peakx.extend([nu[range_index][np.argmax(lorentz_differential(nu[range_index]))],\
            nu[range_index][np.argmin(lorentz_differential(nu[range_index]))]])
    peaky.extend([np.max(lorentz_differential(nu)[range_index]), \
             np.min(lorentz_differential(nu)[range_index])])

print(peakx, extreme)

