import numpy as np
import matplotlib.pyplot as plt


colors=['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02']

files=["results_2023-08.dat","results-2023-12.dat", "results_2024-02.dat" ]
labels=["08/2023", "12/2023-Ankerl", "02/2024"]
markers=["o", "^", "s"]

for i,f in enumerate(files):
    t,x = np.loadtxt(f,skiprows=1,unpack=True)
    plt.plot(t,x/60,'--',marker=markers[i],label=labels[i],color=colors[i])

plt.xlabel("number of cores")
plt.ylabel("Simulation time [min]")
plt.legend()
plt.savefig("results.png",dpi=300)
plt.show()
