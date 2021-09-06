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
from scipy import stats
from matplotlib import rcParams
import tikzplotlib


# User parameter
outputTIKZ=True
outputPDF=False
outputPNG=False
showGraphic=True
colors=['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02']
#plt.style.use("ggplot")
#plt.rcParams['lines.linewidth']=3
#plt.rcParams['axes.facecolor']='w'
plt.rcParams['legend.numpoints'] = 1
#plt.rcParams['xtick.minor.visible'] = True
#plt.rcParams['xtick.minor.width'] = 2

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

fnames = ["uniform_refinement/L2Error.dat","dynamic_mesh_0.5/L2Error.dat", "dynamic_mesh_0.3/L2Error.dat"]
label= ["Uniform", "Kelly - $\epsilon=0.5$", "Kelly - $\epsilon=0.3$"]
symbols = ["o", "s", "^", "*"]
mssize=8
lwidth=2

#nx, uL2E = numpy.loadtxt(fname, unpack=True)

fig = plt.figure(figsize=[7.47,6.5])
#fig = plt.figure()

ax = fig.add_subplot(111) # Create plot object

ax.set_yscale('log')
ax.set_xscale('log')
ax.set_ylim([1e-4,1e-1])
#ax.set_xlim([1e-2,2e-1])

plt.ylabel('$\Vert e \Vert_2 $')
plt.xlabel('$N_{cells}^{1/2}$')

for i,f in enumerate(fnames):
    print ("R-> %s" %f)
    mat = numpy.loadtxt(f,skiprows=1, usecols=(0, 1))
    n=mat[:,0]
    uL2E=mat[:,1]
    dx=(n)**0.5
    a,b = numpy.polyfit(numpy.log(dx),numpy.log(uL2E),1)
    ax.plot(dx,uL2E,symbols[i],color=colors[i],label='$\Vert e_{\mathbf{u}}\Vert_{2}$ '+ label[i],ms=mssize, alpha=0.8)
    ax.plot(dx,numpy.exp(b)*dx**a,'--',color=colors[i],lw=lwidth,label='$\Vert e_{\mathbf{u}}\Vert_{2}=%3.2f  \Delta x^{%3.2f}$' %(numpy.exp(b),a))

ax.grid(b=True, which='minor', color='grey', linestyle='-')
ax.grid(b=True, which='major', color='k', linestyle='-')

ax.legend(loc=1)

print ('A u    = ', a)
print ('R^2 u  = ', rsquared(numpy.log(dx),numpy.log(uL2E)))

plt.tight_layout()
if (outputPNG): plt.savefig("./L2Error.png",dpi=1000)
if (outputPDF): plt.savefig("./L2Error.pdf")
if (outputTIKZ):
    tikzplotlib.clean_figure()
    tikzplotlib.save("L2_error_taylor_couette.tex",axis_height='9cm', axis_width='11cm')
if (showGraphic): plt.show()


