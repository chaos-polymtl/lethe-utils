# -*- coding: utf-8 -*-


"""
Name   : postprocess_data.py
Author : Audrey Collard-Daigneault
Date   : 17-12-2020
Desc   : This code plots those following data type (<u>/<ub>, <v>/<ub>, <u'u'>/<ub²>, <v'v'>/<ub²>, <u'v'>/<ub²>) of
         generated Lethe data csv files (with the postprocess_data code) with the experimental data of Rapp 2009
         NOTE : data text files of Rapp are dated 2009, but the article is from 2011.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import glob
from pathlib import Path


################################################ FILL OUT THIS PART ###################################################

# Reynolds number of the simulation
Re = 5600

# Information about the lethe data
path_to_data = "./output_csv/"
prefix_name = "graph_all"  # literature and Lethe data to plot should all be in this

# Path and name to save graphs (no extention)
path_to_save = "./output_geometry/"
Path(path_to_save).mkdir(parents=True, exist_ok=True)



name_to_save = "dataingeometry"

# Scale factor for the curves
# Suggestions : 2/3 for average velocities, 15 for reynolds normal stresses and 20 for reynolds shear stresses
scale_factors = [2, 3, 15, 15, 20]

# Label for Lethe data for the legend
# NOTE : make sure the number of labels are the same that the number of Lethe simulation data in csv files and
#        and associated to the right data set
labels = ["Lethe - 1M - 720s", "Lethe - 4M - 300s","Lethe - 4M - 500s"]


#######################################################################################################################

# Design of the geometry
# Polynomial coefficients
a1 = 2.800000000000E+01
b1 = 0.000000000000E+00
c1 = 6.775070969851E-03
d1 = -2.124527775800E-03

a2 = 2.507355893131E+01
b2 = 9.754803562315E-01
c2 = -1.016116352781E-01
d2 = 1.889794677828E-03

a3 = 2.579601052357E+01
b3 = 8.206693007457E-01
c3 = -9.055370274339E-02
d3 = 1.626510569859E-03

a4 = 4.046435022819E+01
b4 = -1.379581654948E+00
c4 = 1.945884504128E-02
d4 = -2.070318932190E-04

a5 = 1.792461334664E+01
b5 = 8.743920332081E-01
c5 = -5.567361123058E-02
d5 = 6.277731764683E-04

a6 = 5.639011190988E+01
b6 = -2.010520359035E+00
c6 = 1.644919857549E-02
d6 = 2.674976141766E-05

# Values related to the geometry
H = 28.0
max_x = 9 * H
max_y = 3.035 * H

# Initiate vectors for plotting
x_vector = np.linspace(0, max_x, 100)
y = np.empty(len(x_vector))

# Generate top and bottom lines for the geometry with polynomials
for i, x in enumerate(x_vector):
    new_x = (max_x - x)  # for the right hill

    # Polynomial equations for left hill
    if 0 <= x < 9:
        y[i] = a1 + b1 * x + c1 * x ** 2 + d1 * x ** 3
        # Check and fix if y is over H
        if y[i] > H:
            y[i] = H

    elif 9 <= x < 14:
        y[i] = a2 + b2 * x + c2 * x ** 2 + d2 * x ** 3

    elif 14 <= x < 20:
        y[i] = a3 + b3 * x + c3 * x ** 2 + d3 * x ** 3

    elif 20 <= x < 30:
        y[i] = a4 + b4 * x + c4 * x ** 2 + d4 * x ** 3

    elif 30 <= x < 40:
        y[i] = a5 + b5 * x + c5 * x ** 2 + d5 * x ** 3

    elif 40 <= x < 54:
        y[i] = a6 + b6 * x + c6 * x ** 2 + d6 * x ** 3
        # Check and fix if y is under 0
        if y[i] < 0:
            y[i] = 0.0

    # Polynomial equations for left hill
    elif 243 < x <= 252:
        y[i] = a1 + b1 * new_x + c1 * new_x ** 2 + d1 * new_x ** 3
        # Check and fix if y is over H
        if y[i] > H:
            y[i] = H

    elif 238 < x <= 243:
        y[i] = a2 + b2 * new_x + c2 * new_x ** 2 + d2 * new_x ** 3

    elif 232 < x <= 238:
        y[i] = a3 + b3 * new_x + c3 * new_x ** 2 + d3 * new_x ** 3

    elif 222 < x <= 232:
        y[i] = a4 + b4 * new_x + c4 * new_x ** 2 + d4 * new_x ** 3

    elif 212 < x <= 222:
        y[i] = a5 + b5 * new_x + c5 * new_x ** 2 + d5 * new_x ** 3

    elif 198 < x <= 212:
        y[i] = a6 + b6 * new_x + c6 * new_x ** 2 + d6 * new_x ** 3
        # Check and fix if y is under 0
        if y[i] < 0:
            y[i] = 0.0

    # Set y to 0 if in flat area
    else:
        y[i] = 0.0

# Normalize results with H (like if H was 1 and not 28)
x_vector /= H
y_bottom = y / H
y_top = max_y * np.ones(len(x_vector)) / H

# Data type to plot and label
all_data_type = ["average_velocity_0", "average_velocity_1", "reynolds_normal_stress_0",
                 "reynolds_normal_stress_1", "reynolds_shear_stress_uv"]

x_labels = [r"$\langle u \rangle/u_{b}$", r"$\langle v \rangle/u_{b}$", r"$\langle u'u' \rangle/u_{b}^{2}$",
            r"$\langle v'v' \rangle/u_{b}^{2}$", r"$\langle u'v' \rangle/u_{b}^{2}$"]

# x position to plot
x_position = [0.05, 1, 2, 3, 4, 5, 6, 7, 8]

# Associate filename to data type
nb_of_files = len(glob.glob1(path_to_data, f"{prefix_name}*"))
range_of_files = list(range(1, nb_of_files + 1))
range_of_files = [str(int).rjust(2, '0') for int in range_of_files]

filenames = []
data_type_files = [[], [], [], [], []]
for file_nb in range_of_files:
    # Search for file with prefix
    filename = [filename for filename in os.listdir(path_to_data)
                if filename.startswith(prefix_name + "_" + file_nb)][0]

    for i in range(0, len(all_data_type)):
        if all_data_type[i] in filename:
            data_type_files[i].append(filename)

for index, data_type in enumerate(all_data_type):
    # Plot data for the choosen data type
    fig, ax = plt.subplots()

    ax.plot(x_vector, y_bottom, '-k', linewidth=0.5)
    ax.plot(x_vector, y_top, '-k', linewidth=0.5)

    # Set info for this data type
    x_label = x_labels[index]
    scale_factor = scale_factors[index]

    # Get the filenames for the data type
    files = data_type_files[index]

    is_first_curve = True
    # Process the file if the choosen data_type is in the file name
    for name in files:
        data = pd.read_csv(path_to_data + name, sep=",")
        x = float(name.split("_x_")[1].split(".csv")[0])

        if x in x_position:
            # Verify if number of labels is right
            nb_data = int(data.shape[1] / 2)
            nb_lethe_data = nb_data - 2
            assert len(labels) == nb_lethe_data, f"It seems to have {nb_lethe_data} sets of Lethe data and you gave " \
                                                 f"{len(labels)} labels, please verify your labels names or your csv files."

            pos = 0
            nb_curve = 0
            # Scale data
            for i in range(0, data.shape[1], 2):
                data[data.columns[i]] = scale_factor * data[data.columns[i]] + x

                # Set lebels and colors (max 4 Lethe data sets)
                colors = ["xkcd:crimson", "xkcd:bright blue", "xkcd:dark lavender", "xkcd:pale orange"]
                if is_first_curve is True:
                    if "Rapp" in data.columns[i]:
                        label = 'Experimental - Rapp2009'
                        color = "xkcd:black"
                        nb_curve += 1
                    elif "Breuer" in data.columns[i]:
                        label = 'Simulation LESOCC - Breuer2009'
                        color = "xkcd:green"
                        nb_curve += 1
                    else:
                        label = labels[pos]
                        color = colors[pos]
                        pos += 1
                        nb_curve += 1

                    ax.plot(data[data.columns[i]], data[data.columns[i + 1]], "--", color=color, label=label,
                            linewidth=0.75)

                    # All first curves are plot
                    if nb_curve == nb_data:
                        is_first_curve = False
                else:
                    if "Rapp" in data.columns[i]:
                        color = "xkcd:black"
                    elif "Breuer" in data.columns[i]:
                        color = "xkcd:green"
                    else:
                        color = colors[pos]
                        pos += 1

                    ax.plot(data[data.columns[i]], data[data.columns[i + 1]], "--", color=color, linewidth=0.75)

    # Plot and save graph
    ax.set_title(data_type + " at Re = " + str(Re))
    ax.set_xlabel("$x/h$ ; " + str(scale_factor) + "$*$" + x_label)
    ax.set_ylabel("$y/h$")
    plt.vlines([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 0, max_y / H, linestyle=':', color='xkcd:dark grey', linewidth=0.75)
    ax.set_ybound(-0.5, max_y / H + nb_data * 0.4)
    plt.gca().set_aspect('equal', adjustable='box')
    ax.legend(fontsize='x-small')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.savefig(path_to_save + name_to_save + "_" + data_type + ".png", dpi=500)
    plt.close(fig)
    ax.clear()
