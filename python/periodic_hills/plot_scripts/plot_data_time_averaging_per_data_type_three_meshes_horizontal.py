# Name   : plot_data_with_geometry_mesh_refinement.py
# Author : Laura Prieto Saavedra (Adpated from Catherine Radburn and Audrey Collard-Daigneault)
# Date   : 22-06-2021
# Desc   : This code plots simulation data from Lethe and other data from literature.
#           It loads .csv files and plot data into a .png file. 
#           It plots the data for x/h = 0.5,2,4,6 for an specific data type.

import pandas
import numpy
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches
from matplotlib.patches import ConnectionPatch
from pathlib import Path
import time
from mpl_toolkits.axes_grid.inset_locator import inset_axes

start_time = time.time()

########################################################################################################################
# SET VARIABLES

# Reynolds number of the simulation (Currently available for Re = 5600 only)
Re = 5600

# Path to folder where Lethe simulation data is stored
path_to_lethe_data = "../output_csv/all_data/"

#Filename
#Coarse mesh
file_names_lethe_data = ["0.025_250K_500s_5600", "0.025_250K_600s_5600", "0.025_250K_700s_5600", "0.025_250K_800s_5600", "0.025_250K_900s_5600", "0.025_250K_1000s_5600"]

#Fine mesh
file_names_lethe_data_2 = ["0.025_1M_500s_5600_old_baseline", "0.025_1M_600s_5600_old_baseline", "0.025_1M_700s_5600_old_baseline", "0.025_1M_800s_5600", "0.025_1M_900s_5600_old_baseline", "0.025_1M_1000s_old_baseline"]

#Fine mesh
file_names_lethe_data_3 = ["0.025_4M_500s_5600", "0.025_4M_600s_5600", "0.025_4M_700s_5600", "0.025_4M_800s_5600", "0.025_4M_900s_5600", "0.025_4M_1000s_5600"]

# Label for Lethe data for the legend
# NOTE : make sure the number of labels are the same that the number of files names of lethe data
labels = ["Lethe - 500s", "Lethe - 600s", "Lethe - 700s", "Lethe - 800s","Lethe - 900s","Lethe baseline - 1000s"]

# Information about the literature data
path_to_literature_data = "../output_csv/literature/5600/"

# Time step used
time_step = 0.025

# Save graph.png 
# folder_to_save_png = "../output_png/averaging/"
folder_to_save_png = "../article_figures/"

Path(folder_to_save_png).mkdir(parents=True, exist_ok=True)

# Extract and generate graphs for all x_values and data_types? (True or False)
all_data = True

# Enable zoom in plots
zoom_in = True

# Save a figure or show plot only (True or False)
save_figure = True

########################################################################################################################
# Function to retrieve data from .csv files
def obtain_data(x_values, path_to_literature_data, path_to_lethe_data, file_names_lethe_data, file_names_lethe_data_2, files_names_lethe_data_3, data_type):

    index = 0
    Rapp2009_all_data = list()
    Breuer2009_all_data = list()
    Lethe_all_data = list()
    Lethe_all_data_2 = list()
    Lethe_all_data_3 = list()

    # Create temporal arrays to avoid code repetition
    file_names = [file_names_lethe_data, file_names_lethe_data_2, file_names_lethe_data_3]
    lethe_data_array = [Lethe_all_data, Lethe_all_data_2, Lethe_all_data_3]

    for x_value in x_values:
        # Read data and append to list
        Rapp2009_csv = path_to_literature_data + '_Rapp2009' + str(data_type) + '_x_' + str(x_value) + '.csv'
        Rapp2009_data = pandas.read_csv(Rapp2009_csv)
        Rapp2009_data = Rapp2009_data.to_numpy()
        Rapp2009_data = numpy.delete(Rapp2009_data, 0, 1)
        Rapp2009_all_data.append(Rapp2009_data)
    
        Breuer2009_csv = path_to_literature_data + '_Breuer2009' + str(data_type) + '_x_' + str(x_value) + '.csv'
        Breuer2009_data = pandas.read_csv(Breuer2009_csv)
        Breuer2009_data = Breuer2009_data.to_numpy()
        Breuer2009_data = numpy.delete(Breuer2009_data, 0, 1)   
        Breuer2009_all_data.append(Breuer2009_data)

        for i in range(len(file_names)):
            Lethe_data=list()
            for file in file_names[i]:
                Lethe_data_csv = path_to_lethe_data + '_Lethe_data_' + str(file) + '_' + str(data_type) + '_x_' + str(x_value) + '.csv'
                Lethe_data_loc = pandas.read_csv(Lethe_data_csv)
                Lethe_data_loc = Lethe_data_loc.to_numpy()
                Lethe_data_loc = numpy.delete(Lethe_data_loc, 0, 1)
                Lethe_data.extend(Lethe_data_loc)
            lethe_data_array[i].append(Lethe_data)
        
    # print(Breuer2009_all_data)
    return Breuer2009_all_data, Rapp2009_all_data, Lethe_all_data, Lethe_all_data_2, Lethe_all_data_3

