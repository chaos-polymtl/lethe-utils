import numpy as np
import matplotlib.pyplot as plt

colors = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02']

files = ["results_2024-10_master.dat","results_2024-10_master_10000_lb.dat", "results_2024-10_master_10000_lb_1000_pw.dat"]
labels = ["master", "LB: 10 000", "LB: 10 000 + PW: 1000" ]
markers = ["o", "^", "s", "<", ">"]

for i, f in enumerate(files):
    x, t = np.loadtxt(f, skiprows=1, unpack=True)
    print(t)
    plt.plot(x, t / 60, '--', marker=markers[i], label=labels[i],
             color=colors[i])

plt.xlabel("number of cores")
plt.ylabel("Simulation time [min]")
plt.legend()
plt.savefig("results.png", dpi=300)
plt.show()
