#!/usr/bin/python3
# This program makes the plot for L2 error of two series of data

# Author : Bruno Blais

#Python imports
import os
import sys
import numpy as np
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
# MAIN PROGRAM
#================================
syms = ["^","o","s", ">"]

prefix="proc_"
suffix=".dat"
nprocs=7
time=np.zeros([9,nprocs])

for i in range(0,nprocs):
    fname = prefix + str(i+1) + suffix
    print ("R-> %s" %fname)
    mat = np.loadtxt(fname)
    time[:,i]=mat[:,2]
    if(i==0) : dofs=mat[:,0]

fig = plt.figure()
ax = fig.add_subplot(111) # Create plot object
time[8,1:] = time[8,1:]/1.12
ax.plot(1+np.arange(nprocs),time[8,0]/time[8,:],syms[0],markerfacecolor="None",markeredgewidth=3,label="$n_{DOF}=12M$")
ax.plot(1+np.arange(nprocs),time[7,0]/time[7,:],syms[1],markerfacecolor="None",markeredgewidth=3,label="$n_{DOF}=3.1M$")
ax.plot(1+np.arange(nprocs),time[6,0]/time[6,:],syms[2],markerfacecolor="None",markeredgewidth=3,label="$n_{DOF}=790K$")
#ax.set_yscale('log')

plt.ylabel('Speedup')
plt.xlabel('Number of processors')

#ax.plot(dx,uL2E,'ko',label='$\Vert e_{\mathbf{u}}\Vert_{2}$')
#ax.plot(dx,numpy.exp(b)*dx**a,'-k',label='$\Vert e_{\mathbf{u}}\Vert_{2}=%3.2f  \Delta x^{%3.2f}$' %(numpy.exp(b),a))

ax.legend(loc="best")

plt.tight_layout()
if (outputPNG): plt.savefig("./scalup.png",dpi=300)
if (showGraphic): plt.show()
