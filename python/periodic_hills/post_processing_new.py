# Name   : postprocess_data_new.py
# Author : Catherine Radburn (adapted from Audrey Collard-Daigneault)
# Date   : 27-04-2021
# Desc   : This code plots simulation data from Lethe and other data from literature.
#           Each run will extract the literature and Lethe data for a specified x_value and data_type, save extracted
#           data as .csv files, and plot extracted data into a .png file.
#           If all x_value and data_type available are required, ignore x_value and data_type in lines 46 and 49, and
#           make all_data = True

import pandas
import numpy
from matplotlib import pyplot as plt
from pathlib import Path
import time
start_time = time.time()

########################################################################################################################
# SET VARIABLES

# Reynolds number of the simulation (Currently available for Re = 5600 only)
Re = 5600

# Information about the Lethe data
path_to_lethe_data = "./lethe/"
# file_names_lethe_data = ["data_3","data_3_bdf2"]  # add all lethe files in this list
# file_names_lethe_data = ["data_3"],"data_6_500s"]  # add all lethe files in this list
# file_names_lethe_data = ["data_3"]
file_names_lethe_data = ["4M_600", "1M_800"]

# Label for Lethe data for the legend
# NOTE : make sure the number of labels are the same that the number of files names of lethe data
# labels = ["Lethe - 1M - 720s", "Lethe - 4M - 300s","Lethe - 4M - 500s"]
# labels = ["Lethe - 1M - bdf1","Lethe - 1M - bdf2"]
# labels = ["Lethe - 1M - 720s"]
labels = ["Lethe - 4M - 600s", "Lethe - 1M - 800s"]

# Information about the literature data
path_to_literature_data = "./lit/Re_5600/"

# Save graph.png and data.csv
folder_to_save_png = "./output_png/"
Path(folder_to_save_png).mkdir(parents=True, exist_ok=True)

folder_to_save_csv = "./output_csv/"
Path(folder_to_save_csv).mkdir(parents=True, exist_ok=True)

# x/h position: Set x_value to be equal to 0.05, 0.5, 1, 2, 3, 4, 5, 6, 7 or 8
x_value = 0.5

# data type options: Set data_type to be equal to "average_velocity_0", "average_velocity_1", "reynolds_normal_stress_0"
# "reynolds_normal_stress_1", "reynolds_shear_stress_uv", "reynolds_normal_stress_2" or "turbulent_kinetic_energy"
data_type = "average_velocity_1"

# Extract and generate graphs for all x_values and data_types? (True or False)
all_data = False

# Display the title on the output graphs? (True or False)
display_title = True

########################################################################################################################

