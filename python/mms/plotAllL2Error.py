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

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111) # Create plot object
ax.set_yscale('log')
ax.set_xscale('log')
plt.ylabel('$\Vert e \Vert_2 $')
plt.xlabel('$\Delta x^{-1}$')
ax.grid(b=True, which='minor', color='grey', linestyle='--')
ax.grid(b=True, which='major', color='k', linestyle='-')

for i in range(0,len(sys.argv)-1):
    fname = sys.argv[i+1]
    #Input file
    print ("R-> %s" %fname)
    mat = numpy.loadtxt(fname,skiprows=1, usecols=(0, 1))
    n=mat[:,0]
    uL2E=mat[:,1]
    dx=(n)**0.5
    a,b = numpy.polyfit(numpy.log(dx),numpy.log(uL2E),1)
    color = next(ax._get_lines.prop_cycler)['color']
    ax.plot(dx,uL2E,syms[i],color=color,label='$\Vert e_{\mathbf{u}}\Vert_{2}$')
    ax.plot(dx,numpy.exp(b)*dx**a,'-',color=color,label="$\mathcal{O} (\Delta x^{%3.2f})$" %(a))

#ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
#          ncol=4, fancybox=True, shadow=True)
ax.legend(ncol=2, fancybox=True, bbox_to_anchor=(0.5,0.7))
plt.tight_layout()
if (outputPNG): plt.savefig("./L2ErrorAll.png",dpi=300)
if (outputPDF): plt.savefig("./L2ErrorAll.pdf")
if (showGraphic): plt.show()

