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
syms = ["^","o","s", ">","*"]
labels = ["Q1","Q2","Q3", "Q4","Q5"]

# Error vs Time

fig = plt.figure()
ax = fig.add_subplot(111) # Create plot object
ax.set_yscale('log')
ax.set_xscale('log')
plt.ylabel('$\Vert e \Vert_2 $')
plt.xlabel('Simulation time [s]')
for i in range(0,len(sys.argv)-1):

    fname = sys.argv[i+1]

    #Input file
    print ("R-> %s" %fname)
    mat = numpy.loadtxt(fname,skiprows=1,usecols=(1,3))
    uL2E=mat[:,0]
    time=mat[:,1]
    ax.plot(time,uL2E,"-"+syms[i],label=labels[i])

ax.legend()
plt.tight_layout()
if (outputPNG): plt.savefig("./L2Error-vs-Timing.png",dpi=300)
if (outputPDF): plt.savefig("./L2Error-vs-Timing.pdf")
if (showGraphic): plt.show()

# Time vs Error

fig = plt.figure()
ax = fig.add_subplot(111) # Create plot object
ax.set_yscale('log')
ax.set_xscale('log')
plt.xlabel('$\Vert e \Vert_2 $')
plt.ylabel('Simulation time [s]')
for i in range(0,len(sys.argv)-1):

    fname = sys.argv[i+1]

    #Input file
    print ("R-> %s" %fname)
    mat = numpy.loadtxt(fname,skiprows=1,usecols=(1,3))
    uL2E=mat[:,0]
    time=mat[:,1]
    ax.plot(uL2E,time,"-"+syms[i],label=labels[i])

ax.legend()
plt.tight_layout()
if (outputPNG): plt.savefig("./Timing-vs-L2Error.png",dpi=300)
if (outputPDF): plt.savefig("./Timing-vs-L2Error.pdf")
if (showGraphic): plt.show()


