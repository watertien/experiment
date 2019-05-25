# -*- encoding: utf8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import BSpline, make_interp_spline

__author__ = 'Tian'

fname = "../data/E1_chi_different_G_record.xlsx"
# col_name = ['R', 'temp', 'B', 'X', 'Y', 'theta', 'freq', 'noise']
col_name = ['temp', 'B', 'R', 'theta', 'I']
data = pd.read_excel(fname, delimiter='\t', names=col_name, skiprows=[0])
data = data.sort_values('temp')
data["R"] = data.R.values * 1e-6
data["theta"] = data.theta.values * np.pi / 180
data["X"] = data.R.values * np.cos(data.theta.values)
data["Y"] = data.R.values * np.sin(data.theta.values)
# data = data.loc[:56000,:]
magnetic = np.array([1., 2., 3., 3.5])
current = np.array([2., 4, 6, 7])

foo = np.linspace(85, 92.0)

# Background phase difference
bg_phase = -155.48 * np.pi / 180 # Unit: radian
bg_phase_right = (-155.48 + 90) * np.pi / 180 # Unit: radian
bg_x = [np.cos(bg_phase), -np.cos(bg_phase)]
bg_y = [np.sin(bg_phase), -np.sin(bg_phase)]
bg_x_right = [np.cos(bg_phase_right), -np.cos(bg_phase_right)]
bg_y_right = [np.sin(bg_phase_right), -np.sin(bg_phase_right)]

fig, axs = plt.subplots(figsize=(8,8), nrows=2, ncols=1, sharex=True)
cs = ["b", 'y', 'g', 'r']
lines = []

for c, field, _current in zip(cs, magnetic, current):
    # fix_b = data[abs(data.B + field) < 0.3].copy(deep=True)
    fix_b = data[data.I == _current].copy(deep=True)
    # with pd.ExcelWriter(f"../data/E1_chi_{field}kG_refined.xlsx") as writer:
    #     fix_b.to_excel(writer)
    # Caused by non-ideal and non-symmetry coils
    non_ideal_coils = np.copy(np.mean(fix_b[["X", "Y"]][fix_b.temp == max(fix_b.temp)]))
    # Remove non-ideal term
    points_offset = fix_b[["X", "Y"]] - non_ideal_coils
    # Get Re and Im parts
    points_re = np.sum(points_offset * np.array([bg_x_right[0], bg_y_right[0]]), axis=1)
    points_im = np.sum(points_offset * np.array([bg_x[0], bg_y[0]]), axis=1)

    spl = make_interp_spline(fix_b.temp, points_im, k=2)
    im_spline = spl(foo)
    spl = make_interp_spline(fix_b.temp, points_re, k=2)
    re_spline = spl(foo)
    lines.append(axs[0].plot(fix_b.temp, points_im,\
                'o', color=c, markersize=5, alpha=.6, label=f'B={field:.1f}kG')[0] )
    axs[0].plot(foo,im_spline, '-', color=c, alpha=.3)

    axs[1].plot(fix_b.temp, points_re,\
                'o', color=c,markersize=5, alpha=.6, label=f'B={field:.1f}kG')
    axs[1].plot(foo,re_spline, '-', color=c, alpha=.3)
# fname = "../data/E1_chi_0G.xls"
# data0 = pd.read_csv(fname, delimiter='\t', names=col_name, skiprows=[0, 1])
# data0 = data0.loc[:50000,:]
#
# # Caused by non-ideal and non-symmetry coils
# non_ideal_coils = np.copy(np.mean(data0[["X", "Y"]][data0.temp == max(data0.temp)]))
# # Remove non-ideal term
# points_offset = data0[["X", "Y"]] - non_ideal_coils
# # Get Re and Im parts
# points_re = np.sum(points_offset * np.array([bg_x_right[0], bg_y_right[0]]), axis=1)
# points_im = np.sum(points_offset * np.array([bg_x[0], bg_y[0]]), axis=1)
#
# axs[0].plot(data0.temp, points_im ,'o', alpha=.1, markersize=3, label='B=0.0kG')
# axs[1].plot(data0.temp, points_re ,'o', alpha=.1, markersize=3, label='B=0.0kG')

axs[0].set_ylabel(r"$K\cdot Im(\chi)$")
axs[0].set_title(r"$\chi$-T under Different DC Magnetic Field", pad=30.0, fontsize=15)
axs[0].ticklabel_format(axis='y', style='sci', scilimits=(-7, -6))

axs[1].ticklabel_format(axis='y', style='sci', scilimits=(-7, -6))
axs[1].set_ylabel(r"$K\cdot Re(\chi)$")
axs[1].set_xlabel("Temperature/K")

axs[1].set_xlim(85, 92.5)
axs[0].legend(lines, [i.get_label() for i in lines], ncol=4,\
           markerscale=2, loc="upper right", bbox_to_anchor=(0.89,1.14), shadow=True)

fig.subplots_adjust(hspace=0)
plt.savefig(r"../figure/E1_chi_different_G_record_refined.png", dpi=450, transparent=True)
# plt.show()
