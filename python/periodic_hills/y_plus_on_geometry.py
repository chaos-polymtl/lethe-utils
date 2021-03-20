# Name   : y_plus_on_geometry.py
# Author : Catherine Radburn
# Date   : 12-03-2021
# Desc   : This code evaluates and plots y+ across the length, and plots the values superimposed onto the geometry.
#           The near-wall region of data is extracted from Lethe. y+ is calculated from the gradient of the x velocity
#           in the y direction (the wall shear stress).
#           Note that this code only applies if alpha = 1 (i.e. no stretching of geometry)

import pandas
import numpy
from matplotlib import pyplot as plt
from pathlib import Path
import time
start_time = time.time()

########################################################################################################################
# SET VARIABLES

# Reynolds number and kinematic viscosity of the simulation (Currently available for Re = 5600 only)
Re = 5600
viscosity = 1.78571E-04

# Information about the Lethe data
path_to_lethe_data = "./lethe/"
# file_names_lethe_data = ["data_3","data_3_bdf2"]  # add all lethe files in this list
# file_names_lethe_data = ["time_0.025_600s", "time_0.025_700s", "time_0.025_800s","time_0.025_900s","time_0.025_1000s"]  # add all lethe files in this list
file_names_lethe_data = ["data_3"]
# file_names_lethe_data = ["data_3", "data_5_800s"]

# Label for Lethe data for the legend
# NOTE : make sure the number of labels are the same that the number of files names of lethe data
# labels = ["Lethe - 1M - 720s", "Lethe - 4M - 300s","Lethe - 4M - 500s"]
# labels = ["Lethe - 600s","Lethe - 700s","Lethe - 800s","Lethe - 900s","Lethe - 1000s"]
labels = ["Lethe - 1M - 720s"]
# labels = ["Lethe - 1M - 720s", "Lethe - 4M - 800s"]

# Information about the literature data
path_to_literature_data = "./lit/Re_5600/"

# Save graph.png and data.csv
folder_to_save_png = "./output_png/"
Path(folder_to_save_png).mkdir(parents=True, exist_ok=True)

folder_to_save_csv = "./output_csv/"
Path(folder_to_save_csv).mkdir(parents=True, exist_ok=True)

########################################################################################################################

# Lethe data extraction of files associated with x/h
def lethe_data_extraction(path_to_lethe_data, file_names_lethe_data, Re):
    assert Re == 5600, "Currently available for Re = 5600 only."

    # Set index
    index = 1
    extracted_lethe_data = []

    # For each Lethe file present
    for file_name in file_names_lethe_data:
        lethe_csv = path_to_lethe_data + file_name + ".csv"
        # Iterates through lethe_csv file
        iter_csv = pandas.read_csv(lethe_csv, usecols=["Points_0", "Points_1", "average_velocity_0",
                                                       "reynolds_shear_stress_uv"], sep=",", iterator=True,
                                                        chunksize=1000)
        # Saves required columns in range [0, 1.1] to Pandas dataframe lethe_data_range (up to y=1.2 for hills)
        lethe_lower_wall_data = pandas.concat(
            [chunk[(chunk["Points_1"] > 0) & (chunk["Points_1"] < 1.2)] for chunk in iter_csv])

        # Sort dataframe by x value
        lethe_lower_wall_data.sort_values(by=['Points_0'])

        # Convert Pandas dataframe into numpy array
        lethe_lower_wall_array = lethe_lower_wall_data.to_numpy()

        # Output
        print("Lethe data " + str(index) + " extracted")
        extracted_lethe_data.append(lethe_lower_wall_array)
        index += 1

    return extracted_lethe_data

