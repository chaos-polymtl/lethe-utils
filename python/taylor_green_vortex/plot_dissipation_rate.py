###########################################################
# File : plot_dissipation_rate.py
#---------------------------------------------------------
# Plots the dissipation rate from the kinetic energy
# and from the enstrophy and compares them with a
# solution
###########################################################


import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Arguments for calculation of the dissipation rate')
parser.add_argument("-ke", "--kinetic_rate", type=str, help="Name of the input file for kinetic energy dissipation rate", required=True)
parser.add_argument("-ens", "--enstrophy", type=str, help="Name of the input file for the enstrophy", required=True)

parser.add_argument("-v", "--viscosity", type=float, help="viscosity", required=True)
args, leftovers=parser.parse_known_args()

viscosity=args.viscosity
fname_ke=args.kinetic_rate
fname_ens=args.enstrophy

prefix_ref="/reference/jacobs_rateE_256.dat"
fname_ref=os.path.dirname(os.path.realpath(__file__))+prefix_ref

t_ike,ike=np.loadtxt(fname_ke,skiprows=1,unpack=True)
t_ens,ens=np.loadtxt(fname_ens,skiprows=1,unpack=True)
t_ref,ref=np.loadtxt(fname_ref,skiprows=1,unpack=True)

ens=ens*viscosity*2 


plt.plot(t_ike,ike,label="Kinetic energy dissipation")
plt.plot(t_ens,ens,label="Enstrophy energy dissipation")
plt.plot(t_ref,ref,label="Reference")
plt.legend()

plt.show()
