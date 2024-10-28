import numpy as np
import matplotlib.pyplot as plt

colors = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02']

files = ["results_2023-08.dat", "results-2023-12.dat", "results_2024-02.dat",
        "results_2024-10_master.dat", "results_2024-10_test_branch.dat"]
labels = ["08/2023", "12/2023-Ankerl", "02/2024", "master", "test branch"]
markers = ["o", "^", "s", "<", ">"]

for i, f in enumerate(files):
    x, t = np.loadtxt(f, skiprows=1, unpack=True)
    plt.plot(x, t / 60, '--', marker=markers[i], label=labels[i],
             color=colors[i])

plt.xlabel("number of cores")
plt.ylabel("Simulation time [min]")
plt.legend()
plt.savefig("results.png", dpi=300)
plt.show()