# Function to find y_plus for each Lethe file
def y_plus(extracted_lethe_data, viscosity):
    fudge_factor = 8

    index = 1
    extracted_y_plus = []

    for i in range(len(extracted_lethe_data)):
        # Extract numpy array for each Lethe data file
        data_array = extracted_lethe_data[i]
        wall_array = data_array[data_array[:, 0].argsort()]

        # For each value of x, find the wall-nearest point
        # For each unique value of x "k"
        wall_nearest_points = []
        for k in numpy.unique(wall_array[:,0]):
            # initialise y_nearest variable
            y_nearest = numpy.array([[1000000, 1000000, 1000000, 1000000]])
            averaging_data = []

            # Each index "k" where the unique value of x appears
            for m in numpy.where(wall_array == k)[0]:
                # Find the minimum value of y at each value of x
                # if wall_array y value is smaller than y_nearest, replace
                if wall_array[m,1] < y_nearest[0,1] and wall_array[m, 2] != 0:
                    y_nearest = numpy.array([wall_array[m, :]])
                    averaging_data = [y_nearest]
                elif wall_array[m, 1] == y_nearest[0, 1] and wall_array[m, 2] != 0:
                    averaging_data.append(numpy.array([wall_array[m, :]]))

            # Average data
            averaging_data = numpy.asarray(averaging_data)
            averaging_data = numpy.squeeze(averaging_data)
            average_u = numpy.sum(averaging_data[:, 2]) / numpy.shape(averaging_data)[0]
            average_uv = numpy.sum(averaging_data[:, 3]) / numpy.shape(averaging_data)[0]
            wall_point = [averaging_data[0, 0], averaging_data[0, 1], average_u, average_uv]

            # Append y_nearest to wall_nearest_points
            wall_nearest_points.append(wall_point)

        # Convert to array
        wall_nearest_points = numpy.asarray(wall_nearest_points)
        wall_nearest_points = wall_nearest_points[wall_nearest_points[:, 0].argsort()]

        # Initialise output lists
        y_plus_data = []

        # Calculate y+ at each x value
        for m in range(numpy.shape(wall_nearest_points)[0]):
            x = wall_nearest_points[m,0]
            y1 = wall_nearest_points[m,1]

            # Scale to h=28
            x = 28*x

            # Determine y value of wall (y0) from geometry
            # First hill
            if x < 9:
                y0 = min(2.800000000000E+01, 2.800000000000E+01 + (0.000000000000E+00 * x) + (6.775070969851E-03 * (x ** 2)) - (2.124527775800E-03 * (x ** 3)))
            elif 9 <= x < 14:
                y0 = 2.507355893131E+01 + (9.754803562315E-01 * x) - (1.016116352781E-01 * (x ** 2)) + (1.889794677828E-03 * (x ** 3))
            elif 14 <= x < 20:
                y0 = 2.579601052357E+01 + (+8.206693007457E-01 * x) - (9.055370274339E-02 * (x ** 2)) + (1.626510569859E-03 * (x ** 3))
            elif 20 <= x < 30:
                y0 = 4.046435022819E+01 - (1.379581654948E+00 * x) + (1.945884504128E-02 * (x ** 2)) - (2.070318932190E-04 * (x ** 3))
            elif 30 <= x < 40:
                y0 = 1.792461334664E+01 + (8.743920332081E-01 * x) - (5.567361123058E-02 * (x ** 2)) + (6.277731764683E-04 * (x ** 3))
            elif 40 <= x < 54:
                y0 = max(0, (5.639011190988E+01 - (2.010520359035E+00 * x) + (1.644919857549E-02 * (x ** 2)) + (2.674976141766E-05 * (x ** 3))))

            # Second hill
            elif 198 <= x < 212:
                y0 = max(0, (5.639011190988E+01 - (2.010520359035E+00 * (252-x)) + (1.644919857549E-02 * ((252-x) ** 2)) + (2.674976141766E-05 * ((252-x) ** 3))))
            elif 212 <= x < 222:
                y0 = 1.792461334664E+01 + (8.743920332081E-01 * (252-x)) - (5.567361123058E-02 * ((252-x) ** 2)) + (6.277731764683E-04 * ((252-x) ** 3))
            elif 222 <= x < 232:
                y0 = 4.046435022819E+01 - (1.379581654948E+00 * (252-x)) + (1.945884504128E-02 * ((252-x) ** 2)) - (2.070318932190E-04 * ((252-x) ** 3))
            elif 232 <= x < 238:
                y0 = 2.579601052357E+01 + (+8.206693007457E-01 * (252-x)) - (9.055370274339E-02 * ((252-x) ** 2)) + (1.626510569859E-03 * ((252-x) ** 3))
            elif 238 <= x < 243:
                y0 = 2.507355893131E+01 + (9.754803562315E-01 * (252-x)) - (1.016116352781E-01 * ((252-x) ** 2)) + (1.889794677828E-03 * ((252-x) ** 3))
            elif x >= 243:
                y0 = min(2.800000000000E+01, 2.800000000000E+01 + (0.000000000000E+00 * (252-x)) + (6.775070969851E-03 * ((252-x) ** 2)) - (2.124527775800E-03 * ((252-x) ** 3)))

            else:
                y0 = 0

            # Rescale for h=1
            y0 = y0/28
            x = x/28

            assert y0 < y1, "The point on the wall y0 must have a lower y-value than the point immediately above the wall y1"

            # Calculate y+
            y_cc = (y1 - y0)/2
            viscous_stress = viscosity * ((wall_nearest_points[m, 2]) / (y1 - y0))
            re_stress = wall_nearest_points[m, 3]
            tau = viscous_stress - re_stress
            y_plus = (y_cc*numpy.sqrt(abs(tau)))/(viscosity)
            y_plus_geo = y0 + y_plus

            if y_plus_geo < fudge_factor:
                y_plus_data.append([x, y_plus_geo])

        y_plus_data = numpy.asarray(y_plus_data)

        # Output
        print("y+ values of Lethe data " + str(index) + " extracted")
        extracted_y_plus.append(y_plus_data)

        index += 1

    return extracted_y_plus

