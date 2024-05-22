# -*- coding: utf-8 -*-

import numpy as np
import argparse
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import os 
from tc_functions import *


#Plot font and colors
font = {'weight' : 'normal',
        'size'   : 13}

plt.rc('font', **font)
colors=['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02']

#Parameter of the simulation 
class parameter(): 
    re = 1.0          #Outer radius
    ri = 0.5          #Inner radius
    kappa = 0.5       #Radius ratio (ri/re)
    omega = 1.0       #Angular velocity (rad/s)
    d = 0.5           #Width of the annulus (re - ri)
    alpha = 2*np.pi   #Aspect ratio (L/d)
    nu = 6.25e-5      #Kinematic viscosity
    rho = 1.0         #Fluid density 
    Re = 4000         #Reynolds number

prm = parameter() 

### Simulations data ###
parser = argparse.ArgumentParser(description='Arguments for calculation of the kinetic energy')
parser.add_argument("-kin", "--kinetic_energy", type=str, help="Name of the input file for the kinetic energy", required=True)
parser.add_argument("-l", "--legend", type=str, help="Legend label", required=False)
args, leftovers=parser.parse_known_args()
fname_kin=args.kinetic_energy
leg = args.legend


t_1, kin = np.loadtxt(fname_kin,skiprows=1,unpack=True)
plt.plot(t_1,kin,'k', label = leg,lw=2)
plt.xlabel("Time [-]")
plt.ylabel("Kinetic energy [-]")
#plt.legend(loc = 'lower right')
plt.show()
