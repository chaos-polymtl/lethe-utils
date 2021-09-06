#!/usr/bin/python3
# This program makes the plot for L2 error of two series of data

# Author : Bruno Blais

#Python imports
import os
import sys
import numpy as np
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
symbols = ["o", "s", "^", "*"]




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

#folder="uniform_refinement"
folder="uniform_refinement"
fnames =["/torque.00.dat","/torque_solid.dat"]
labels= ['Outer cylinder','Inner cylinder']
mssize=8
lwidth=2

k=0.25
mu=1
R=1
Omega=1
torque_ana = 4*np.pi*mu*Omega*R**2*1*(k**2/(1-k**2))
print(torque_ana)
fig = plt.figure(figsize=[7.47,6.5])

ax = fig.add_subplot(111) # Create plot object
ax.set_yscale('log')
ax.set_xscale('log')
plt.ylabel('$\Vert e \Vert_2 $')
plt.xlabel('$\Delta x = N_{cells}^{1/2}$')
ax.grid(b=True, which='minor', color='grey', linestyle='--')
ax.grid(b=True, which='major', color='k', linestyle='-')

for i,f in enumerate(fnames):
#Input file
    print ("R-> %s" %f)
    mat = np.loadtxt(folder+f,skiprows=1)
    n=mat[:,0]
    torque=mat[:,3]
    torque_err = np.abs(torque -torque_ana) / np.abs(torque_ana)
    dx=(n)**0.5
    ax.plot(dx,torque_err,'ko')
    # Linear regression
    a,b = np.polyfit(np.log(dx),np.log(torque_err),1)
    ax.plot(dx,torque_err,symbols[i],color=colors[i],label=labels[i],ms=mssize)
    ax.plot(dx,np.exp(b)*dx**a,'-',lw=lwidth,color=colors[i],label='$\Vert e_{\mathbf{T}}\Vert_{2}=%3.2f  \Delta x^{%3.2f}$' %(np.exp(b),a))

    print ('A u    = ', a)
    print ('R^2 u  = ', rsquared(np.log(dx),np.log(torque_err)))


ax.legend(loc=1)



plt.tight_layout()
if (outputPNG): plt.savefig(folder+"-L2Error.png",dpi=300)
if (outputPDF): plt.savefig(folder+"-L2Error.pdf")
if (outputTIKZ):
    tikzplotlib.clean_figure()
    tikzplotlib.save("L2_error_torque_taylor_couette.tex",axis_height='9cm', axis_width='11cm')
if (showGraphic): plt.show()