# Literature data extraction of files associated with x/h
def literature_data_extraction(x_value, data_type, path_to_literature_data, folder_to_save_csv, Re):
    assert Re == 5600, "Currently available for Re = 5600 only."

    # Using x value to determine which file number is required
    if x_value == 0.05:
        literature_data_nb = "01"
        ww_lit_data_nb = "05"
    elif x_value == 0.5:
        literature_data_nb = "02"
        ww_lit_data_nb = None
    elif x_value == 1:
        literature_data_nb = "03"
        ww_lit_data_nb = None
    elif x_value == 2:
        literature_data_nb = "04"
        ww_lit_data_nb = "11"
    elif x_value == 3:
        literature_data_nb = "05"
        ww_lit_data_nb = None
    elif x_value == 4:
        literature_data_nb = "06"
        ww_lit_data_nb = "17"
    elif x_value == 5:
        literature_data_nb = "07"
        ww_lit_data_nb = None
    elif x_value == 6:
        literature_data_nb = "08"
        ww_lit_data_nb = None
    elif x_value == 7:
        literature_data_nb = "09"
        ww_lit_data_nb = None
    elif x_value == 8:
        literature_data_nb = "10"
        ww_lit_data_nb = "23"
    else:
        literature_data_nb = None
        ww_lit_data_nb = None

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
    elif data_type == "reynolds_normal_stress_2":
        literature_data_type = "w'w'/u_b^2"
    elif data_type == "turbulent_kinetic_energy":
        literature_data_type = "k/u_b^2"
    else:
        literature_data_type = None

    # Getting literature data
    # To obtain reynolds_normal_stress_2
    if ww_lit_data_nb is not None and literature_data_type == "w'w'/u_b^2":
        Rapp2009_data = None
        Breuer2009_csv = path_to_literature_data + "Breuer2009/Breuer2009_" + str(ww_lit_data_nb) + ".csv"
        Breuer2009_data = pandas.read_csv(Breuer2009_csv, usecols=["x", "Curve" + str(ww_lit_data_nb)], sep=",")
        Breuer2009_data = [numpy.array(Breuer2009_data["Curve" + str(ww_lit_data_nb)]),numpy.array(Breuer2009_data["x"])]

    elif ww_lit_data_nb is None and literature_data_type == "w'w'/u_b^2":
        Rapp2009_data = Breuer2009_data = None

    # To obtain turbulent_kinetic_energy
    elif literature_data_nb is not None and literature_data_type == "k/u_b^2":
        Rapp2009_data = None
        Breuer2009_csv = path_to_literature_data + "Breuer2009_UFR3-30/Breuer2009_3-30_" + str(literature_data_nb) + ".csv"
        Breuer2009_data = pandas.read_csv(Breuer2009_csv, usecols=["y/h", literature_data_type], sep=";")
        Breuer2009_data = [numpy.array(Breuer2009_data[literature_data_type]), numpy.array(Breuer2009_data["y/h"])]

    # To obtain all other data_type
    elif literature_data_nb is not None and literature_data_type is not None:
        Rapp2009_csv = path_to_literature_data + "Rapp2009_UFR3-30/Rapp2009_" + str(literature_data_nb) + ".csv"
        Rapp2009_data = pandas.read_csv(Rapp2009_csv, usecols=["y/h", literature_data_type], sep=",")
        Rapp2009_data = [numpy.array(Rapp2009_data[literature_data_type]), numpy.array(Rapp2009_data["y/h"])]

        Breuer2009_csv = path_to_literature_data + "Breuer2009_UFR3-30/Breuer2009_3-30_" + str(
            literature_data_nb) + ".csv"
        Breuer2009_data = pandas.read_csv(Breuer2009_csv, usecols=["y/h", literature_data_type], sep=";")
        Breuer2009_data = [numpy.array(Breuer2009_data[literature_data_type]), numpy.array(Breuer2009_data["y/h"])]
    else:
        Rapp2009_data = Breuer2009_data = None

    # Write output arrays to .csv files
    pandas.DataFrame(Rapp2009_data).to_csv(
        folder_to_save_csv + '_Rapp2009' + str(data_type) + '_x_' + str(x_value) + '.csv')
    pandas.DataFrame(Breuer2009_data).to_csv(
        folder_to_save_csv + '_Breuer2009' + str(data_type) + '_x_' + str(x_value) + '.csv')

    print("Literature data extracted for x = ", x_value, " and for data type = " + data_type)
    return Breuer2009_data, Rapp2009_data, literature_data_type


