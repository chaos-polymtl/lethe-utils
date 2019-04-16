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

fname = sys.argv[1]

#Input file
print ("R-> %s" %fname)
nx, uL2E, pL2E = numpy.loadtxt(fname, unpack=True)

dx=2**nx
fig = plt.figure()

ax = fig.add_subplot(111) # Create plot object
ax.plot(dx,uL2E,'ko')

ax.set_yscale('log')
ax.set_xscale('log')

plt.ylabel('$\Vert e \Vert_2 $')
plt.xlabel('$\Delta x^{-1}$')

# Linear regression
a,b = numpy.polyfit(numpy.log(dx),numpy.log(uL2E),1)
ap,bp = numpy.polyfit(numpy.log(dx),numpy.log(pL2E),1)

ax.grid(b=True, which='minor', color='grey', linestyle='--')
ax.grid(b=True, which='major', color='k', linestyle='-')

ax.plot(dx,uL2E,'ko',label='$\Vert e_{\mathbf{u}}\Vert_{2}$')
ax.plot(dx,numpy.exp(b)*dx**a,'-k',label='$\Vert e_{\mathbf{u}}\Vert_{2}=%3.2f  \Delta x^{%3.2f}$' %(numpy.exp(b),a))

ax.plot(dx,pL2E,'ks',label='$\Vert e_{\mathbf{p}}\Vert_{2}$')
ax.plot(dx,numpy.exp(bp)*dx**ap,'-k',label='$\Vert e_{\mathbf{p}}\Vert_{2}=%3.2f  \Delta x^{%3.2f}$' %(numpy.exp(bp),ap))

ax.legend(loc=2)

print ('A velocity    = ', a)
print ('R^2 velocity  = ', rsquared(numpy.log(dx),numpy.log(uL2E)))
print ('A pressure    = ', ap)
print ('R^2 pressure  = ', rsquared(numpy.log(dx),numpy.log(pL2E)))

if (outputPDF): plt.savefig("./L2Error.pdf")
if (showGraphic): plt.show()

