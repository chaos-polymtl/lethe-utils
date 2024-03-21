# Name   : plot_data_with_geometry_baseline.py
# Author : Laura Prieto (adapted from Catherine Radburn and Audrey Collard-Daigneault)
# Date   : 05-07-2021
# Desc   : This code plots those following data type (u/u_b, v/u_b, u'u'/u_b², v'v'/u_b², u'v'/u_b²) of
#          generated Lethe data csv files (with the post_processing_new.py code) with the experimental data of Rapp 2009
#          and the computational data of Breuer 2009.
#           If all x_value and data_type available are required, ignore data_type and scale_factor in lines 40 and 45, and
#           make all_data = True.

import pandas
import numpy
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches
from matplotlib.patches import ConnectionPatch
from pathlib import Path
import time
start_time = time.time()

################################################ FILL OUT THIS PART ###################################################

# Reynolds number of the simulation
Re = 5600

# Path to .csv file (same as post_processing_new.py)
path_to_lethe_data = "../output_csv/all_data/"
path_to_literature_data = "../output_csv/literature/"+ str(Re) + "/"

# Path and name to save graphs
path_to_save = "../article_figures/"

Path(path_to_save).mkdir(parents=True, exist_ok=True)

# Label for Lethe data for the legend (should be the same as used in post_processing_new.py)
# NOTE : make sure the number of labels are the same that the number of Lethe simulation data in csv files and
#        and associated to the right data set
labels = ["Lethe baseline 250K", "Lethe baseline 1M", "Lethe baseline 4M"]

# File names of lethe data
file_names_lethe_data = ["0.1_250K_1000s_5600", "0.1_1M_1000s_old_baseline", "0.1_4M_1000s_5600"]
# data_type_available = ["average_velocity_0", "average_velocity_1", "reynolds_normal_stress_0",
#                            "reynolds_normal_stress_1", "reynolds_shear_stress_uv"]
data_type = "reynolds_shear_stress_uv"

# Scale factor for the curves
# Suggestions : 0.8 for average_velocity_0, 3 for average_velocity_1, 5 for reynolds_normal_stress_0,
#               15 for reynolds_normal_stress_1, and 10 for reynolds_shear_stress
scale_factor = 10

# Extract and generate graphs for all x_values and data_types? (True or False)
all_data = True

# Display the title on the output graphs? (True or False)
display_title = False

#Add zoom in plots?
zoom_in_plots = True

#######################################################################################################################
# Function to define hill geometry
def hill_geometry():
    # Shape of lower wall geometry
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
    x_vector = numpy.linspace(0, max_x, 100)
    y = numpy.empty(len(x_vector))

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
    y_top = max_y * numpy.ones(len(x_vector)) / H

    return x_vector, y_bottom, y_top

# Function to retrieve data from .csv files
def obtain_data(x_available, path_to_lethe_data, file_names_lethe_data, data_type, path_to_literature_data):
    all_x_data = []
    for x_value in x_available:
        data = []

        # Read data and append to list
        Rapp2009_csv = path_to_literature_data + '_Rapp2009' + str(data_type) + '_x_' + str(x_value) + '.csv'
        Rapp2009_data = pandas.read_csv(Rapp2009_csv)
        Rapp2009_data = Rapp2009_data.to_numpy()
        data.append(Rapp2009_data)

        if Re == 5600 or Re == 10600:
            Breuer2009_csv = path_to_literature_data + '_Breuer2009' + str(data_type) + '_x_' + str(x_value) + '.csv'
            Breuer2009_data = pandas.read_csv(Breuer2009_csv)
            Breuer2009_data = Breuer2009_data.to_numpy()
            data.append(Breuer2009_data)

        for file in file_names_lethe_data:
            Lethe_data_csv = path_to_lethe_data + '_Lethe_data_' + str(file) + '_' + str(data_type) + '_x_' + str(x_value) + '.csv'
            Lethe_data = pandas.read_csv(Lethe_data_csv)
            Lethe_data = Lethe_data.to_numpy()
            data.append(Lethe_data)

        # Create list containing lists of data at all x available
        all_x_data.append(data)
    return all_x_data

