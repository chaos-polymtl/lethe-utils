# Name   : literature_data_extraction.py
# Author : Laura Prieto Saavedra (Adpated from Catherine Radburn and Audrey Collard-Daigneault)
# Date   : 22-06-2021
# Desc   : This code extracts the literature data for the periodic hills case for a specified x_value and data_type.
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

# Reynolds number of the simulation (Currently available for Re = 5600, 10600, 37000 (experimental) only)
Re = 5600

# Information about the literature data
path_to_literature_data = "./lit/Re_5600/"

# Save data in csv files
folder_to_save_csv = "./output_csv/literature/5600/"
Path(folder_to_save_csv).mkdir(parents=True, exist_ok=True)

# If an specific x/h position is needed: Set x_value to be equal to 0.05, 0.5, 1, 2, 3, 4, 5, 6, 7 or 8
x_value = 0.5

# data type options: Set data_type to be equal to "average_velocity_0", "average_velocity_1", "reynolds_normal_stress_0"
# "reynolds_normal_stress_1", "reynolds_shear_stress_uv", "reynolds_normal_stress_2" or "turbulent_kinetic_energy"
data_type = "average_velocity_1"

# Extract and generate graphs for all x_values and data_types? (True or False)
all_data = True


########################################################################################################################

# Literature data extraction of files associated with x/h
def literature_data_extraction(x_value, data_type, path_to_literature_data, folder_to_save_csv, Re):
    assert Re == 5600 or Re == 10600 or Re == 37000, "Currently available for Re = 5600, 10600 and 37000 (exp) only."

    # Using x value to determine which file number is required
    if x_value == 0.05:
        literature_data_nb = "01"
        if Re == 10600 or Re == 37000:
            ww_lit_data_nb = None
        else:
            ww_lit_data_nb = "05"
    elif x_value == 0.5:
        literature_data_nb = "02"
        ww_lit_data_nb = None
    elif x_value == 1:
        literature_data_nb = "03"
        ww_lit_data_nb = None
    elif x_value == 2:
        literature_data_nb = "04"
        if Re == 10600 or Re == 37000:
            ww_lit_data_nb = None
        else:
            ww_lit_data_nb = "11"        
    elif x_value == 3:
        literature_data_nb = "05"
        ww_lit_data_nb = None
    elif x_value == 4:
        literature_data_nb = "06"
        if Re == 10600 or Re == 37000:
            ww_lit_data_nb = None
        else:
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
        if Re == 10600 or Re == 37000:
            ww_lit_data_nb = None
        else: 
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
        if Re == 37000:
            Breuer2009_data = None
        else:
            Breuer2009_csv = path_to_literature_data + "Breuer2009/Breuer2009_" + str(ww_lit_data_nb) + ".csv"
            Breuer2009_data = pandas.read_csv(Breuer2009_csv, usecols=["x", "Curve" + str(ww_lit_data_nb)], sep=",")
            Breuer2009_data = [numpy.array(Breuer2009_data["Curve" + str(ww_lit_data_nb)]),numpy.array(Breuer2009_data["x"])]

    elif ww_lit_data_nb is None and literature_data_type == "w'w'/u_b^2":
        Rapp2009_data = Breuer2009_data = None

    # To obtain turbulent_kinetic_energy
    elif literature_data_nb is not None and literature_data_type == "k/u_b^2":
        Rapp2009_data = None
        if Re == 37000:
            Breuer2009_data = None
        else:
            Breuer2009_csv = path_to_literature_data + "Breuer2009_UFR3-30/Breuer2009_3-30_" + str(literature_data_nb) + ".csv"
            Breuer2009_data = pandas.read_csv(Breuer2009_csv, usecols=["y/h", literature_data_type], sep=";")
            Breuer2009_data = [numpy.array(Breuer2009_data[literature_data_type]), numpy.array(Breuer2009_data["y/h"])]

    # To obtain all other data_type
    elif literature_data_nb is not None and literature_data_type is not None:
        Rapp2009_csv = path_to_literature_data + "Rapp2009_UFR3-30/Rapp2009_" + str(literature_data_nb) + ".csv"
        Rapp2009_data = pandas.read_csv(Rapp2009_csv, usecols=["y/h", literature_data_type], sep=",")
        Rapp2009_data = [numpy.array(Rapp2009_data[literature_data_type]), numpy.array(Rapp2009_data["y/h"])]

        if Re == 37000:
            Breuer2009_data = None
        else:
            Breuer2009_csv = path_to_literature_data + "Breuer2009_UFR3-30/Breuer2009_3-30_" + str(
                literature_data_nb) + ".csv"
            Breuer2009_data = pandas.read_csv(Breuer2009_csv, usecols=["y/h", literature_data_type], sep=";")
            Breuer2009_data = [numpy.array(Breuer2009_data[literature_data_type]), numpy.array(Breuer2009_data["y/h"])]
    else:
        Rapp2009_data = Breuer2009_data = None

    # Write output arrays to .csv files
    pandas.DataFrame(Rapp2009_data).to_csv(
        folder_to_save_csv + '_Rapp2009' + str(data_type) + '_x_' + str(x_value) + '.csv')
    if Re == 5600 or Re == 10600:
        pandas.DataFrame(Breuer2009_data).to_csv(
        folder_to_save_csv + '_Breuer2009' + str(data_type) + '_x_' + str(x_value) + '.csv')

    print("Literature data extracted for x = ", x_value, " and for data type = " + data_type)
    return Breuer2009_data, Rapp2009_data, literature_data_type


########################################################################################################################
# RUN FUNCTIONS
# Collect all data types at each x_value
if all_data is True:
    data_type_available = ["average_velocity_0", "average_velocity_1", "reynolds_normal_stress_0",
                           "reynolds_normal_stress_1", "reynolds_shear_stress_uv", "reynolds_normal_stress_2"]   # turbulent_kinetic_energy
    x_available = [0.05, 0.5, 1, 2, 3, 4, 5, 6, 7, 8]

    for x in x_available:
        for flow_property in data_type_available:
            [Breuer2009_data, Rapp2009_data, literature_data_type] = literature_data_extraction(x, flow_property, path_to_literature_data,
                                                                      folder_to_save_csv, Re)
# Collect a specified x_value and data_type
else:
    # EXTRACT DATA FROM LITERATURE FUNCTION (loop through all x, data type)
    [Breuer2009_data, Rapp2009_data, literature_data_type] = literature_data_extraction(x_value, data_type, path_to_literature_data, folder_to_save_csv, Re)

print("--- %s seconds ---" % (time.time() - start_time))
