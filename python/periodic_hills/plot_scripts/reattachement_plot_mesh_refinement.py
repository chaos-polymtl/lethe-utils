# Name   : reattachment_plot_mesh_refinement.py
# Author : Laura Prieto Saavedra (Adpated from Catherine Radburn and Audrey Collard-Daigneault)
# Date   : 22-06-2021
# Desc   : This code plots simulation data from Lethe and other data from literature.
#           It loads .csv files and plot data into a .png file. Displaying the title is optional.
#           If all x_value and data_type available are required, ignore x_value and data_type in lines 46 and 49, and
#           make all_data = True.
#           On line 350, a tolerance is specified. This may need to be varied if too little/too much data is plotted.

import pandas
import numpy
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches
from matplotlib.patches import ConnectionPatch
from pathlib import Path
import math 
import time

start_time = time.time()

########################################################################################################################
# SET VARIABLES

#This information is obtained by running the near_wall_processing.py script for every simulation

mesh_labels = ["Lethe - 250K", "Lethe - 500K", "Lethe - 1M", "Lethe - 4M"]

#Reattachement points at different averaging times.
#250K
reattachment_points_1 = [5.11776931156123, 5.09686651116088, 5.045595935082811, 5.039710668073614, 5.059829429669876, 5.079026106079334]
average_times_1 = [500, 600, 700, 800, 900, 1000] 

#500K
reattachment_points_2 = [4.632744089624518, 4.632911085716633, 4.625248808252732, 4.628748473476688, 4.6306247666503495, 4.65011904021285]
average_times_2 = [500, 600, 700, 800, 900, 1000] 

#1M
reattachment_points_3 = [4.929045392294163, 4.89558853808692, 4.896752607702034, 4.8661037487483805, 4.8181314809444125, 4.803963093638626]
average_times_3 = [500, 600, 700, 800, 900, 1000] 

#4M
# reattachment_points_4 = [4.82322082908, 4.809037746, 4.8116936081221, 4.83547590569519, 4.82277937063245] #Old
reattachment_points_4 = [4.906411955197181, 4.870164512002711, 4.820498723025258, 4.8443378030659651, 4.860565672666695, 4.835132662030343]
average_times_4 = [500, 600, 700, 800, 900, 1000]

reattachment_points = [reattachment_points_1, reattachment_points_2, reattachment_points_3, reattachment_points_4]
average_times = [average_times_1, average_times_2, average_times_3, average_times_4]

# Save graph.png 
folder_to_save_png = "../conference_figure/"
# folder_to_save_png = "../journal_im/"
Path(folder_to_save_png).mkdir(parents=True, exist_ok=True)

########################################################################################################################

def plot_reattachment_points(reattachment_points, average_times, folder_to_save_png, mesh_labels):
    
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.family']='DejaVu Serif'
    plt.rcParams['font.serif']='cm'
    plt.rcParams['font.size'] = 16

    fig, ax = plt.subplots()

    markers = ["s", "o", "P", "*", "X"]
    colors = ["xkcd:blue", "xkcd:lime green", "xkcd:red", "xkcd:orange", "xkcd:pumpkin", "xkcd:gold"]    
    # colors = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494"]
    #Plot Lethe data
    index = 0
    for reattachment_point in reattachment_points:
        average_times_flows_through = list()
        for time in average_times[index]:
            average_times_flows_through.append((time - 207)/9)

        ax.scatter(average_times_flows_through, reattachment_point, marker = markers[index], label = mesh_labels[index], color = colors[index], s = 18)
        index = index + 1
    
    #Plot lethe error
    reattachment_point_average = [5.07, 4.63, 4.86, 4.85]
    constant = [0.5, 0.5, 0.5, 0.4]
    error_flow_through = numpy.linspace(1,146, num = 145)

    index = 0
    for reattachment_point in reattachment_point_average:
        error_reattachment_points_1 = list()
        error_reattachment_points_2 = list()
        for flow_through in error_flow_through:
            error = constant[index]/math.sqrt(flow_through)
            error_reattachment_points_1.append(reattachment_point + error)
            error_reattachment_points_2.append(reattachment_point - error)

        ax.plot(error_flow_through, error_reattachment_points_1, ':', color = colors[index], linewidth = 1.2)
        ax.plot(error_flow_through, error_reattachment_points_2, ':', color = colors[index], linewidth = 1.2)
        index = index + 1


    # Plot previous studies
    previous_studies_reattachement_points = [5.14, 4.56, 4.72, 4.82, 5.04]
    previous_studies_flows_through = [38, 55, 55, 61, 61]

    ax.scatter(previous_studies_flows_through, previous_studies_reattachement_points, marker = "^", label = "Previous studies", s = 16, color = 'purple')
    
    # Plot Breuer's point

    breuer_reattachment_point = 5.09
    breuer_flows_through = 145

    ax.scatter(breuer_flows_through, breuer_reattachment_point, marker = "D", label = "LESOCC - Breuer 2009", s = 16, color = 'xkcd:gold')

    # Plot Rapp's line
    rapp_reattachment_point = [4.83]*146
    rapp_flow_through = range(146)

    ax.plot(rapp_flow_through, rapp_reattachment_point, "--", label = "Experimental - Rapp 2009", color = "k", linewidth = 1.2 )
    
    fig.set_size_inches(9,5)
    ax.set_xlim([0,147])
    ax.set_xlabel("Averaging time [Flows throughs]")
    ax.set_ylabel("Reattachment length [-]")
    fig.subplots_adjust(right=0.6)
    # plt.tight_layout()
    ax.legend(loc='right', bbox_to_anchor=(1.85, 0.5), facecolor = 'white', framealpha = 0.75, ncol=1, edgecolor = 'black', fancybox = False, shadow = False)
    fig.savefig(folder_to_save_png + "reattachement_point_mesh_refinement_5600_all_new.eps",dpi=800)
    # plt.show()

    # For the graphical anstract figure
    # fig.set_size_inches(6,5)
    # ax.legend(loc = "lower center", bbox_to_anchor=(0.5, -0.5), ncol = 2, facecolor = 'white', framealpha = 0.75, edgecolor = 'black', fancybox = False, shadow = False)
    # fig.subplots_adjust(bottom=0.3)
    # fig.savefig(folder_to_save_png + "reattachement_point_mesh_refinement_5600_all_graphical_abstract.eps",dpi=800)

########################################################################################################################
# RUN FUNCTIONS
plot_reattachment_points(reattachment_points, average_times, folder_to_save_png, mesh_labels)

print("--- %s seconds ---" % (time.time() - start_time))