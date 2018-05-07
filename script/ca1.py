import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt("../data/ca1.tian.csv", delimiter=',')
q = data[-1, 1:]
e = 1.602  # charge of an electron unit: x 10^-19 C
n = np.round(q / e)
#  temp = n[:4]
#  n[3] = (n[3] + n[4]) / 2
#  n = temp
#  q = q[:4]
p = np.polyfit(n, q, 1)
poly = np.poly1d(p)
foo = np.linspace(n.min() - 0.2, n.max() + 0.2)
bar = poly(foo)

plt.style.use("grayscale")
fig = plt.figure(1)
ax = fig.add_subplot(111)

#  Plot scatters
scatter = ax.scatter(n, q, alpha=0.3, marker=r"$\otimes$", label="Original Data", s=200)
#  Plot linear fit line
line = ax.plot(foo, bar, label="Linear Fit")
#  Set x and y axis
ax.set_xlabel("n(Multiple of e)", fontsize=14)
ax.set_ylabel(r"Charge/$10^{-19}$C", fontsize=14)
ax.set_title("Linear Fit of n-q Graph", fontsize=16)
ax.legend()
#  Print slope of the line
#  Double curly brace to prevent .format parsing "-19"
ax.text(4.5, 5, r"Result={0:.3f}$\times10^{{-19}}$C" .format(p[0]))
plt.show(fig)