# Plot literature values against Lethe values
def plot_to_png(Breuer2009_all_data, Rapp2009_all_data, lethe_all_data, lethe_all_data_2, lethe_all_data_3, data_type, x_values, labels,
                folder_to_save_png, time_step):
    # Plotting results
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.family']='DejaVu Serif'
    plt.rcParams['font.serif']='cm'
    plt.rcParams['font.size'] = 16

    nrows = 3
    ncols = 4
    fig, axs = plt.subplots(nrows, ncols) 

    colors = ["xkcd:blue", "xkcd:lime green", "xkcd:red", "xkcd:orange", "xkcd:brown", "xkcd:pink", "xkcd:gold"]       
    
    # Set display axis titles
    if data_type == "average_velocity_0":
        x_axis_label = "$u/u_b$"
    elif data_type == "average_velocity_1":
        x_axis_label = "$v/u_b$"
    elif data_type == "reynolds_normal_stress_0":
        x_axis_label = "$u'u'/u_b^2$"
    elif data_type == "reynolds_normal_stress_1":
        x_axis_label = "$v'v'/u_b^2$"
    elif data_type == "reynolds_shear_stress_uv":
        x_axis_label = "$u'v'/u_b^2$"
    elif data_type == "reynolds_normal_stress_2":
        x_axis_label = "$w'w'/u_b^2$"
    elif data_type == "turbulent_kinetic_energy":
        x_axis_label = "$k/u_b^2$"
    else:
        x_axis_label = None
    
    x_labels = list()
    index = 0
    for x_value in x_values:
        x_labels.append(x_axis_label + " at $x/h$=" + str(x_value))

    if zoom_in == True:
        # Fix limits for zoom in plots depending on data type    
        if data_type == "average_velocity_0":
            location = 'upper left'
        elif data_type == "reynolds_normal_stress_0":
            location = 'upper right'
        elif data_type == "reynolds_shear_stress_uv":
            location = 'upper left'
        else:
            location = 'upper right'

        # Create sub axes for zoom-in plots of each subplot
        sub_axes = list()
        for i in range(nrows):
            for j in range(ncols):
                sub_axes.append(inset_axes(axs[i][j], height = "30%", width = "30%", loc = location))

    # Data corresponding to first row of subplots
    for i in range(nrows):
        value = 0
        number_of_subaxes = ncols*i
        lethe_row_data = list()
        if (i == 0):
            lethe_row_data = lethe_all_data
        elif (i == 1):
            lethe_row_data = lethe_all_data_2
        elif (i == 2):
            lethe_row_data = lethe_all_data_3

        for j in range(ncols):
            for x_value in x_values:
                # Plot Lethe data
                index = 0
                chunk = 0
                for file_name in file_names_lethe_data:
                    if file_name is not None:
                        if lethe_row_data[value] != []:
                            axs[i][j].plot(lethe_row_data[value][chunk], lethe_row_data[value][chunk+1], '--', label=labels[index] if (i == 0 and j ==0 and x_value ==x_values[0]) else "", color=colors[index], linewidth = 1.2, zorder = 3, mfc = 'none') 
                            
                            if zoom_in == True:
                                sub_axes[number_of_subaxes].plot(lethe_row_data[value][chunk], lethe_row_data[value][chunk+1], '--', color=colors[index], linewidth = 1.2, zorder = 3, mfc = 'none') 
                            
                            index = index + 1
                            chunk = chunk + 2

                # Plot Breuer data
                if Breuer2009_all_data[value] != []:
                    axs[i][j].plot(Breuer2009_all_data[value][0], Breuer2009_all_data[value][1], ':', color="k", linewidth = 1.2,
                                label='LESOCC - Breuer 2009' if (i == 0 and j ==0 and x_value ==x_values[0]) else "", zorder = 2)
                    if zoom_in == True:
                        sub_axes[number_of_subaxes].plot(Breuer2009_all_data[value][0], Breuer2009_all_data[value][1], ':', color="k", linewidth = 1.2, zorder = 2)

                # Plot Rapp data
                if Rapp2009_all_data != []:
                    axs[i][j].plot(Rapp2009_all_data[value][0], Rapp2009_all_data[value][1], '-', color="k", linewidth = 1.2,
                               label = 'Experimental - Rapp 2009' if (i == 0 and j ==0 and x_value ==x_values[0]) else "",zorder = 1)
                    if zoom_in == True:
                        sub_axes[number_of_subaxes].plot(Rapp2009_all_data[value][0], Rapp2009_all_data[value][1], '-', color="k", linewidth = 1.2,zorder = 1)               

            axs[i][j].set(xlabel=x_labels[value]) #,ylabel="$y/h$") 
            value = value + 1
            number_of_subaxes = number_of_subaxes + 1

    if zoom_in == True:

        # Fix limits for zoom in plots depending on data type  x =([x1,x2],[x1,x2],[x1,x2],[x1,x2])    
        if data_type == "average_velocity_0":
            x_lims = [[-0.2,0.1],[-0.3,0],[-0.2,0.1],[0,0.2]]*nrows
            y_lims =([0.8,1.1],[0,0.3],[0, 0.3],[0, 0.3])*nrows 
        elif data_type == "reynolds_normal_stress_0":
            x_lims =([0,0.02],[0.01,0.03],[0,0.05],[0,0.05])*nrows
            y_lims =([0.8,1.0],[0,0.2],[2.5,3.1],[2.5,3.1])*nrows
        elif data_type == "reynolds_shear_stress_uv":
            x_lims =([-0.01,0],[-0.01,0],[-0.005,0.005],[-0.005,0.005])*nrows 
            y_lims =([0.8,1],[0,0.2],[2.8,3.1],[2.8,3.1])*nrows
        else:
            print("Zoom in plots not implemented for this data type.")
            exit()

        for index in range(nrows*ncols):
            sub_axes[index].set_xlim(x_lims[index]); sub_axes[index].set_ylim(y_lims[index])
            sub_axes[index].set_yticks([])
            sub_axes[index].set_xticks([])

        index = 0
        for i in range(nrows):
            for j in range(ncols):
                x1 = x_lims[index][0]; x2=x_lims[index][1]; y1=y_lims[index][0]; y2=y_lims[index][1]
                axs[i][j].add_patch(patches.Rectangle((x1,y1),(x2-x1),(y2-y1),linewidth=0.5, edgecolor='gray', facecolor = 'none'))
                line1 = ConnectionPatch(xyA=(x2 - (x2-x1)/2, y2), coordsA=axs[i][j].transData, xyB=(x1 + (x2-x1)/2, y1), coordsB=sub_axes[index].transData, color = 'gray',linewidth=0.5, arrowstyle ="->", zorder = 0)
                axs[i][j].add_artist(line1)
                index = index + 1

                if data_type == "average_velocity_0":
                    axs[i][j].xaxis.set_major_locator(ticker.MultipleLocator(0.3))
                    axs[i][j].yaxis.set_major_locator(ticker.MultipleLocator(0.5))
                    axs[i][j].set_xlim([-0.25,1.25])
                    axs[i][j].set_ylim([-0.05, 3.1])
                elif data_type == "reynolds_normal_stress_0":
                    axs[i][j].xaxis.set_major_locator(ticker.MultipleLocator(0.04))
                    axs[i][j].yaxis.set_major_locator(ticker.MultipleLocator(0.5))
                    axs[i][j].set_xlim([-0.01,0.14])
                    axs[i][j].set_ylim([-0.05, 3.1])
                elif data_type == "reynolds_shear_stress_uv":
                    axs[i][j].xaxis.set_major_locator(ticker.MultipleLocator(0.02))
                    axs[i][j].yaxis.set_major_locator(ticker.MultipleLocator(0.5))
                    axs[i][j].set_xlim([-0.05,0.01])
                    axs[i][j].set_ylim([-0.05, 3.1])

    # Set size, legend, titles
    fig.set_size_inches(11,12)
    lgd = fig.legend(loc='lower center', ncol = 4, bbox_to_anchor=(0.5, 0.005), bbox_transform = plt.gcf().transFigure, facecolor = 'white', framealpha = 0.75,  edgecolor = 'black', fancybox = False, shadow = False)

    label_of_rows =["Coarse \ (250K)", "Regular \ (1M)", "Fine \ (4M)"]
    for i in range(nrows):
        axs[i][0].set_title(r"$\underline{\bf{" + label_of_rows[i] + "}}$", loc='left', x = -0.35, y = 1.07)
        axs[i][0].set(ylabel="$y/h$")

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.15)
    fig.subplots_adjust(hspace=0.65)

    if save_figure == False:
        plt.show()
    elif zoom_in == False and save_figure == True:
        fig.savefig(folder_to_save_png + "graph_" + data_type + "_x_time_averaging_t=" + str(time_step) + "_horizontal.eps",dpi=800)
    else:
        fig.savefig(folder_to_save_png + "graph_" + data_type + "_x_time_averaging_t=" + str(time_step) + "_with_zoom_in_horizontal.eps",dpi=800)


