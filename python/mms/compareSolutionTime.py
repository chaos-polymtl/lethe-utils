#!/usr/bin/python3
# This program makes the plot for L2 error of two series of data 

# Author : Bruno Blais

#Python imports
import os
import sys
import numpy
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FormatStrFormatter
import pylab
from scipy import stats
from matplotlib import rcParams


# User parameter
outputPDF=False
outputPNG=True
showGraphic=True


# Modify font of the graphic
font = {'weight' : 'normal',
        'size'   : 18}
plt.rc('font', **font)
plt.rcParams['legend.numpoints'] = 1
params = {'backend': 'ps',
             'axes.labelsize': 24,
             'text.fontsize': 28,
             'legend.fontsize': 17,
             'xtick.labelsize': 15,
             'ytick.labelsize': 15,
             'text.usetex': True,
             }
plt.rcParams.update(params)


#================================
# FUNCTIONS
#================================

def rsquared(x, y):
    """ Return R^2 where x and y are array-like."""
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return r_value**2

#================================
# MAIN PROGRAM
#================================
syms = ["^","o","s", ">"]
labels = ["ILU-GMRES/AMG-GMRES"]
fig = plt.figure()
ax = fig.add_subplot(111) # Create plot object
#ax.set_yscale('log')
ax.set_xscale('log')
plt.ylabel('$t_{AMG-GMRES}/t_{ILU-GMRES}$')
plt.xlabel('Number of DOFs')

assert(len(sys.argv)==3)
fnameGMRES= sys.argv[1]
fnameAMG  = sys.argv[2]

#Input file
print ("R-> %s" %fnameGMRES)
matGMRES = numpy.loadtxt(fnameGMRES)
timeGMRES=matGMRES[:,2]
nxGMRES=4*(2**matGMRES[:,0])**3
matAMG = numpy.loadtxt(fnameAMG)
timeAMG=matAMG[:,2]
nxAMG=matAMG[:,0]**2.

ax.plot(nxGMRES,timeGMRES/timeAMG,"-"+syms[0],label=labels[0])
ax.plot([nxGMRES[0],nxGMRES[-1]], [1,1], "k--")
ax.legend()
plt.tight_layout()
if (outputPNG): plt.savefig("./AMG-GMRES.png",dpi=300)
if (showGraphic): plt.show()

