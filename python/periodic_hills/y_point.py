"""
Name   : y_point.py
Author : Audrey Collard-Daigneault
Date   : 16-12-2020
Desc   : This code plots the non-dimensional wall distance (y+) at the lower wall.
         NOTE : yes, this may take a while if your csv files are super duper big :)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

############################# FILL OUT THIS PART #################################
# Reynolds number of the simulation (Currently available for Re = 5600 only)
Re = 5600

# Information about the lethe data
path_to_lethe_data = "C:/Users/Acdai/OneDrive - polymtl.ca/Polytechnique/Session A2020/" \
                     "Periodic Hills Benchmark Case/Data/data_simulation/reynolds_5600/"
file_names_lethe_data = ["data_3"]  # add all lethe files in this list

# Information about the literature data
path_to_literature_data = "C:/Users/Acdai/OneDrive - polymtl.ca/Polytechnique/Session A2020/" \
                          "Periodic Hills Benchmark Case/Data/data_literature/reynolds_5600/"

# Saving file type ("graph" or "csv")
file_type = "csv"

# Path to save graph or csv
path_to_save = "C:/Users/Acdai/OneDrive - polymtl.ca/Polytechnique/Session A2020/" \
               "Periodic Hills Benchmark Case/Data/graph/"
name_to_save = "yplus"

# Label for Lethe data for the legend
# NOTE : make sure the number of labels are the same that the number of files names of lethe data
labels = ["Lethe - ~1M cells - full simulation"]

##################################################################################

# Verify the number of labels is right
assert len(labels) == len(
    file_names_lethe_data), f"It seems to have {len(file_names_lethe_data)} Lethe data files and you gave " \
                            f"{len(labels)} labels, please verify your labels names."

# Colors for ploting
colors = ["xkcd:crimson", "xkcd:bright blue", "xkcd:dark lavender", "xkcd:pale orange"]

# Array initiation for files
lethe_csv = []
lethe_data = []
y_plus_per_file = []
x_per_file = []

# Reading Lethe data and sort them by x values
for file_nb, lethe_file in enumerate(file_names_lethe_data):
    lethe_csv = path_to_lethe_data + lethe_file + ".csv"
    lethe_data = pd.read_csv(lethe_csv, usecols=["Points_0", "Points_1", "average_velocity_0"], sep=",").sort_values(
        "Points_0")

    u_values = []
    nb_z_point = []
    point_y = []
    point_x = []
    unique_x = np.unique(lethe_data["Points_0"])

    for x in unique_x:
        x_data = lethe_data.loc[(np.abs(lethe_data["Points_0"] - x) < 1e-6)].sort_values("Points_1")

        # Get the 3 points in y direction for Lagrange polynome
        count = 0
        y_value = -1
        for i, y in x_data["Points_1"].iteritems():
            if ~np.isclose(y, y_value):
                count += 1
                if count <= 3:
                    u_values.append(0)
                    nb_z_point.append(0)
                    point_x.append(x)
                    point_y.append(y)

            if count <= 3:
                u_values[-1] += x_data["average_velocity_0"][i]
                nb_z_point[-1] += 1

            y_value = y

        # Progression
        max_x = np.max(unique_x)
        print(
            f"Estimated progression {round((x + file_nb * max_x) / ((file_nb + 1) * max_x) * 100, 2)}%")

    # Average time-averaged values in z direction
    u_values = np.array(u_values) / np.array(nb_z_point)

    # Initiate variables
    dudy = []
    viscosity = 1.78571E-04
    y_plus = []
    x = []

    # Calculate du/dy at wall with Lagrange polynome derivatives and the non-dimensional wall distance
    for i in range(0, len(u_values), 3):
        poly = lagrange(np.array(point_y[i:i + 3]), np.array(u_values[i:i + 3]))
        poly_diff = np.polyder(poly)
        dudy.append(poly_diff(point_y[i]))
        dy = point_y[i + 1] - point_y[i]
        y_plus.append(np.sqrt(np.abs(dudy[-1] * viscosity)) * (dy / 2) / viscosity)
        x.append(point_x[i])

    y_plus_per_file.append(y_plus)
    x_per_file.append(x)

# Literature data from Breuer2009
breuer2009_csv = path_to_literature_data + "Breuer2009/Breuer2009_27.csv"
literature_data = pd.read_csv(breuer2009_csv, usecols=["x", "Curve27"], sep=",")
literature_name = "Simulation LESOCC - Breuer 2009"

if file_type == "graph":
    fig, ax = plt.subplots()

    for i, lethe_file in enumerate(file_names_lethe_data):
        name = labels[i]
        color = colors[i]
        ax.plot(x_per_file[i], y_plus_per_file[i], color=color, label=name)
    ax.plot(literature_data["x"], literature_data["Curve27"], '--', color='xkcd:green', label=literature_name)
    ax.set_title("Distribution of $y^{+}$ along the lower wall at Re = " + str(Re))
    ax.set_xlabel("$x/h$")
    ax.set_ylabel("$y^{+}$")
    ax.legend()
    fig.savefig(path_to_save + name_to_save + ".png")
    plt.show()
    plt.close(fig)
    ax.clear()
elif file_type == "csv":
    # Find the max value of the array length
    data_size = []
    data_size.append(literature_data[0].shape[0])
    for i in range(0, len(file_names_lethe_data)):
        data_size.append(len(y_plus_per_file[i]))

    index_max_size = np.max(np.array(data_size))
    arrays_to_dataframe = pd.DataFrame(index=range(1, index_max_size))

    for i, lethe_file in enumerate(file_names_lethe_data):
        arrays_to_dataframe.loc[:, 'x_' + lethe_file] = pd.Series(x_per_file[i])
        arrays_to_dataframe.loc[:, 'yplus_' + lethe_file] = pd.Series(y_plus_per_file[i])

    arrays_to_dataframe.loc[:, "yplus_Breuer2009"] = pd.Series(literature_data["Curve27"])
    arrays_to_dataframe.loc[:, "y_Breuer2009"] = pd.Series(literature_data["x"])

    arrays_to_dataframe.to_csv(path_to_save + name_to_save + ".csv", index=False, header=True)