# Function to produce lower wall geometry
def wall_geometry():
    # Initialise list
    y_wall = []

    # Cycle over x in linspace over the x domain
    for x in numpy.linspace(0, 9, num=270, endpoint=True):
        # Scale to h=28
        x = 28 * x

        # Determine y value of wall (y0) from geometry
        # First hill
        if x < 9:
            y0 = min(2.800000000000E+01, 2.800000000000E+01 + (0.000000000000E+00 * x) + (6.775070969851E-03 * (x ** 2)) - (
                        2.124527775800E-03 * (x ** 3)))
        elif 9 <= x < 14:
            y0 = 2.507355893131E+01 + (9.754803562315E-01 * x) - (1.016116352781E-01 * (x ** 2)) + (
                        1.889794677828E-03 * (x ** 3))
        elif 14 <= x < 20:
            y0 = 2.579601052357E+01 + (+8.206693007457E-01 * x) - (9.055370274339E-02 * (x ** 2)) + (
                        1.626510569859E-03 * (x ** 3))
        elif 20 <= x < 30:
            y0 = 4.046435022819E+01 - (1.379581654948E+00 * x) + (1.945884504128E-02 * (x ** 2)) - (
                        2.070318932190E-04 * (x ** 3))
        elif 30 <= x < 40:
            y0 = 1.792461334664E+01 + (8.743920332081E-01 * x) - (5.567361123058E-02 * (x ** 2)) + (
                        6.277731764683E-04 * (x ** 3))
        elif 40 <= x < 54:
            y0 = max(0, (5.639011190988E+01 - (2.010520359035E+00 * x) + (1.644919857549E-02 * (x ** 2)) + (
                        2.674976141766E-05 * (x ** 3))))

        # Second hill
        elif 198 <= x < 212:
            y0 = max(0, (5.639011190988E+01 - (2.010520359035E+00 * (252 - x)) + (1.644919857549E-02 * ((252 - x) ** 2)) + (
                        2.674976141766E-05 * ((252 - x) ** 3))))
        elif 212 <= x < 222:
            y0 = 1.792461334664E+01 + (8.743920332081E-01 * (252 - x)) - (5.567361123058E-02 * ((252 - x) ** 2)) + (
                        6.277731764683E-04 * ((252 - x) ** 3))
        elif 222 <= x < 232:
            y0 = 4.046435022819E+01 - (1.379581654948E+00 * (252 - x)) + (1.945884504128E-02 * ((252 - x) ** 2)) - (
                        2.070318932190E-04 * ((252 - x) ** 3))
        elif 232 <= x < 238:
            y0 = 2.579601052357E+01 + (+8.206693007457E-01 * (252 - x)) - (9.055370274339E-02 * ((252 - x) ** 2)) + (
                        1.626510569859E-03 * ((252 - x) ** 3))
        elif 238 <= x < 243:
            y0 = 2.507355893131E+01 + (9.754803562315E-01 * (252 - x)) - (1.016116352781E-01 * ((252 - x) ** 2)) + (
                        1.889794677828E-03 * ((252 - x) ** 3))
        elif x >= 243:
            y0 = min(2.800000000000E+01,
                     2.800000000000E+01 + (0.000000000000E+00 * (252 - x)) + (6.775070969851E-03 * ((252 - x) ** 2)) - (
                                 2.124527775800E-03 * ((252 - x) ** 3)))
        else:
            y0 = 0

        # Rescale for h=1
        y0 = y0 / 28
        x = x / 28

        y_wall.append([x, y0])

    # Output
    y_wall = numpy.asarray(y_wall)

    return y_wall

# Plot of y+ values
def plot_y_plus(folder_to_save_png, extracted_y_plus, y_wall, labels, Re):
    # Plotting results
    fig, ax = plt.subplots()

    # Colours for graphs
    colors = ['#1b9e77', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#58aef5']
    index = 0

    # Plot y_plus_geo values
    for file_name in extracted_y_plus:
        if file_name is not None:
            ax.plot(file_name[:,0], file_name[:,1], '-', label=labels[index], color=colors[index])
            index += 1

    # Plot lower wall
    if y_wall is not None:
        ax.plot(y_wall[:, 0], y_wall[:, 1], '-', color='black')
        index += 1

    ax.set_title("y_plus along the lower wall at Re = " + str(Re))
    ax.set_xlabel("x/h")
    ax.set_ylabel("y/h")
    ax.legend()
    fig.savefig(
        folder_to_save_png + "graph_y_plus_geometry.png",
        dpi=300)
    plt.close(fig)
    ax.clear()

########################################################################################################################
# RUN FUNCTIONS

# Verify the number of labels is right
assert len(labels) == len(file_names_lethe_data), f"It seems to have {len(file_names_lethe_data)} Lethe data files and you gave " \
                            f"{len(labels)} labels, please verify your labels names."

# Collect required data types from near wall region
lethe_data = lethe_data_extraction(path_to_lethe_data, file_names_lethe_data, Re)
y_plus_data = y_plus(lethe_data, viscosity)
y_geometry = wall_geometry()
plot_y_plus(folder_to_save_png, y_plus_data, y_geometry, labels, Re)

print("--- %s seconds ---" % (time.time() - start_time))
