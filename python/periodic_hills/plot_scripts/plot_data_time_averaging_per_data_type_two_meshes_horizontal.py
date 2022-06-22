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

########################################################################################################################
# Function to retrieve data from .csv files
def obtain_data(x_values, path_to_literature_data, path_to_lethe_data, file_names_lethe_data, file_names_lethe_data_2, data_type):

    index = 0
    Rapp2009_all_data = list()
    Breuer2009_all_data = list()
    Lethe_all_data = list()
    Lethe_all_data_2 = list()

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

        Lethe_data=list()
        for file in file_names_lethe_data:
            Lethe_data_csv = path_to_lethe_data + '_Lethe_data_' + str(file) + '_' + str(data_type) + '_x_' + str(x_value) + '.csv'
            Lethe_data_loc = pandas.read_csv(Lethe_data_csv)
            Lethe_data_loc = Lethe_data_loc.to_numpy()
            Lethe_data_loc = numpy.delete(Lethe_data_loc, 0, 1)
            Lethe_data.extend(Lethe_data_loc)
        Lethe_all_data.append(Lethe_data)

        Lethe_data_2=list()
        for file in file_names_lethe_data_2:
            Lethe_data_csv = path_to_lethe_data + '_Lethe_data_' + str(file) + '_' + str(data_type) + '_x_' + str(x_value) + '.csv'
            Lethe_data_loc = pandas.read_csv(Lethe_data_csv)
            Lethe_data_loc = Lethe_data_loc.to_numpy()
            Lethe_data_loc = numpy.delete(Lethe_data_loc, 0, 1)
            Lethe_data_2.extend(Lethe_data_loc)
        Lethe_all_data_2.append(Lethe_data_2)
        
    # print(Breuer2009_all_data)
    return Breuer2009_all_data, Rapp2009_all_data, Lethe_all_data, Lethe_all_data_2

