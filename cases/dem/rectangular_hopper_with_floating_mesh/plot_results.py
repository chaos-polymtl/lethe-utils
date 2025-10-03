import numpy as np
import argparse 
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import MaxNLocator


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

files = ["results_2024-11_master_pw_2k.dat",]
labels = ["PW: 2_000", ]
markers = ["o", "^", "s", "<", ">"]


# Create the plot
fig, ax1 = plt.subplots()
ax2 = ax1.twiny()

parser = argparse.ArgumentParser(
    description="Read a list of files from the command line."
)

parser.add_argument(
    "-f", "--files",
    metavar="FILE",
    type=str,
    nargs="+",   # one or more files
    required=True,
    help="List of input files"
)

parser.add_argument(
    "-l", "--labels",
    metavar="LABEL",
    type=str,
    nargs="+",   # one or more labels
    required=True,
    help="List of input files"
)

args = parser.parse_args()

for i, f in enumerate(args.files):
    x, t = np.loadtxt(f, skiprows=1, unpack=True)
    print(t)
    # Plot the primary y-axis
    ax1.plot(np.array(x,dtype=int), t / 60, '-', marker=markers[i], label=args.labels[i],
             color=colors[i])

# Customize the first y-axis
ax1.legend()
ax1.set_xlabel("Number of nodes")
ax1.set_ylabel("Simulation time [min]")
ax1.set_ylim([0, 1200])
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))


new_tick_location = np.array([1, 2, 3, 4, 5, 10, 15,20])
new_tick_labels = [f"{2*tick}" for tick in new_tick_location]
print(new_tick_labels)

ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(new_tick_location)
ax2.set_xticklabels(new_tick_labels)

# Adjust the padding between the x-axis label and the axis
ax2.set_xlabel(r"Number of particles $\cdot 10^6$", labelpad=10)  # Use labelpad to adjust padding


# Optionally, adjust title padding for the second x-axis
#ax2.set_title("Number of particles $\cdot 10^6$", pad=10)

plt.tight_layout()
plt.savefig("results.png", dpi=300)
plt.show()
