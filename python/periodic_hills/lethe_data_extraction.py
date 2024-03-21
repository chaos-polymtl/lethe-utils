# Name   : lethe_data_extraction.py
# Author : Laura Prieto Saavedra (Adpated from Catherine Radburn and Audrey Collard-Daigneault)
# Date   : 22-06-2021
# Desc   : This code extracts the Lethe data for the periodic hills case for a specified x_value and data_type.
#          The data is saved as .csv files in the output_csv file. This only needs to be done once, as this data is 
#          not changing and it can be reused. 

#           If all x_value and data_type available are required, ignore x_value and data_type in lines 46 and 49, and
#           make all_data = True.
#           On line 350, a tolerance is specified. This may need to be varied if too little/too much data is plotted.

import pandas
import numpy
from matplotlib import pyplot as plt
from pathlib import Path
import time
start_time = time.time()

########################################################################################################################
# SET VARIABLES

# Reynolds number of the simulation (Currently available for Re = 5600, 10600, 37000 only)
Re = 5600

# Path to folder where Lethe simulation data is stored
path_to_lethe_data = "./lethe_data/"

#Filename
# example: file_names_lethe_data = ["0.0125_1M_1000s", "0.025_4M_800s"]
# file_names_lethe_data = ["0.1_4M_1000s_5600", "0.05_4M_1000s_5600", "0.025_4M_1000s_5600", "0.0125_4M_1000s_5600"]

# file_names_lethe_data = ["0.025_500K_500s_5600"] #, "0.025_4M_600s_5600", "0.025_4M_700s_5600", "0.025_4M_800s_5600", "0.025_4M_900s_5600"]

# file_names_lethe_data = ["0.1_120k_800s_10600" , "0.1_250k_800s_10600" , "0.1_500k_800s_10600"]
file_names_lethe_data = ["0.1_120k_800s_37000" , "0.1_250k_800s_37000" , "0.1_500k_800s_37000"]

#Create a solver according to case
folder_to_save_csv = "./output_csv/all_data/"
Path(folder_to_save_csv).mkdir(parents=True, exist_ok=True)

# x/h position: Set x_value to be equal to 0.05, 0.5, 1, 2, 3, 4, 5, 6, 7 or 8
x_value = 6

# data type options: Set data_type to be equal to "average_velocity_0", "average_velocity_1", "reynolds_normal_stress_0"
# "reynolds_normal_stress_1", "reynolds_shear_stress_uv", "reynolds_normal_stress_2" or "turbulent_kinetic_energy"
data_type = "reynolds_normal_stress_0"

# Extract and generate graphs for all x_values and data_types? (True or False)
all_data = True

########################################################################################################################

# Lethe data extraction of files associated with x/h
def lethe_data_extraction(x_value, data_type, path_to_lethe_data, file_names_lethe_data, Re):
    assert Re == 5600 or Re == 10600 or Re == 37000, "Currently available for Re = 5600, 10600, 37000 only."

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

            # If static mesh, upper and lower datasets will contain the same number of points. Adaptive meshes may not.
            if numpy.size(lethe_data_lower_y) == numpy.size(lethe_data_upper_y):
                lethe_data_data_type = ((upper_data_values - lower_data_values) * int_fraction) + lower_data_values
                lethe_data_y = ((lethe_data_upper_y - lethe_data_lower_y) * int_fraction) + lethe_data_lower_y
            else:
                # Ensure corresponding y values are used in interpolation
                tol = 0.01
                for upper_index, upper_y in numpy.ndenumerate(lethe_data_upper_y):
                    for lower_index, lower_y in numpy.ndenumerate(lethe_data_lower_y):
                        if upper_y >= lower_y and upper_y <= lower_y+tol:
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
        pandas.DataFrame(file).to_csv(folder_to_save_csv + '_Lethe_data_' + str(file_names_lethe_data[index-1]) + '_' + str(data_type) + '_x_' + str(x_value) + '.csv')
        index += 1

    return extracted_lethe_data

########################################################################################################################
# RUN FUNCTIONS

# Collect all data types at each x_value
if all_data is True:
    # data_type_available = ["average_velocity_0", "average_velocity_1", "reynolds_normal_stress_0",
                        #    "reynolds_normal_stress_1", "reynolds_shear_stress_uv", "reynolds_normal_stress_2"]   # turbulent_kinetic_energy
    data_type_available = ["average_velocity_0","reynolds_normal_stress_0", "reynolds_shear_stress_uv"] 
    x_available = [0.05, 0.5, 1, 2, 3, 4, 5, 6, 7, 8]
    # x_available = [0.5, 2, 4, 6]

    for x in x_available:
        for flow_property in data_type_available:
            lethe_data = lethe_data_extraction(x, flow_property, path_to_lethe_data, file_names_lethe_data, Re)

# Collect a specified x_value and data_type
else:
    # EXTRACT DATA FROM LETHE FUNCTION (loop through all x, data type)
    lethe_data = lethe_data_extraction(x_value, data_type, path_to_lethe_data, file_names_lethe_data, Re)

print("--- %s seconds ---" % (time.time() - start_time))
