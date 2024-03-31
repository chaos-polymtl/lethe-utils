#############################################################################
"""
Postprocessing automation tool.

By: Olivier Gaboriault
Date: January 13th, 2024
"""
#############################################################################
'''Importing Libraries'''
import sys


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from lethe_pyvista_tools import *

#############################################################################

# Take case path as argument
prm_file_names = np.array(
    [
     #"75_01_05/75_01_05.prm",
     #"75_01_10/75_01_10.prm",
     #"75_01_20/75_01_20.prm"
     "75_03_05/75_03_05.prm",
     "75_03_10/75_03_10.prm",
     "75_03_20/75_03_20.prm"
     ]) # ./parameter.prm -->peut-[etre # ./parameter.prm -->peut-[etre
plt.figure(figsize=(10, 6))

# Loop over a
for i in range(len(prm_file_names)):
    print(f"\n\n Starting postprocessing for simulation number {i + 1} / {len(prm_file_names)}.")
    # Variables from the first section of the .prm of the .prm file
    with open("./" + prm_file_names[i], 'r') as file:
        lines = file.readlines()  # Read all lines into a list

    number_of_layers = int((lines[3]).split('=')[1]) + 2
    blade_speed = float((lines[4]).split('=')[1])
    delta_B_P = float((lines[5]).split('=')[1])
    delta_o = float((lines[6]).split('=')[1])
    delta_n = float((lines[7]).split('=')[1])
    GAP = float((lines[9]).split('=')[1])
    first_layer_extrusion = float((lines[10]).split('=')[1])
    n_layer_extrusion = float((lines[11]).split('=')[1])
    first_starting_time = float((lines[12]).split('=')[1])
    delta_starting_time = float((lines[13]).split('=')[1])
    extra_time_layer_zero = float((lines[14]).split('=')[1])
    blade_thickness = 0.004267766952966369

    # Create the particle object
    prm_file_name = (prm_file_names[i]).split('/')[1]

    pvd_name = 'out.pvd'
    ignore_data = ['type', 'volumetric contribution', 'velocity', 'torque', 'fem_torque', 'fem_force']
    particle = lethe_pyvista_tools((prm_file_names[i]).split('/')[0], prm_file_name, pvd_name, ignore_data=ignore_data)
    #############################################################################

    # Bluid plate domain
    # This string could be use to isolate the start and the end of the build plate (not for now)
    input_string = particle.prm_dict["initial translation"]
    x_min_Feeder = float(input_string[0].split(',')[0])  # --> This is the X translation of solid object #1
    x_max_Feeder = float(input_string[1].split(',')[0])  # --> This is the X translation of solid object #1
    x_min_BP = float(input_string[2].split(',')[0])  # --> This is the X translation of solid object #2
    x_max_BP = float(input_string[3].split(',')[0])  # --> This is the X translation of solid object #3

    # Lenght of the domain
    input_string = particle.prm_dict["grid arguments"].split(',')
    domain_x_length = float(input_string[4].split(':')[1])  # This is the dealii triangulation in X
    domain_z_length = float(input_string[6].split(':')[0])  # This is the dealii triangulation in Z
    build_plate_length = x_max_BP - x_min_BP
    build_plate_area = domain_z_length * build_plate_length

    # How much time it takes for a blade to move throw all the domain
    # This will help to find the starting time of each blade, thus the mesuring time we should use
    blade_time_per_layer = domain_x_length / blade_speed

    # Blade starting time

    # Times it takes for a blade to cross the domain in the X direction
    time_per_layer = (domain_x_length + blade_thickness) / blade_speed

    # Finding the departure time of all the blades
    every_starting_time = np.empty(number_of_layers)
    every_starting_time[0] = first_starting_time + extra_time_layer_zero
    for j in range(1, number_of_layers):
        every_starting_time[j] = every_starting_time[j - 1] + time_per_layer * delta_starting_time

    print(every_starting_time)

    # Time step to measure the relative density off the powder on the feeder
    measuring_time_Feeder_rel_density = every_starting_time

    # Time step to measure the relative density off the powder on the build plate
    measuring_time_PB_rel_density = every_starting_time + 0.9 * blade_time_per_layer

    # Create lists of vtus we want to analyse
    vtu_measure_Feeder_slice = 0
    vtu_measure_Feeder_rel_density = np.array([], dtype=int)
    vtu_measure_BP_rel_density = np.array([], dtype=int)

    # Loop over the vtu in the list and add the one right after the blade
    which_layer = 0
    index_F_RD = 0
    time = particle.time_list

    for j in range(len(particle.list_vtu)):
        if time[j] > measuring_time_Feeder_rel_density[0] + x_max_Feeder * 1.1 / blade_speed:
            vtu_measure_Feeder_slice = j
            break

    for j in range(len(particle.list_vtu)):
        if index_F_RD < number_of_layers and time[j] >= measuring_time_Feeder_rel_density[index_F_RD]:
            vtu_measure_Feeder_rel_density = np.append(vtu_measure_Feeder_rel_density, int(j) - 1)
            index_F_RD += 1

        if time[j] >= measuring_time_PB_rel_density[which_layer]:
            vtu_measure_BP_rel_density = np.append(vtu_measure_BP_rel_density, int(j))
            which_layer += 1

            if which_layer == number_of_layers:
                break

    BP_rel_density_each_layer = np.array([])
    BP_rel_density_cumulative = np.array([])
    volume_on_BP = np.zeros(number_of_layers)
    volume_on_feeder = np.zeros(number_of_layers)
    feeder_rel_density = np.array([])
    # Loop over this new list
    print(f" ####### Lists of analysed vtus :"
          f"\n Feeder_slice       : {vtu_measure_Feeder_slice}"
          f"\n Feeder_rel_density :{vtu_measure_Feeder_rel_density}"
          f"\n BP_rel_density     :{vtu_measure_BP_rel_density}"
          f"\n #######")

    # Constant used for the volume calculation
    volume_cst = 1. / 6. * np.pi

    ## Feeder section ##
    initial_feeder_height = -(number_of_layers) * n_layer_extrusion - first_layer_extrusion

    # Feeder slices subsection
    current_height = 0
    feeder_layer_limits = np.array([])
    while current_height >= initial_feeder_height:
        feeder_layer_limits = np.append(feeder_layer_limits, current_height)
        current_height -= n_layer_extrusion

    df = particle.get_df(vtu_measure_Feeder_slice)

    x_positions = df.points[:, 0]
    y_positions = df.points[:, 1]
    feeder_powder_volume_in_slices = np.zeros(len(feeder_layer_limits))
    slice_volume = n_layer_extrusion * domain_z_length * (x_max_Feeder - x_min_Feeder)

    for j in range(len(x_positions)):
        if x_min_Feeder <= x_positions[j] <= x_max_Feeder and y_positions[j] > feeder_layer_limits[-1]:
            # Find in which bin the particle is respective to the limits and add it's volume to the right bin
            feeder_powder_volume_in_slices[np.digitize(y_positions[j], feeder_layer_limits)] += volume_cst * (df["diameter"][j]) ** 3

    feeder_slices_rel_density = feeder_powder_volume_in_slices / slice_volume

    print(f"\n Feeder's slice relative density: \n{feeder_slices_rel_density} \n #######")

    # Feeder relative density subsection
    height = initial_feeder_height
    for index, k in enumerate(vtu_measure_Feeder_rel_density[1:], start=1):
        # Position of every particle in the X direction
        df = particle.get_df(k)
        x_positions = df.points[:, 0]

        # Available volume
        available_volume = -height * domain_z_length * (x_max_Feeder - x_min_Feeder)

        # Loop throw all the particle
        for j in range(len(x_positions)):
            # Check if they are inside the desired range
            if x_min_Feeder <= x_positions[j] <= x_max_Feeder:
                volume_on_feeder[index] += volume_cst * (df["diameter"][j]) ** 3

        # Compute the relative density in the feeder
        feeder_rel_density = np.append(feeder_rel_density,volume_on_feeder[index] / available_volume )

        # Adjust the vertical available space for the next layer
        height = initial_feeder_height + first_layer_extrusion + n_layer_extrusion * (index - 1)

    print(f"\n Feeder's volume of powder: \n{volume_on_feeder} \n #######")
    print(f"\n Feeder's relative density: \n{feeder_rel_density} \n#######")

    for index, k in enumerate(vtu_measure_BP_rel_density):


        # Load the position in df
        df = particle.get_df(k)

        # Position of every particle in the X direction
        x_positions = df.points[:, 0]

        # Loop throw all the particle
        for j in range(len(x_positions)):
            # Test if they are inside the desired range
            if x_min_BP <= x_positions[j] <= x_max_BP:
                volume_on_BP[index] += volume_cst * (df["diameter"][j]) ** 3

        #print(f"Index: {index}")
        #print(f"K : {k}")
        #print(f"Volume : {volume_on_BP[index]}")

        if index != 0:
            # Total vertical displacement of the build plate
            total_height = index * delta_n
            available_volume = total_height * build_plate_area
            this_layer_height = delta_n

            BP_rel_density_cumulative = np.append(BP_rel_density_cumulative,
                                                  (volume_on_BP[index] - volume_on_BP[0]) / available_volume)
            BP_rel_density_each_layer = np.append(BP_rel_density_each_layer, (volume_on_BP[index] - volume_on_BP[index - 1]) / (
                    this_layer_height * build_plate_area))


    print(f" Powder volume on build plate      : \n{volume_on_BP} \n ######## ")
    print(f" Powder volume in the reservoir    : \n{volume_on_feeder} \n ######## ")
    print(f" Relative density in the reservoir : \n{feeder_rel_density} \n ######## ")
    print(f" Relative density of each layer    : \n{BP_rel_density_each_layer} \n ######## ")
    print(f" Cummulative relative density      : \n{BP_rel_density_cumulative} \n ########")

    np.save("./00_binary/" + prm_file_name.split(".")[0] + "_PowderVolumeFeed", volume_on_feeder)
    np.save("./00_binary/" + prm_file_name.split(".")[0] + "_RelDensityFeed", feeder_rel_density)
    np.save("./00_binary/" + prm_file_name.split(".")[0] + "_RelDensityFeederLayers", feeder_slices_rel_density)
    np.save("./00_binary/" + prm_file_name.split(".")[0] + "_LRD", BP_rel_density_each_layer)
    np.save("./00_binary/" + prm_file_name.split(".")[0] + "_CRD", BP_rel_density_cumulative)
    np.save("./00_binary/" + prm_file_name.split(".")[0] + "_number_of_layers", number_of_layers-1)

    print("Binary files saved!")

print("Job is done")