# Lethe data extraction of files associated with x/h
def lethe_data_extraction(x_value, data_type, path_to_lethe_data, file_names_lethe_data, Re):
    assert Re == 5600, "Currently available for Re = 5600 only."

    # Set bounds for x-values to be stored in iteration
    lower_bound = x_value - 0.1  # Tolerance set at 0.1 based on spacing in x-values at coarse mesh in initial case
    upper_bound = x_value + 0.1

    # Set index
    index = 1
    extracted_lethe_data = []

    # For each Lethe file present
    for file_name in file_names_lethe_data:
        lethe_csv = path_to_lethe_data + file_name + ".csv"

        # Iterates through lethe_csv file
        iter_csv = pandas.read_csv(lethe_csv, usecols=["Points_0", "Points_1", data_type], sep=",", iterator=True,
                                   chunksize=10000)
        # Saves required columns in range [lower_bound, upper_bound] to Pandas dataframe lethe_data_range
        lethe_data_range = pandas.concat(
            [chunk[(chunk["Points_0"] > lower_bound) & (chunk["Points_0"] < upper_bound)] for chunk in iter_csv])

        # Sort dataframe by x value
        lethe_data_range.sort_values(by=['Points_0'])

        # Convert Pandas dataframe into numpy array
        lethe_data_range_array = lethe_data_range.to_numpy()

        # If the x_value is exact
        if x_value in lethe_data_range_array[:, 0]:
            print("Unique data found for x/h = ", x_value)

            # Initialise extracted data lists
            y_data = []
            data_type_data = []

            # Find rows which contain x_value
            for i in range(numpy.shape(lethe_data_range_array)[0]):
                if lethe_data_range_array[i, 0] == x_value:
                    # Add y and data_type values to list
                    y_data.append([lethe_data_range_array[i, 1]])
                    data_type_data.append([lethe_data_range_array[i, 2]])

            # Convert to numpy arrays
            y_data = numpy.asarray(y_data)
            data_type_data = numpy.asarray(data_type_data)
            
            # Average across z values
            # Initialise lists
            lethe_data_y = []
            lethe_data_data_type = []

            # For each unique value of y "i"
            for i in numpy.unique(y_data):
                averaging_data = []

                # Each index "j" where the unique value of y appears
                for j in numpy.where(y_data == i)[0]:
                    # Find values in d at each index j and add to averaging_data array
                    averaging_data.append([data_type_data[j, 0]])

                # Remove initial row and average data
                averaging_data = numpy.asarray(averaging_data)
                average = numpy.sum(averaging_data) / (numpy.shape(averaging_data)[0])

                # Add values for interpolation
                lethe_data_y.append([i])
                lethe_data_data_type.append([average])

            # Convert to numpy arrays
            lethe_data_y = numpy.asarray(lethe_data_y)
            lethe_data_data_type = numpy.asarray(lethe_data_data_type)

            # Output array
            file_name = [lethe_data_data_type, lethe_data_y]

        # If the x_value is not exact, interpolate between values
        else:
            print("No unique data found for x/h = ", x_value, " Interpolating")
            # Find rows which contain x_values nearest to x_value

            # Initialise blank error array of same length as lethe_data_range_array
            abs_error = numpy.zeros((numpy.shape(lethe_data_range_array)[0], 1))

            for i in range(numpy.shape(lethe_data_range_array)[0]):
                # Calculate absolute error between exact x_value and data x_values
                abs_error[i, 0] = lethe_data_range_array[i, 0] - x_value

            # Sort absolute error array
            abs_error = numpy.sort(abs_error, axis=0)

            # Find value immediately greater and smaller than x_value
            just_above_x_value = (abs_error[abs_error > 0][0]) + x_value
            just_below_x_value = (abs_error[abs_error < 0][-1]) + x_value
            print("Interpolation values identified : ", just_below_x_value, "and", just_above_x_value)

            # Initialise interpolation matrices
            upper_interpolation_matrix = []
            lower_interpolation_matrix = []

            # Consider each row of the matrix and create new matrices
            for i in range(numpy.shape(lethe_data_range_array)[0]):
                if lethe_data_range_array[i, 0] == just_above_x_value:
                    # Create matrix of y and data_type values just above x_value
                    upper_interpolation_matrix.append([lethe_data_range_array[i, 1], lethe_data_range_array[i, 2]])
                elif lethe_data_range_array[i, 0] == just_below_x_value:
                    # Create matrix of y and data_type values just below x_value
                    lower_interpolation_matrix.append([lethe_data_range_array[i, 1], lethe_data_range_array[i, 2]])

            for i in numpy.unique(upper_interpolation_matrix):
                print(i)
            
            
            # Upper interpolation values

            # Convert interpolation matrices to numpy arrays
            upper_interpolation_matrix = numpy.asarray(upper_interpolation_matrix)

            # Sort columns by y value
            upper_interpolation_matrix.argsort(axis=0)

            # Average data across z values
            # Create array of y values
            y_data_upper = numpy.delete(upper_interpolation_matrix, 1, 1)

            # Set up arrays to calculate interpolation
            upper_d = numpy.delete(upper_interpolation_matrix, 0, 1)

            # Initialise interpolation arrays
            lethe_data_upper_y = []
            upper_data_values = []

            # For each unique value of y "i"
            for i in numpy.unique(y_data_upper):
                upper_averaging_data = []

                # Each index "j" where the unique value of y appears
                for j in numpy.where(y_data_upper == i)[0]:
                    # Find values in d at each index j and add to averaging_data array
                    upper_averaging_data.append([upper_d[j, 0]])

                # Convert to array and average data
                upper_averaging_data = numpy.asarray(upper_averaging_data)
                u_average = numpy.sum(upper_averaging_data) / (numpy.shape(upper_averaging_data)[0])

                # Add values to arrays for interpolation
                lethe_data_upper_y.append([i])
                upper_data_values.append([u_average])

            # Convert to array
            lethe_data_upper_y = numpy.asarray(lethe_data_upper_y)
            upper_data_values = numpy.asarray(upper_data_values)

            # Lower interpolation values (as above)
            lower_interpolation_matrix = numpy.asarray(lower_interpolation_matrix)
            lower_interpolation_matrix.argsort(axis=0)
            y_data_lower = numpy.delete(lower_interpolation_matrix, 1, 1)
            lower_d = numpy.delete(lower_interpolation_matrix, 0, 1)

            # Initialise interpolation arrays
            lethe_data_lower_y = []
            lower_data_values = []

            for i in numpy.unique(y_data_lower):
                lower_averaging_data = []

                # Each index "j" where the unique value of y appears
                for j in numpy.where(y_data_lower == i)[0]:
                    # Find values in d at each index j and add to averaging_data array
                    lower_averaging_data.append([lower_d[j, 0]])

                # Convert to array and average data
                lower_averaging_data = numpy.asarray(lower_averaging_data)
                l_average = numpy.sum(lower_averaging_data) / (numpy.shape(lower_averaging_data)[0])
                lethe_data_lower_y.append([i])
                lower_data_values.append([l_average])

            # Convert to array
            lethe_data_lower_y = numpy.asarray(lethe_data_lower_y)
            lower_data_values = numpy.asarray(lower_data_values)

            # Prepare for linear interpolation
            int_fraction = (x_value - just_below_x_value) / (just_above_x_value - just_below_x_value)
            lethe_data_data_type = []
            lethe_data_y = []

            # Ensure corresponding y values are used in interpolation
            for upper_index, upper_y in numpy.ndenumerate(lethe_data_upper_y):
                for lower_index, lower_y in numpy.ndenumerate(lethe_data_lower_y):
                    if upper_y >= lower_y and upper_y <= lower_y+0.001:
                        # Linear interpolation : u = (u_2 - u_1) * (x - x_1) / (x2 - x1) + u_1
                        lethe_data = ((upper_data_values[upper_index] - lower_data_values[lower_index]) * int_fraction) + lower_data_values[lower_index]
                        lethe_y = ((upper_y - lower_y) * int_fraction) + lower_y

                        lethe_data_data_type.append([lethe_data])
                        lethe_data_y.append([lethe_y])

            lethe_data_data_type = numpy.asarray(lethe_data_data_type)
            lethe_data_y = numpy.asarray(lethe_data_y)

            # Create matrix of interpolated data points and y/h
            file_name = [lethe_data_data_type, lethe_data_y]

        # Output
        print("Lethe data " + str(index) + " extracted for x = ", x_value, " and for data type = " + data_type)
        extracted_lethe_data.append(file_name)

        # Reshape numpy arrays to write to .csv
        file = [numpy.concatenate(lethe_data_data_type), numpy.concatenate(lethe_data_y)]
        # Write output arrays to .csv files
        pandas.DataFrame(file).to_csv(folder_to_save_csv + '_Lethe_data_' + str(file_names_lethe_data[index-1]) + str(data_type) + '_x_' + str(x_value) + '.csv')
        index += 1

    return extracted_lethe_data


