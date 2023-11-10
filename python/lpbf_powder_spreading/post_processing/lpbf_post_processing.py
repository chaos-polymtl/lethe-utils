#############################################################################
"""
Postprocessing automation tool.

By: Olivier Gaboriault
Date: October 30th, 2023
"""
#############################################################################
'''Importing Libraries'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append("../lethe/lethe/contrib/postprocessing/")
from lethe_pyvista_tools import *

#############################################################################
'''Simulation properties'''

#Take case path as argument
prm_file_names = np.array(["lpbf_0100_0100_22_000_ALUM","lpbf_0100_0100_22_100_ALUM","lpbf_0100_0100_22_500_ALUM"])  # ./parameter.prm -->  lpbg_LayerHeight_BladeSpeed_NumberOfLayers_DomainLength_Alloy.prm
color = np.array(["blue","red","green","cyan","yellow"])
plt.figure(figsize=(10,6))

#Loop over a
for i in range(len(prm_file_names)):
    # Create the particle object
    prm_file_name = prm_file_names[i]
    pvd_name = 'out.pvd'
    ignore_data = ['type', 'volumetric contribution', 'velocity', 'torque', 'fem_torque', 'fem_force']
    particle = lethe_pyvista_tools(".", prm_file_name, pvd_name, ignore_data=ignore_data)
#############################################################################

    # Variables from the title of the .prm file
    delta_o          = float(prm_file_name[18:21]) * (10 ** -6)
    delta_n          = 100 * (10 ** -6)
    GAP              = 500 * ()
    layer_height     = float(prm_file_name[5:9]) * (10 ** -6)
    blade_speed      = float(prm_file_name[10:14]) * (10 ** -3)
    number_of_layers = int(prm_file_name[15:17])

    # Bluid plate domain
    # This string could be use to isolate the start and the end of the build plate (not for now)
    input_string = particle.prm_dict["initial translation"]
    x_min = float(input_string[2].split(',')[0])     # --> This is the X translation of solid object #2
    x_max = float(input_string[3].split(',')[0])     # --> This is the X translation of solid object #3

    # Lenght of the domain
    input_string = particle.prm_dict["grid arguments"].split(',')
    domain_x_length = float(input_string[4].split(':')[1])   # This is the dealii triangulation in X
    domain_z_length = float(input_string[6].split(':')[0])   # This is the dealii triangulation in Z
    build_plate_length = x_max - x_min
    build_plate_area = domain_z_length * build_plate_length

    # How much time it takes for a blade to move throw all the domain
    # This will help to find the starting time of each blade, thus the mesuring time we should use
    blade_time_per_layer = domain_x_length / blade_speed

    # Blade starting time
    # This is use to find which vtu files is right after the passing of the blade.
    input_string =  particle.prm_dict["grid arguments"].split(',')
    first_starting_time = 0.3                     # --> HARD CODED IN THE CASE_GENERATOR
    every_mesuring_time = np.empty(number_of_layers)
    every_mesuring_time[0] = first_starting_time + blade_time_per_layer * 0.95            # 0.9 is hard coded


    for j in range(1, number_of_layers):
        every_mesuring_time[j] = every_mesuring_time[j - 1] + blade_time_per_layer * 0.7  # 0.7 is hard coded

    # Create the list of vtu we want to analyse
    # If we do 10 layers, we should have 10 vtu to analyse

    vtu_mesure = np.zeros(number_of_layers, dtype=np.int32)

    # Loop over the vtu in the list and add the one right after the blade
    which_layer = 0
    for j in range(len(particle.list_vtu)):
        # Time of the vtu
        time = particle.time_list[j]

        if time >= every_mesuring_time[which_layer]:
            vtu_mesure[which_layer] = int(j)
            which_layer += 1

            if which_layer == len(every_mesuring_time):
                break

    relative_density_of_each_layer = np.zeros(number_of_layers)
    relative_density_in_total = np.zeros(number_of_layers)
    volume_of_particles = np.zeros(number_of_layers)
    # Loop over this new list
    print("List of vtu which are analyze : ")
    print(vtu_mesure)
    for k in range(1, len(vtu_mesure)):
        df = particle.get_df(vtu_mesure[k])

        # Position of every particle in the X direction
        x_positions = df.points[:,0]

        # Loop throw all the particle
        for j in range(len(x_positions)):
            # Test if they are inside the desired range
            if x_positions[j] >= x_min and x_positions[j] <= x_max:
                volume_of_particles[k] += 1. / 6. * np.pi * (df["diameter"][j])**3


        # Total vertical displacement of the build plate
        total_height = delta_o + (k- 1) * layer_height + 100 * 10**-6
        available_volume = total_height * build_plate_area

        this_layer_height = layer_height
        if (k==1):
            this_layer_height = delta_o + 100 * 10**-6 # delta_B-P

        relative_density_in_total[k] = volume_of_particles[k] / available_volume
        relative_density_of_each_layer[k] = (volume_of_particles[k] - volume_of_particles[k-1]) / (this_layer_height * build_plate_area)

    print(relative_density_of_each_layer[1:-6])
    print("#######")
    print(relative_density_in_total[1:-6])

    plt.plot(np.arange(0,number_of_layers-7), relative_density_of_each_layer[1:-6],"-o" ,color = color[i],label = f"Layers RD - {int(round(delta_o*10**6))} $\mu m$", markersize = 5)
    plt.plot(np.arange(0,number_of_layers-7), relative_density_in_total[1:-6]     ,"--x",color = color[i],label = f"Cummlative RD - {int(round(delta_o*10**6))} $\mu m$",markersize = 5)




plt.title("Evolution of powder layer relative density compare to the \n cumulative relative density for different $\delta_{o}$", fontsize = 16)
plt.xticks(np.arange(0,number_of_layers - 7))
plt.ylabel("Powder relative density",fontsize = 14)
plt.xlabel("Layer number",fontsize = 14)
plt.grid()
plt.legend()
plt.show()








