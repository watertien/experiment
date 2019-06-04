import matplotlib.pyplot as plt
import numpy as np
import glob



def smooth(arr, span=4):
    smoothed = np.zeros(arr.shape)
    length = arr.size
    for i in range(span, length):
        # For ndarray, when use arr slicing as
        # function arguements, out of length is valid
        # and doesn't influence sum or mean operation
        # But when (i-4) is less than zero, slicing will
        # return an empty array that will cause RuntimeWarrning for mean function
        # but the sum(both built-in and np.sum) will return zero
        # So, for the very first elements of arr, 
        # just call max function to return a non-empty array
        # and call min function for the tail elements of array
        smoothed[i] = np.mean(arr[min(i+4, length):max(i-4, 0):-1])
    return smoothed    


files = [r"..\data\refined_671_Li6D1.csv", r"..\data\refined_671012_Li7D1_Li6D2.csv",\
         r"..\data\refined_670999_Li7D2.csv"]
arr = []

for f in files:
    data = np.genfromtxt(f, delimiter=',')
    n0, n1 = np.argmin(data[:,1]), np.argmax(data[:,1])
    arr.extend(data[n0:n1,0])

fig, ax = plt.subplots(figsize=(15, 4))
ax.plot(arr, 'r+', markersize=4, alpha=.2)
plt.rcParams.update({'font.size': 14})
ax.set_xlabel("Time Index")
ax.set_ylabel("PD Voltage Signal")
ax.set_title("50%Li-6,50%Li-7 Absorption Line(After concatenation)")
plt.savefig("../figure/E4_aborption_concatenate.png", dpi=450, transparent=True)
plt.show()

