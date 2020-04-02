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
outputPDF=True
outputPNG=True
showGraphic=True
width=8
height=5

# Modify font of the graphic
font = {'weight' : 'normal',
        'size'   : 18}
plt.rc('font', **font)
plt.rcParams['legend.numpoints'] = 1
params = {'backend': 'ps',
             'axes.labelsize': 20,
             'text.fontsize': 20,
             'legend.fontsize': 16,
             'xtick.labelsize': 14,
             'ytick.labelsize': 14,
             'text.usetex': True,
             }
plt.rcParams.update(params)

colors=['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02']

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

fig = plt.figure(figsize=(width,height))
#fig = plt.figure()
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
    #color = next(ax._get_lines.prop_cycler)['color']
    ax.plot(dx,uL2E,syms[i],color=colors[i],label=labels[i] + ' - $\Vert e_{\mathbf{u}}\Vert_{2}$')
    ax.plot(dx,numpy.exp(b)*dx**a,'-',color=colors[i],label="$\mathcal{O} (\Delta x^{%3.1f})$" %(a))

#ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
#          ncol=4, fancybox=True, shadow=True)
ax.legend(ncol=2, fancybox=True,columnspacing=0.2, handletextpad=0.3,labelspacing=0.2)#, bbox_to_anchor=(0.5,0.7)
plt.ylim([1e-11,1e+3])
plt.tight_layout()
if (outputPNG): plt.savefig("./L2_error_all.png",dpi=300)
if (outputPDF): plt.savefig("./L2_error_all.pdf")
if (showGraphic): plt.show()


# Time vs Error
fig = plt.figure(figsize=(width,height))
#fig = plt.figure()
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
    ax.plot(uL2E,time,"-"+syms[i],label=labels[i],color=colors[i])

ax.grid(b=True, which='minor', color='grey',alpha=0.5, linestyle='--')
ax.grid(b=True, which='major', color='k', linestyle='-')
ax.legend()
plt.tight_layout()
if (outputPNG): plt.savefig("./timing_vs_L2_error.png",dpi=300)
if (outputPDF): plt.savefig("./timing_vs_L2_error.pdf")
if (showGraphic): plt.show()