# Function to plot data at all x
def plot_onto_geometry(x_available, Re, all_x_data, folder_to_save, x_vector, y_bottom, y_top, scale_factor,
                       lethe_labels, x_label, show_title, data_type):
    
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.family']='DejaVu Serif'
    plt.rcParams['font.serif']='cm'
    plt.rcParams['font.size'] = 10

    # Plot data for the chosen data type
    fig = plt.figure()
    # plt.subplots_adjust(bottom = 0., left = 0, top = 1., right = 1)
    ax = fig.add_subplot(2,8,(9,16))

    # Plot geometry
    ax.plot(x_vector, y_bottom, '-k', linewidth=0.5, zorder = 0)
    ax.plot(x_vector, y_top, '-k', linewidth=0.5, zorder = 0)

    if zoom_in_plots is True:
        ax2 = fig.add_subplot(2,8,(2,3), aspect='equal', zorder = 2)
        ax3 = fig.add_subplot(2,8,(4,5), aspect='equal', zorder = 2)
        ax4 = fig.add_subplot(2,8,(6,7), aspect='equal', zorder = 2)

        ax2.plot(x_vector, y_bottom, '-k', linewidth=0.5)
        ax2.plot(x_vector, y_top, '-k', linewidth=0.5)

        ax3.plot(x_vector, y_bottom, '-k', linewidth=0.5)
        ax3.plot(x_vector, y_top, '-k', linewidth=0.5)

        ax4.plot(x_vector, y_bottom, '-k', linewidth=0.5)
        ax4.plot(x_vector, y_top, '-k', linewidth=0.5)

    # Plot data
    for i, x_value in enumerate(x_available):
        # Extract data at x value
        data_x = all_x_data[i]

        # Specify colours for Lethe plots
        colors = ["xkcd:blue", "xkcd:lime green", "xkcd:red", "xkcd:orange", "xkcd:brown", "xkcd:pink", "xkcd:gold"]
        # colors = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494"]    

        # data_x is a list of Rapp then Breuer then Lethe numpy arrays at x_value
        for j, dataset in enumerate(data_x):
            if j == 0:   # Data is from Rapp
                # Scale data to plot and remove first column
                dataset[0, :] = (scale_factor * dataset[0, :]) + x_value
                dataset = numpy.delete(dataset, 0, 1)

                # Set labels, colour
                label = 'Experimental - Rapp 2009'
                color = "k"

                # Plot y-values, data
                # Only include label on first x plot
                if x_value == 0.5:
                    ax.plot(dataset[0,:], dataset[1,:], "-", color=color, label=label, linewidth=1.2)
                    if zoom_in_plots is True:
                        ax2.plot(dataset[0,:], dataset[1,:], "-", color=color, linewidth=1.2)
                        ax3.plot(dataset[0,:], dataset[1,:], "-", color=color, linewidth=1.2)
                        ax4.plot(dataset[0,:], dataset[1,:], "-", color=color, linewidth=1.2)
                else:
                    ax.plot(dataset[0,:], dataset[1,:], "-", color=color, linewidth=1.2)
                    if zoom_in_plots is True:
                        ax2.plot(dataset[0,:], dataset[1,:], "-", color=color, linewidth=1.2)
                        ax3.plot(dataset[0,:], dataset[1,:], "-", color=color, linewidth=1.2)
                        ax4.plot(dataset[0,:], dataset[1,:], "-", color=color, linewidth=1.2)

            elif j == 1 and Re != 37000:      # Data is from Breuer
                # Scale data to plot and remove first column
                dataset[0,:] = (scale_factor * dataset[0,:]) + x_value
                dataset = numpy.delete(dataset, 0, 1)

                # Set labels, colour
                label = 'LESOCC - Breuer 2009'
                color = "k"

                # Plot y-values, data
                # Only include label on first x plot
                if x_value == 0.5:
                    ax.plot(dataset[0,:], dataset[1,:], ":", color=color, label=label, linewidth=1.2)
                    if zoom_in_plots is True:                    
                        ax2.plot(dataset[0,:], dataset[1,:], ":", color=color, linewidth=1.2)
                        ax3.plot(dataset[0,:], dataset[1,:], ":", color=color, linewidth=1.2)
                        ax4.plot(dataset[0,:], dataset[1,:], ":", color=color, linewidth=1.2)

                else:
                    ax.plot(dataset[0,:], dataset[1,:], ":", color=color, linewidth=1.2)
                    if zoom_in_plots is True:
                        ax2.plot(dataset[0,:], dataset[1,:], ":", color=color, linewidth=1.2)
                        ax3.plot(dataset[0,:], dataset[1,:], ":", color=color, linewidth=1.2)
                        ax4.plot(dataset[0,:], dataset[1,:], ":", color=color, linewidth=1.2)

            else:   # Data is from Lethe
                # Scale data to plot and remove first column
                dataset[0, :] = (scale_factor * dataset[0, :]) + x_value
                dataset = numpy.delete(dataset, 0, 1)

                # Set labels, colour
                label = lethe_labels[j-2]
                color = colors[j-2]

                # Plot y-values, data
                # Only include label on first x plot
                if x_value == 0.5:
                    ax.plot(dataset[0, :], dataset[1, :], "--", color=color, label=label, linewidth=1.2)
                    if zoom_in_plots is True:                 
                        ax2.plot(dataset[0,:], dataset[1,:], "--", color=color, linewidth=1.2)
                        ax3.plot(dataset[0,:], dataset[1,:], "--", color=color, linewidth=1.2)
                        ax4.plot(dataset[0,:], dataset[1,:], "--", color=color, linewidth=1.2)

                else:
                    ax.plot(dataset[0, :], dataset[1, :], "--", color=color, linewidth=1.2)
                    if zoom_in_plots is True:
                        ax2.plot(dataset[0,:], dataset[1,:], "--", color=color, linewidth=1.2)
                        ax3.plot(dataset[0,:], dataset[1,:], "--", color=color, linewidth=1.2)
                        ax4.plot(dataset[0,:], dataset[1,:], "--", color=color, linewidth=1.2)

    # Plot and save graph
    if show_title is True:
        if data_type == "average_velocity_0":
            title = "Average x velocity $u$"
        elif data_type == "average_velocity_1":
            title = "Average y velocity $v$"
        elif data_type == "reynolds_normal_stress_0":
            title = "Reynolds normal stress $u'u'$"
        elif data_type == "reynolds_normal_stress_1":
            title = "Reynolds normal stress $v'v'$"
        elif data_type == "reynolds_shear_stress_uv":
            title = "Reynolds shear stress $u'v'$"
        elif data_type == "reynolds_normal_stress_2":
            title = "Reynolds normal stress $w'w'$"
        elif data_type == "turbulent_kinetic_energy":
            title = "Turbulent kinetic energy $k$"
        else:
            title = None

        ax.set_title(title + " at Re = " + str(Re))
   
    #Settings of main plot

    # ax.set_xlabel("$x/h$ ; " + str(scale_factor) + x_label, fontname="Arial")
    ax.set_xlabel("$x/h$")
    ax.set_ylabel("$y/h$")
    # plt.vlines([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 3.035, linestyle=':', color='xkcd:dark grey', linewidth=0.7)
    ax.set_ybound(-0.05, 3.035)
    ax.set_xbound(0,9)
    plt.gca().set_aspect('equal', adjustable='box')
    # ax.legend(fontsize='x-small')

    if Re == 10600:
        # fig.subplots_adjust(bottom=0.7)
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.6), facecolor = 'white', framealpha = 0.75, ncol=3, edgecolor = 'black', fancybox = False, shadow = False)
    elif Re == 37000:
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.6), facecolor = 'white', framealpha = 0.75, ncol=2, edgecolor = 'black', fancybox = False, shadow = False)
    else:
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.6), facecolor = 'white', framealpha = 0.75, ncol=3, edgecolor = 'black', fancybox = False, shadow = False)
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    ##Zoom plots: set the coordinates for the zoom-in plot x1, x2, y1, y2
    if zoom_in_plots is True:
        #1st. Zoom in
        if data_type == "average_velocity_0":
             x1 = 0; x2 = 0.7; y1 = 0.7; y2 = 1.4 #for average velocity
        else:
            x1 = 0; x2 = 0.7; y1 = 0.7; y2 = 1.4 #for reynolds normal stress
        ax2.set_xbound(x1, x2)
        ax2.set_ybound(y1, y2)
        ax2.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
        ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.2))

        ax.add_patch(patches.Rectangle((x1,y1),(x2-x1),(y2-y1),linewidth=0.5, edgecolor='gray', facecolor = 'none'))
        ax2_1 = ConnectionPatch(xyA=(x1 + (x2-x1)/2, y2), coordsA=ax.transData, xyB=(x1 + (x2-x1)/2, y1), coordsB=ax2.transData, color = 'gray',linewidth=0.5, arrowstyle ="->", zorder = 1)
        fig.add_artist(ax2_1)

        #2nd zoom in
        if data_type == "average_velocity_0":
            x1 = 3.6; x2 = 4.3; y1 = 0; y2 = 0.7 #for average velocity
        elif data_type == "reynolds_shear_stress_uv":
            x1 = 3.5; x2 = 4.2; y1 = 0; y2 = 0.7 #for reynolds shear stress
        else:
            x1 = 3.9; x2 = 4.6; y1 = 0; y2 = 0.7 #for reynolds normal stress
        ax3.set_xbound(x1, x2)
        ax3.set_ybound(y1, y2)
        ax3.xaxis.set_major_locator(ticker.MultipleLocator(0.2))

        ax3.yaxis.set_major_locator(ticker.MultipleLocator(0.2))

        ax.add_patch(patches.Rectangle((x1,y1),(x2-x1),(y2-y1),linewidth=0.5, edgecolor='gray', facecolor = 'none'))
        ax3_1 = ConnectionPatch(xyA=(x1 + (x2-x1)/2, y2), coordsA=ax.transData, xyB=(x1 + (x2-x1)/2, y1), coordsB=ax3.transData, color = 'gray',linewidth=0.5, arrowstyle ="->", zorder = 1)
        fig.add_artist(ax3_1)

        #3rd zoom in
        if data_type == "average_velocity_0":
            x1 = 7.2; x2 = 7.9; y1 = 2.3; y2 = 3.035 #for average velocity
        else:
            x1 = 6.6; x2 = 7.3; y1 = 2.3; y2 = 3.035 #for reynolds normal stress
        ax4.set_xbound(x1, x2)
        ax4.set_ybound(y1, y2)
        ax4.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
        ax4.yaxis.set_major_locator(ticker.MultipleLocator(0.2))

        ax.add_patch(patches.Rectangle((x1,y1),(x2-x1),(y2-y1),linewidth=0.5, edgecolor='gray', facecolor = 'none'))
        ax4_1 = ConnectionPatch(xyA=(x1 + (x2-x1)/2, y2), coordsA=ax.transData, xyB=(x1 + (x2-x1)/2, y1), coordsB=ax4.transData, color = 'gray',linewidth=0.5, arrowstyle ="->", zorder = 1)
        fig.add_artist(ax4_1)


    plt.tight_layout()
    # plt.show()
    plt.savefig(folder_to_save + "baseline_data_in_geometry_" + str(data_type) + "_" + str(Re) +".eps", dpi=800, bbox_inches='tight')
    plt.close(fig)
    ax.clear()
    
    if zoom_in_plots is True:
        ax2.clear()
        ax3.clear()
        ax4.clear()

    print("Data plotted over geometry")
    return