# Plot literature values against Lethe values
def plot_to_png(Breuer2009_data, Rapp2009_data, lethe_data, data_type, x_value, labels,
                folder_to_save_png, show_title):
    # Plotting results
    fig, ax = plt.subplots()

    # Colours for graphs
    colors = ['#1b9e77', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#58aef5']
    index = 0

    # Set display axis titles
    if data_type == "average_velocity_0":
        x_axis_label = "$v/u_b$"
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

    # Plot Lethe data
    for file_name in lethe_data:
        if file_name is not None:
            ax.plot(file_name[0], file_name[1], '--', label=labels[index], color=colors[index])
            index += 1

    # Plot Breuer data
    if Breuer2009_data is not None:
        ax.plot(Breuer2009_data[0], Breuer2009_data[1], '-', alpha=0.7, color='orange',
                label='LESOCC - Breuer 2009')

    # Plot Rapp data
    if Rapp2009_data is not None:
        ax.plot(Rapp2009_data[0], Rapp2009_data[1], '--', color='black',
                label='Experimental - Rapp 2009')

    # Only display title if specified
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

        ax.set_title(title + " at Re = " + str(Re) + " at x = " + str(x_value))

    ax.set_xlabel(x_axis_label)
    ax.set_ylabel("$y/h$")
    ax.legend()
    fig.savefig(
        folder_to_save_png + "graph_" + data_type + "_x_" + str(x_value) + ".png",
        dpi=300)
    plt.close(fig)
    ax.clear()

########################################################################################################################
# RUN FUNCTIONS

# Verify the number of labels is right
assert len(labels) == len(file_names_lethe_data), f"It seems to have {len(file_names_lethe_data)} Lethe data files and you gave " \
                            f"{len(labels)} labels, please verify your labels names."

# Collect all data types at each x_value
if all_data is True:
    data_type_available = ["average_velocity_0", "average_velocity_1", "reynolds_normal_stress_0",
                           "reynolds_normal_stress_1", "reynolds_shear_stress_uv", "reynolds_normal_stress_2"]   # turbulent_kinetic_energy
    x_available = [0.05, 0.5, 1, 2, 3, 4, 5, 6, 7, 8]

    for x in x_available:
        for flow_property in data_type_available:
            [Breuer2009_data, Rapp2009_data, literature_data_type] = literature_data_extraction(x, flow_property, path_to_literature_data,
                                                                      folder_to_save_csv, Re)
            lethe_data = lethe_data_extraction(x, flow_property, path_to_lethe_data, file_names_lethe_data, Re)
            plot_to_png(Breuer2009_data, Rapp2009_data, lethe_data, flow_property, x, labels, folder_to_save_png, display_title)

# Collect a specified x_value and data_type
else:
    # EXTRACT DATA FROM LITERATURE FUNCTION (loop through all x, data type)
    [Breuer2009_data, Rapp2009_data, literature_data_type] = literature_data_extraction(x_value, data_type, path_to_literature_data, folder_to_save_csv, Re)

    # EXTRACT DATA FROM LETHE FUNCTION (loop through all x, data type)
    lethe_data = lethe_data_extraction(x_value, data_type, path_to_lethe_data, file_names_lethe_data, Re)

    # PLOT RESULTS
    plot_to_png(Breuer2009_data, Rapp2009_data, lethe_data, data_type, x_value, labels, folder_to_save_png, display_title)

print("--- %s seconds ---" % (time.time() - start_time))