########################################################################################################################
# RUN FUNCTIONS

# Verify the number of labels is right
assert len(labels) == len(file_names_lethe_data), f"It seems to have {len(file_names_lethe_data)} Lethe data files and you gave " \
                            f"{len(labels)} labels, please verify your labels names."

assert len(labels) == len(file_names_lethe_data_2), f"It seems to have {len(file_names_lethe_data_2)} Lethe data files and you gave " \
                            f"{len(labels)} labels, please verify your labels names."

assert len(labels) == len(file_names_lethe_data_3), f"It seems to have {len(file_names_lethe_data_3)} Lethe data files and you gave " \
                            f"{len(labels)} labels, please verify your labels names."

# Collect all data types at each x_value
if all_data is True:
    # data_type_available = ["average_velocity_0", "average_velocity_1", "reynolds_normal_stress_0",
                        #    "reynolds_normal_stress_1", "reynolds_shear_stress_uv", "reynolds_normal_stress_2"]   # turbulent_kinetic_energy
    # x_available = [0.05, 0.5, 1, 2, 3, 4, 5, 6, 7, 8]
    data_type_available = ["average_velocity_0", "reynolds_normal_stress_0", "reynolds_shear_stress_uv"]
    x_available = [0.5, 2, 4, 6]

    # for x in x_available:
    for flow_property in data_type_available:
        [Breuer2009_all_data, Rapp2009_all_data, lethe_all_data, lethe_all_data_2, lethe_all_data_3] = obtain_data(x_available, path_to_literature_data, path_to_lethe_data, file_names_lethe_data, file_names_lethe_data_2, file_names_lethe_data_3, flow_property)
        plot_to_png(Breuer2009_all_data, Rapp2009_all_data, lethe_all_data, lethe_all_data_2, lethe_all_data_3, flow_property, x_available, labels, folder_to_save_png, time_step)

print("--- %s seconds ---" % (time.time() - start_time))