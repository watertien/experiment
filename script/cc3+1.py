import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("../data/cc3+1.csv", delimiter=',')
meter1 = data[0, :]
meter2 = data[1, :]
meter3 = data[2, :]
meter4 = data[3, :]

#p = np.polyfit(meter1, meter4, 1)
#pa = np.poly1d(p)
foo = np.linspace(0, meter1[-1] + 0.1, 100)
#bar = pa(foo)

ax = plt.gca()
line1, = ax.plot(meter1, meter2, marker='^', alpha=0.4)
line2, = ax.plot(foo, foo, alpha=0.4)
ax.set_title("Microscope-Micrometer Caliper")
ax.set_xlabel("Replacement/mm")
ax.set_ylabel("Voltage/V")
#ax.legend(prop={"size": 14})
ax.text(1, 3, "y=x")

plt.savefig("../figure/cc3+3.png")
