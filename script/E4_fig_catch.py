import glob
import numpy as np
import matplotlib.pyplot as plt

__author__ = "Tian"


def wave_viewer(title):
    data = np.loadtxt(title, delimiter=',', skiprows=2, usecols=(0,1))
    ch1 = data[:,0]
    ch2 = data[:,1]
    fig, ax = plt.subplots(figsize=(10, 2))
    fig.canvas.set_window_title(title)
    ax.plot(ch1, marker='o', markersize=3, alpha=.4, linestyle=' ', color='red')
    ax.plot(ch2, marker='s', markersize=3, alpha=.4, linestyle=' ', color='blue')
    cid = fig.canvas.mpl_connect("button_press_event", cutter)
    return fig, ax, cid
    

def cutter(event):
    """
    Cut mulitiple periods into one single range and save it
    """
    x0 = int(event.xdata)
    xs.append(x0)
    event.inaxes.axvline(x0)
    event.canvas.draw()
    if(len(xs) % 2 == 0):
        print(xs)
        ch1_partial = event.inaxes.lines[0].get_ydata()[xs[-2]:xs[-1]]
        ch2_partial = event.inaxes.lines[1].get_ydata()[xs[-2]:xs[-1]]
        foo = np.vstack((ch1_partial, ch2_partial)).T
        np.savetxt("refined_"+event.canvas.get_window_title(), foo, delimiter=',')
        

if __name__ == "__main__":
    files = glob.glob("../data/E4_67*.csv")
    xs = []
    for fname in files:
        fig, ax, cid = wave_viewer(fname)
    plt.show()    

