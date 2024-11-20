import numpy as np
import matplotlib.pyplot as plt




colors = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02']

from cycler import cycler

colors=['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02']

plt.rcParams['axes.prop_cycle'] = cycler(color = colors)
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['figure.figsize'] = (10,8)
plt.rcParams['lines.linewidth'] = 4
plt.rcParams['lines.markersize'] = '11'
plt.rcParams['markers.fillstyle'] = "none"
plt.rcParams['lines.markeredgewidth'] = 2
plt.rcParams['legend.columnspacing'] = 2
plt.rcParams['legend.handlelength'] = 3
plt.rcParams['legend.handletextpad'] = 0.2
plt.rcParams['legend.frameon'] = True
plt.rcParams['legend.fancybox'] = False
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['font.size'] = '25'
plt.rcParams['font.family']='DejaVu Serif'
plt.rcParams['font.serif']='cm'
plt.rcParams['savefig.bbox']='tight'
plt.rcParams['legend.handlelength']=1

files = ["results_2024-11_master_2.dat"]
labels = ["LB: 10_000 + PW: 10_000","LB: 10_000 + PW: 2_000" ]
markers = ["o", "^", "s", "<", ">"]


# Create the plot
fig, ax1 = plt.subplots()
ax2 = ax1.twiny()

for i, f in enumerate(files):
    x, t = np.loadtxt(f, skiprows=1, unpack=True)
    print(t)
    # Plot the primary y-axis
    ax1.plot(x, t / 60, '--', marker=markers[i], label=labels[i],
             color=colors[i])

# Customize the first y-axis
ax1.set_xlabel("Number of cores")
ax1.set_ylabel("Simulation time [min]")
ax1.set_ylim([0, 650])

new_tick_location = np.array([40,80,120,160,200])

ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(new_tick_location)
ax2.set_xticklabels(np.array(new_tick_location/40,dtype=int))
ax2.set_xlabel("Number of nodes")

#plt.savefig("results.png", dpi=300)
plt.show()