# Plot literature values against Lethe values
def plot_to_png(Breuer2009_all_data, Rapp2009_all_data, lethe_all_data, lethe_all_data_2, data_type, x_values, labels,
                folder_to_save_png, time_step):
    # Plotting results
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.family']='DejaVu Serif'
    plt.rcParams['font.serif']='cm'
    plt.rcParams['font.size'] = 12

    fig, axs = plt.subplots(2, 4)

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
            location = 'center left'
        elif data_type == "reynolds_normal_stress_0":
            location = 'upper right'
        elif data_type == "reynolds_shear_stress_uv":
            location = 'upper left'
        else:
            location = 'upper right'

        sub_axes = list()
        sub_axes.append(inset_axes(axs[0][0], height = "30%", width = "30%", loc = location))
        sub_axes.append(inset_axes(axs[0][1], height = "30%", width = "30%", loc = location))
        sub_axes.append(inset_axes(axs[0][2], height = "30%", width = "30%", loc = location))
        sub_axes.append(inset_axes(axs[0][3], height = "30%", width = "30%", loc = location))
        sub_axes.append(inset_axes(axs[1][0], height = "30%", width = "30%", loc = location))
        sub_axes.append(inset_axes(axs[1][1], height = "30%", width = "30%", loc = location))
        sub_axes.append(inset_axes(axs[1][2], height = "30%", width = "30%", loc = location))
        sub_axes.append(inset_axes(axs[1][3], height = "30%", width = "30%", loc = location))

    value = 0
    number_of_subaxes = 0
    for i in range(1):
        for j in range(4):
            for x_value in x_values:     
                # Plot Lethe data
                index = 0
                chunk = 0
                for file_name in file_names_lethe_data:
                    if file_name is not None:
                        if lethe_all_data[value] != []:
                            if(i == 0 and j == 0 and x_value == x_values[0]):
                                axs[i][j].plot(lethe_all_data[value][chunk], lethe_all_data[value][chunk+1], '--', label=labels[index] , color=colors[index], linewidth = 1.2, zorder = 3, mfc = 'none') 
                                if zoom_in == True:
                                    sub_axes[number_of_subaxes].plot(lethe_all_data[value][chunk], lethe_all_data[value][chunk+1], '--', color=colors[index], linewidth = 1.2, zorder = 3, mfc = 'none')                                 
                            else:
                                axs[i][j].plot(lethe_all_data[value][chunk], lethe_all_data[value][chunk+1], '--', color=colors[index], linewidth = 1.2, zorder = 3, mfc = 'none') 
                                if zoom_in == True:
                                    sub_axes[number_of_subaxes].plot(lethe_all_data[value][chunk], lethe_all_data[value][chunk+1], '--', color=colors[index], linewidth = 1.2, zorder = 3, mfc = 'none') 
                           
                            index = index + 1
                            chunk = chunk + 2

                # Plot Breuer data
                if Breuer2009_all_data[value] != []:
                    if(i == 0 and j == 0 and x_value == x_values[0]):
                        axs[i][j].plot(Breuer2009_all_data[value][0], Breuer2009_all_data[value][1], ':', color="k", linewidth = 1.2,
                                label='LESOCC - Breuer 2009', zorder = 2)
                        if zoom_in == True:
                            sub_axes[number_of_subaxes].plot(Breuer2009_all_data[value][0], Breuer2009_all_data[value][1], ':', color="k", linewidth = 1.2, zorder = 2)
                    else:
                        axs[i][j].plot(Breuer2009_all_data[value][0], Breuer2009_all_data[value][1], ':', color="k", linewidth = 1.2, zorder = 2)
                        if zoom_in == True:
                            sub_axes[number_of_subaxes].plot(Breuer2009_all_data[value][0], Breuer2009_all_data[value][1], ':', color="k", linewidth = 1.2, zorder = 2)

                # Plot Rapp data
                if Rapp2009_all_data != []:
                    if(i == 0 and j == 0 and x_value == x_values[0]):
                        axs[i][j].plot(Rapp2009_all_data[value][0], Rapp2009_all_data[value][1], '-', color="k", linewidth = 1.2,
                                label = 'Experimental - Rapp 2009',zorder = 1)
                        if zoom_in == True:
                            sub_axes[number_of_subaxes].plot(Rapp2009_all_data[value][0], Rapp2009_all_data[value][1], '-', color="k", linewidth = 1.2,zorder = 1)               

                    else:
                        axs[i][j].plot(Rapp2009_all_data[value][0], Rapp2009_all_data[value][1], '-', color="k", linewidth = 1.2,zorder = 1)               
                        if zoom_in == True:
                            sub_axes[number_of_subaxes].plot(Rapp2009_all_data[value][0], Rapp2009_all_data[value][1], '-', color="k", linewidth = 1.2,zorder = 1)               

            axs[i][j].set(xlabel=x_labels[value]) #,ylabel="$y/h$") 
            value = value + 1
            number_of_subaxes = number_of_subaxes + 1

    value = 0
    number_of_subaxes = 4
    for i in range(1,2):
        for j in range(4):
            for x_value in x_values:
                # Plot Lethe data
                index = 0
                chunk = 0
                for file_name in file_names_lethe_data:
                    if file_name is not None:
                        if lethe_all_data_2[value] != []:
                            axs[i][j].plot(lethe_all_data_2[value][chunk], lethe_all_data_2[value][chunk+1], '--', color=colors[index], linewidth = 1.2, zorder = 3, mfc = 'none') 
                            if zoom_in == True:                                
                                sub_axes[number_of_subaxes].plot(lethe_all_data_2[value][chunk], lethe_all_data_2[value][chunk+1], '--', color=colors[index], linewidth = 1.2, zorder = 3, mfc = 'none') 

                            index = index + 1
                            chunk = chunk + 2

                # Plot Breuer data
                if Breuer2009_all_data[value] != []:
                    axs[i][j].plot(Breuer2009_all_data[value][0], Breuer2009_all_data[value][1], ':', color="k", linewidth = 1.2, zorder = 2)
                    if zoom_in == True:
                        sub_axes[number_of_subaxes].plot(Breuer2009_all_data[value][0], Breuer2009_all_data[value][1], ':', color="k", linewidth = 1.2, zorder = 2)

                # Plot Rapp data
                if Rapp2009_all_data != []:
                    axs[i][j].plot(Rapp2009_all_data[value][0], Rapp2009_all_data[value][1], '-', color="k", linewidth = 1.2,zorder = 1)               
                    if zoom_in == True:
                        sub_axes[number_of_subaxes].plot(Rapp2009_all_data[value][0], Rapp2009_all_data[value][1], '-', color="k", linewidth = 1.2,zorder = 1)               

            axs[i][j].set(xlabel=x_labels[value]) #,ylabel="$y/h$") 
            value = value + 1
            number_of_subaxes = number_of_subaxes + 1

    if zoom_in == True:

        # Fix limits for zoom in plots depending on data type    
        if data_type == "average_velocity_0":
            x_lims =([-0.2,0.1],[-0.3,0],[-0.2,0.1],[0,0.2],[-0.2,0.1],[-0.3,0],[-0.2,0.1],[0,0.2]) 
            y_lims =([0.8,1.1],[0,0.3],[0, 0.3],[0, 0.3],[0.8,1.1],[0,0.3],[0, 0.3],[0, 0.3]) 
            for index in range(8):
                sub_axes[index].set_xlim(x_lims[index]); sub_axes[index].set_ylim(y_lims[index])
                # sub_axes[i].yaxis.tick_right()
                sub_axes[index].set_yticks([])
                sub_axes[index].set_xticks([])
            index = 0
            for i in range(2):
                for j in range(4):
                    x1 = x_lims[index][0]; x2=x_lims[index][1]; y1=y_lims[index][0]; y2=y_lims[index][1]
                    axs[i][j].add_patch(patches.Rectangle((x1,y1),(x2-x1),(y2-y1),linewidth=0.5, edgecolor='gray', facecolor = 'none'))
                    line1 = ConnectionPatch(xyA=(x2 - (x2-x1)/2, y2), coordsA=axs[i][j].transData, xyB=(x1 + (x2-x1)/2, y1), coordsB=sub_axes[index].transData, color = 'gray',linewidth=0.5, arrowstyle ="->", zorder = 0)
                    axs[i][j].add_artist(line1)
                    index = index + 1
                    axs[i][j].xaxis.set_major_locator(ticker.MultipleLocator(0.3))
                    axs[i][j].yaxis.set_major_locator(ticker.MultipleLocator(0.5))
                    axs[i][j].set_xlim([-0.25,1.25])
                    axs[i][j].set_ylim([-0.05, 3.1])
    
        elif data_type == "reynolds_normal_stress_0":
            x_lims =([0,0.02],[0.01,0.03],[0,0.05],[0,0.05], [0,0.02],[0.01,0.03],[0,0.05],[0,0.05]) 
            y_lims =([0.8,1.0],[0,0.2],[2.5,3.1],[2.5,3.1], [0.8,1.0],[0,0.2],[2.5,3.1],[2.5,3.1])
            for index in range(8):
                sub_axes[index].set_xlim(x_lims[index]); sub_axes[index].set_ylim(y_lims[index])
                # sub_axes[i].yaxis.tick_right()
                sub_axes[index].set_yticks([])
                sub_axes[index].set_xticks([])
            index = 0
            for i in range(2):
                for j in range(4):
                    x1 = x_lims[index][0]; x2=x_lims[index][1]; y1=y_lims[index][0]; y2=y_lims[index][1]
                    axs[i][j].add_patch(patches.Rectangle((x1,y1),(x2-x1),(y2-y1),linewidth=0.5, edgecolor='gray', facecolor = 'none'))
                    line1 = ConnectionPatch(xyA=(x2, y2 - (y2-y1)/2), coordsA=axs[i][j].transData, xyB=(x1, y1 + (y2-y1)/2), coordsB=sub_axes[index].transData, color = 'gray',linewidth=0.5, arrowstyle ="->", zorder = 0)
                    axs[i][j].add_artist(line1)
                    index = index + 1
                    axs[i][j].xaxis.set_major_locator(ticker.MultipleLocator(0.04))
                    axs[i][j].yaxis.set_major_locator(ticker.MultipleLocator(0.5))
                    axs[i][j].set_xlim([-0.01,0.14])
                    axs[i][j].set_ylim([-0.05, 3.1])
    
        elif data_type == "reynolds_shear_stress_uv":
            # x =([x1,x2],[x1,x2],[x1,x2],[x1,x2]) x limits for each subplot
            x_lims =([-0.01,0],[-0.01,0],[-0.005,0.005],[-0.005,0.005], [-0.01,0],[-0.01,0],[-0.005,0.005],[-0.005,0.005]) 
            y_lims =([0.8,1],[0,0.2],[2.8,3.1],[2.8,3.1], [0.8,1],[0,0.2],[2.8,3.1],[2.8,3.1]) 
            for index in range(8):
                sub_axes[index].set_xlim(x_lims[index]); sub_axes[index].set_ylim(y_lims[index])
                # sub_axes[i].yaxis.tick_right()
                sub_axes[index].set_yticks([])
                sub_axes[index].set_xticks([])
            index = 0
            for i in range(2):
                for j in range(4):
                    x1 = x_lims[index][0]; x2=x_lims[index][1]; y1=y_lims[index][0]; y2=y_lims[index][1]
                    axs[i][j].add_patch(patches.Rectangle((x1,y1),(x2-x1),(y2-y1),linewidth=0.5, edgecolor='gray', facecolor = 'none'))
                    line1 = ConnectionPatch(xyA=(x1, y2 - (y2-y1)/2), coordsA=axs[i][j].transData, xyB=(x2, y1 + (y2-y1)/2), coordsB=sub_axes[index].transData, color = 'gray',linewidth=0.5, arrowstyle ="->", zorder = 0)
                    axs[i][j].add_artist(line1)
                    index = index + 1
                    axs[i][j].xaxis.set_major_locator(ticker.MultipleLocator(0.02))
                    axs[i][j].yaxis.set_major_locator(ticker.MultipleLocator(0.5))
                    axs[i][j].set_xlim([-0.05,0.01])
                    axs[i][j].set_ylim([-0.05, 3.1])
    
        else:
            sub_axes[0].set_xlim([0,1]); sub_axes[0].set_ylim([0,1])
            sub_axes[1].set_xlim([0,1]); sub_axes[1].set_ylim([0,1])
            sub_axes[2].set_xlim([0,1]); sub_axes[2].set_ylim([0,1])
            sub_axes[3].set_xlim([0,1]); sub_axes[3].set_ylim([0,1])

    fig.set_size_inches(11,8)
    # fig.set_size_inches(9,7)
    lgd = fig.legend(loc='lower center', ncol = 4, bbox_to_anchor=(0.5, 0.005), bbox_transform = plt.gcf().transFigure, facecolor = 'white', framealpha = 0.75,  edgecolor = 'black', fancybox = False, shadow = False)
    # lgd = fig.legend(loc='right',bbox_to_anchor=(1.0, 0.5), bbox_transform = plt.gcf().transFigure, facecolor = 'white', framealpha = 0.75,  edgecolor = 'black', fancybox = False, shadow = False)
    axs[0][0].set_title(r"$\underline{\bf{" + "Coarse (250K)" + "}}$", loc='left', x = -0.25, y = 1.07)
    axs[1][0].set_title(r"$\underline{\bf{" + "Fine (1M)" + "}}$", loc='left', x = -0.25, y = 1.07)
    axs[0][0].set(ylabel="$y/h$")
    axs[1][0].set(ylabel="$y/h$")
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.16)
    # fig.subplots_adjust(right=0.7)
    if zoom_in == False:
        fig.savefig(folder_to_save_png + "graph_" + data_type + "_x_time_averaging_t=" + str(time_step) + "_horizontal.eps",dpi=800)
    else:
        fig.savefig(folder_to_save_png + "graph_" + data_type + "_x_time_averaging_t=" + str(time_step) + "_with_zoom_in_horizontal.eps",dpi=800)

    # plt.show()


########################################################################################################################
# RUN FUNCTIONS

# Verify the number of labels is right
assert len(labels) == len(file_names_lethe_data), f"It seems to have {len(file_names_lethe_data)} Lethe data files and you gave " \
                            f"{len(labels)} labels, please verify your labels names."

assert len(labels) == len(file_names_lethe_data_2), f"It seems to have {len(file_names_lethe_data_2)} Lethe data files and you gave " \
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
        [Breuer2009_all_data, Rapp2009_all_data, lethe_all_data, lethe_all_data_2] = obtain_data(x_available, path_to_literature_data, path_to_lethe_data, file_names_lethe_data, file_names_lethe_data_2, flow_property)
        plot_to_png(Breuer2009_all_data, Rapp2009_all_data, lethe_all_data, lethe_all_data_2, flow_property, x_available, labels, folder_to_save_png, time_step)

print("--- %s seconds ---" % (time.time() - start_time))

