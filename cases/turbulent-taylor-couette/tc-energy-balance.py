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
    re = 1.0                       #Outer radius
    ri = 0.5                       #Inner radius
    kappa = 0.5                    #Radius ratio (ri/re)
    omega = 1.0                    #Angular velocity (rad/s)
    d = 0.5                        #Width of the annulus (re - ri)
    alpha = 2*np.pi                #Aspect ratio (L/d)
    nu = 6.25e-5                   #Kinematic viscosity
    rho = 1.0                      #Fluid density 
    Re = 4000                      #Reynolds number
    vol = np.pi*np.pi*re*2 - np.pi*np.pi*ri**2 # volume

prm = parameter() 

skip=2

### Simulations data ###

#Load enstrophy file
parser = argparse.ArgumentParser(description='Arguments for calculation of the dissipation rate')
parser.add_argument("-ens", "--enstrophy", type=str, help="Name of the input file for the enstrophy", required=True)
parser.add_argument("-kin", "--kinetic_energy", type=str, help="Name of the input file for the Kinetic Energy", required=True)
parser.add_argument("-t", "--torque", type=str, help="Name of the input file for the Torque", required=True)
parser.add_argument("-p", "--pressure", type=str, help="Name of the input file for the pressure work", required=True)

parser.add_argument("-l", "--legend", type=str, help="Legend label", required=False)
args, leftovers=parser.parse_known_args()
fname_ens=args.enstrophy
fname_kin=args.kinetic_energy
fname_torque=args.torque
fname_pressure=args.pressure



t_1, e = np.loadtxt(fname_ens,skiprows=skip,unpack=True)
t_2, kin = np.loadtxt(fname_kin,skiprows=skip,unpack=True)
t_3, tx,ty,tz = np.loadtxt(fname_torque,skiprows=skip,unpack=True)
t_4, p = np.loadtxt(fname_pressure,skiprows=skip,unpack=True)

size=np.min([len(t_1),len(t_2),len(t_3)])

e = e * prm.nu
dkin_dt = np.copy(kin)
dkin_dt[1:-1] = (kin[2:] - kin[0:-2])/ (t_2[-1]-t_2[-2])
dkin_dt[0] = (kin[1]-kin[0]) / (t_2[1]-t_2[0])
dkin_dt[-1] = (kin[-1]-kin[-2]) / (t_2[-1]-t_2[-2])

torque_power = tz[:size]*prm.omega/prm.vol/np.pi

plt.plot(t_1[:size],e[:size], label="Enstrophy")
plt.plot(t_2[:size],dkin_dt[:size], label="Kinetic energy decay")
plt.plot(t_3[:size],torque_power[:size], label="Torque")
plt.plot(t_4[:size],p[:size], label="Pressure")

#plt.plot(t_1[:size],dkin_dt[:size]+torque_power[:size]+e[:size]+p[:size], label="Sum")
plt.plot(t_1[:size],-(dkin_dt[:size]+torque_power[:size]+e[:size]+p[:size]), label="Implicit viscosity")


plt.xlabel("Time [-]")
plt.ylabel("Enstrophy [-]")
plt.legend(loc = 'lower right')

plt.show()