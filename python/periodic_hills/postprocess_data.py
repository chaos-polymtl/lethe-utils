"""
Name   : postprocess_data.py
Author : Audrey Collard-Daigneault
Date   : 07-12-2020
Desc   : This code plots simulation data with Lethe and other data from literature
         got with Engauge Digitizer or text files.
         (<u>/<ub>, <v>/<ub>, <u'u'>/<ub²>, <v'v'>/<ub²>, <u'v'>/<ub²>)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


################################################ FILL OUT THIS PART ###################################################

# Reynolds number of the simulation (Currently available for Re = 5600 only)
Re = 5600

# Information about the lethe data
path_to_lethe_data = "./lethe/" \

file_names_lethe_data = ["data_3","data_5_300s","data_5_500s"]  # add all lethe files in this list

# Information about the literature data (
path_to_literature_data = "./lit/Re_5600/" \

# Path to save graphs or csv and prefix name
name_to_save = "graph_all"

folder_to_save_png="./output_png/"
Path(folder_to_save_png).mkdir(parents=True, exist_ok=True)

folder_to_save_csv="./output_csv/"
Path(folder_to_save_csv ).mkdir(parents=True, exist_ok=True)

path_to_save_png = folder_to_save_png+name_to_save
path_to_save_csv = folder_to_save_csv+name_to_save

# Label for Lethe data for the legend
# NOTE : make sure the number of labels are the same that the number of files names of lethe data
labels = ["Lethe - 1M - 720s", "Lethe - 4M - 300s","Lethe - 4M - 500s"]

# x/h position with literature data files
x_available = [0.05, 0.5, 1, 2, 3, 4, 5, 6, 7, 8]

# Extra data extraction? (<w'w'>/<ub²> for x = 0.05, 2, 4 and 8 k/<ub²> for x = 0.05, 0.5, 1, 2, 3, 4, 5, 6, 7 and 8)
extra = [True, False]


#######################################################################################################################


# Literature data extraction of files associated with x/h
def literature_data_extraction(x_value, data_type, path_to_literature_data, Re):
    assert Re == 5600, "Currently available for Re = 5600 only."

    # Setting file number to x value
    if np.isclose(x_value, 0.05):
        literature_data_nb = "01"
    elif np.isclose(x_value, 0.5):
        literature_data_nb = "02"
    elif x_value == 1:
        literature_data_nb = "03"
    elif x_value == 2:
        literature_data_nb = "04"
    elif x_value == 3:
        literature_data_nb = "05"
    elif x_value == 4:
        literature_data_nb = "06"
    elif x_value == 5:
        literature_data_nb = "07"
    elif x_value == 6:
        literature_data_nb = "08"
    elif x_value == 7:
        literature_data_nb = "09"
    elif x_value == 8:
        literature_data_nb = "10"
    else:
        literature_data_nb = None

    # Setting file number or column to data type
    if data_type == "average_velocity_0":
        literature_data_type = "u/u_b"
    elif data_type == "average_velocity_1":
        literature_data_type = "v/u_b"
    elif data_type == "reynolds_normal_stress_0":
        literature_data_type = "u'u'/u_b^2"
    elif data_type == "reynolds_normal_stress_1":
        literature_data_type = "v'v'/u_b^2"
    elif data_type == "reynolds_shear_stress_uv":
        literature_data_type = "u'v'/u_b^2"
    else:
        literature_data_type = None

    # Getting literature data
    if literature_data_nb is not None and literature_data_type is not None:
        Rapp2009_csv = path_to_literature_data + "Rapp2009_UFR3-30/Rapp2009_" + str(literature_data_nb) + ".csv"
        Rapp2009_data = pd.read_csv(Rapp2009_csv, usecols=["y/h", literature_data_type], sep=",")
        Rapp2009_data = [np.array(Rapp2009_data[literature_data_type]), np.array(Rapp2009_data["y/h"])]

        Breuer2009_csv = path_to_literature_data + "Breuer2009_UFR3-30/Breuer2009_3-30_" + str(
            literature_data_nb) + ".csv"
        Breuer2009_data = pd.read_csv(Breuer2009_csv, usecols=["y/h", literature_data_type], sep=";")
        Breuer2009_data = [np.array(Breuer2009_data[literature_data_type]), np.array(Breuer2009_data["y/h"])]
    else:
        Rapp2009_data = Breuer2009_data = None

    return Breuer2009_data, Rapp2009_data


def extra_data_extraction(x_value, data_type, path_to_literature_data, Re):
    assert Re == 5600, "Currently available for Re = 5600 only."

    # For <w'w'>/<ub²> 5 11 17 23
    rns2_data_nb = None
    if data_type == "reynolds_normal_stress_2":
        if np.isclose(x_value, 0.05):
            rns2_data_nb = "05"
        elif x_value == 2:
            rns2_data_nb = "11"
        elif x_value == 4:
            rns2_data_nb = "17"
        elif x_value == 8:
            rns2_data_nb = "23"

        if rns2_data_nb is not None:
            Breuer2009_csv = path_to_literature_data + "Breuer2009/Breuer2009_" + str(
                rns2_data_nb) + ".csv"
            Breuer2009_data = pd.read_csv(Breuer2009_csv, usecols=["x", "Curve" + str(rns2_data_nb)], sep=",")
            Breuer2009_data = [np.array(Breuer2009_data["Curve" + str(rns2_data_nb)]), np.array(Breuer2009_data["x"])]

    k_data_nb = None
    if data_type == "turbulent_kinetic_energy":
        if np.isclose(x_value, 0.05):
            k_data_nb = "01"
        elif np.isclose(x_value, 0.5):
            k_data_nb = "02"
        elif x_value == 1:
            k_data_nb = "03"
        elif x_value == 2:
            k_data_nb = "04"
        elif x_value == 3:
            k_data_nb = "05"
        elif x_value == 4:
            k_data_nb = "06"
        elif x_value == 5:
            k_data_nb = "07"
        elif x_value == 6:
            k_data_nb = "08"
        elif x_value == 7:
            k_data_nb = "09"
        elif x_value == 8:
            k_data_nb = "10"

        if k_data_nb is not None:
            Breuer2009_csv = path_to_literature_data + "Breuer2009_UFR3-30/Breuer2009_3-30_" + str(
                k_data_nb) + ".csv"
            Breuer2009_data = pd.read_csv(Breuer2009_csv, usecols=["y/h", "k/u_b^2"], sep=";")
            Breuer2009_data = [np.array(Breuer2009_data["k/u_b^2"]), np.array(Breuer2009_data["y/h"])]

    if rns2_data_nb is None and k_data_nb is None:
        Breuer2009_data = None

    return Breuer2009_data


# Verify the number of labels is right
assert len(labels) == len(
    file_names_lethe_data), f"It seems to have {len(file_names_lethe_data)} Lethe data files and you gave " \
                            f"{len(labels)} labels, please verify your labels names."


#***************************************************
# Main routine for the postprocessing
#***************************************************

# Data to graph for each x available
file_nb = 0

# Data type to plot
all_data_type = ["average_velocity_0", "average_velocity_1", "reynolds_normal_stress_0",
                 "reynolds_normal_stress_1", "reynolds_shear_stress_uv"]

# Associate x label to data type
x_labels = [r"$\langle u \rangle/u_{b}$", r"$\langle v \rangle/u_{b}$", r"$\langle u'u' \rangle/u_{b}^{2}$",
            r"$\langle v'v' \rangle/u_{b}^{2}$", r"$\langle u'v' \rangle/u_{b}^{2}$"]

# If extra data type is/are True
if extra[0] is True:
    all_data_type.append("reynolds_normal_stress_2")
    x_labels.append(r"$\langle w'w' \rangle/u_{b}^{2}$")

if extra[1] is True:
    all_data_type.append("turbulent_kinetic_energy")
    x_labels.append(r"k/u_{b}^{2}$")

# Reading Lethe data
lethe_csv = []
lethe_data = []
for lethe_file in file_names_lethe_data:
    lethe_csv.append(path_to_lethe_data + lethe_file + ".csv")
    lethe_data.append(pd.read_csv(lethe_csv[-1], usecols=["Points_0", "Points_1"] + all_data_type, sep=","))

# A plot for every x value and data type
for x_value in x_available:
    for index_data_type, data_type in enumerate(all_data_type):
        # Processing Lethe data
        data_to_plot = []
        y_to_plot = []
        for data in lethe_data:
            # Taking data of x value and data type and sorting it for y
            data = data[["Points_0", "Points_1", data_type]]
            y_data = data.loc[(np.abs(data["Points_0"] - x_value) < 1e-6)]

            # If there's no data at x_values, it does using the 2 nearest x
            nb_unique_x = len(np.unique(y_data["Points_0"]))
            if nb_unique_x != 1:
                # Find all x in tolerance = 0.1
                if nb_unique_x < 1:
                    y_data = data.loc[(np.abs(data["Points_0"] - x_value) < 0.1)]

                # Get index of value by sorted difference with x_value
                unique_values = np.unique(y_data["Points_0"])
                delta = np.abs(unique_values - x_value)
                index_sorted_delta = np.argsort(delta)

                # Find the values min and max related to the x_value
                min_x_value = max_x_value = None

                for index in index_sorted_delta:
                    if unique_values[index] < x_value and min_x_value is None:
                        min_x_value = unique_values[index]
                    elif unique_values[index] > x_value and max_x_value is None:
                        max_x_value = unique_values[index]

                y_data_min = data.loc[(np.abs(data["Points_0"] - min_x_value) < 1e-6)]
                y_data_max = data.loc[(np.abs(data["Points_0"] - max_x_value) < 1e-6)]
                y_data = pd.DataFrame(data=y_data_max, columns=y_data_max.columns, index=y_data_max.index)

                # Linear interpolation : u = (u_2 - u_1) * (x - x_1) / (x2 - x1) + u_1
                y_data[data_type].sub(y_data_min[data_type])
                y_data[data_type].mul((x_value - min_x_value) / (max_x_value - min_x_value))
                y_data[data_type].add(y_data_min[data_type])

            y_data = y_data.sort_values("Points_1")

            # Initialization of arrays prior processing
            data_type_values = np.zeros(1)
            y_values = np.zeros(1)
            nb_z_point = np.zeros(1)  # to count number of points in z axis for each y for the average

            # Initialization of some values prior processing
            last_y = y_data["Points_1"].iloc[0]  # first y point
            y_values[0] = last_y

            # Averaging data in the z axis for each y point
            for index, y in y_data["Points_1"].iteritems():
                if ~np.isclose(y, last_y):  # next y point
                    data_type_values = np.append(data_type_values, 0)
                    nb_z_point = np.append(nb_z_point, 0)
                    y_values = np.append(y_values, y)

                data_type_values[-1] += y_data[data_type][index]
                nb_z_point[-1] += 1
                last_y = y

            data_type_values /= nb_z_point

            data_to_plot.append(data_type_values)
            y_to_plot.append(y_values)

        # Taking literature data
        [Breuer2009_data, Rapp2009_data] = literature_data_extraction(x_value, data_type, path_to_literature_data,
                                                                      Re)

        if data_type == "reynolds_normal_stress_2" or data_type == "turbulent_kinetic_energy":
            Breuer2009_data = extra_data_extraction(x_value, data_type, path_to_literature_data, Re)

        file_nb += 1

        # Plotting results
        fig, ax = plt.subplots()

        # If there's Lethe data for this x and this data type
        line_type = '-'  # solid line for the first set of data
        for index, name in enumerate(labels):
            if data_to_plot[index] is not None:
                ax.plot(data_to_plot[index], y_to_plot[index], line_type, label=name)
                line_type = '--'  # dashed lines for other Lethe data

        if Breuer2009_data is not None:
            ax.plot(Breuer2009_data[0], Breuer2009_data[1], '--', color='xkcd:scarlet',
                    label='Simulation LESOCC - Breuer 2009')

        if Rapp2009_data is not None:
            ax.plot(Rapp2009_data[0], Rapp2009_data[1], '--', color='xkcd:black',
                    label='Experimental - Rapp 2009')

        ax.set_title(data_type + " at Re = " + str(Re) + " at x = " + str(x_value))
        ax.set_xlabel(x_labels[index_data_type])
        ax.set_ylabel("$y/h$")
        ax.legend()
        fig.savefig(
            path_to_save_png + "_" + str(file_nb).rjust(2, '0') + "_" + data_type + "_x_" + str(x_value) + ".png",dpi=300)
        plt.close(fig)
        ax.clear()


        # Save CSV file
        # Find the max value of the array length
        data_size = []
        Breuer2009_data is not None and data_size.append(Breuer2009_data[0].size)
        Rapp2009_data is not None and data_size.append(Rapp2009_data[0].size)
        for i in range(0, len(file_names_lethe_data)):
            data_size.append(data_to_plot[i].size)

        index_max_size = np.max(np.array(data_size))
        arrays_to_dataframe = pd.DataFrame(index=range(1, index_max_size))

        for i, lethe_file in enumerate(file_names_lethe_data):
            arrays_to_dataframe.loc[:, data_type + "_" + lethe_file] = pd.Series(data_to_plot[i])
            arrays_to_dataframe.loc[:, "y_" + lethe_file] = pd.Series(y_to_plot[i])

        if Breuer2009_data is not None:
            arrays_to_dataframe.loc[:, data_type + "_Breuer2009"] = pd.Series(Breuer2009_data[0])
            arrays_to_dataframe.loc[:, "y_Breuer2009"] = pd.Series(Breuer2009_data[1])

        if Rapp2009_data is not None:
            arrays_to_dataframe.loc[:, data_type + "_Rapp2009"] = pd.Series(Rapp2009_data[0])
            arrays_to_dataframe.loc[:, "y_Rapp2009"] = pd.Series(Rapp2009_data[1])

        arrays_to_dataframe.to_csv(
            path_to_save_csv + "_" + str(file_nb).rjust(2, '0') + "_" + data_type + "_x_" + str(x_value) + ".csv",
            index=False, header=True)