########################################################################################################################
# Call functions
x_vector_hill, y_bottom_hill, y_top_hill = hill_geometry()

x_available = [0.05, 0.5, 1, 2, 3, 4, 5, 6, 7, 8]

# Set x_label
# data_type_available = ["average_velocity_0", "average_velocity_1", "reynolds_normal_stress_0",
#                             "reynolds_normal_stress_1", "reynolds_shear_stress_uv"]
data_type_available = ["average_velocity_0", "reynolds_normal_stress_0", "reynolds_shear_stress_uv"]

# x_labels_available = ["$u/u_b$", "$v/u_b$", "$u'u'/u_b^2$", "$v'v'/u_b^2$", "$u'v'/u_b^2$"]
x_labels_available = ["$u/u_b$", "$u'u'/u_b^2$", "$u'v'/u_b^2$"]

# Plot all data profiles
if all_data is True:
    scale_available = [0.8, 3, 5, 15, 10]

    # Cycle through all data types
    for data in data_type_available:
        print("Data type: " + data)
        x_label = x_labels_available[data_type_available.index(data)]
        scale = scale_available[data_type_available.index(data)]

        data_at_all_x = obtain_data(x_available, path_to_lethe_data, file_names_lethe_data, data, path_to_literature_data)
        plot_onto_geometry(x_available, Re, data_at_all_x, path_to_save, x_vector_hill, y_bottom_hill, y_top_hill, scale,
                        labels, x_label, display_title, data)

# Plot specify profiles        
else:
    x_label = x_labels_available[data_type_available.index(data_type)]

    data_at_all_x = obtain_data(x_available, path_to_lethe_data, file_names_lethe_data, data_type, path_to_literature_data)
    plot_onto_geometry(x_available, Re, data_at_all_x, path_to_save, x_vector_hill, y_bottom_hill, y_top_hill, scale_factor,
                    labels, x_label, display_title, data_type)

print("--- %s seconds ---" % (time.time() - start_time))
