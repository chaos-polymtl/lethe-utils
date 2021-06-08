import numpy as np
import pandas as pd

# Paths and number of data files
path_to_python_data = "C:/Users/Acdai/OneDrive - polymtl.ca/Polytechnique/Session E2021/GCH8392 - Projet individuel de génie chimique/Data/python/"
path_to_cpp_data    = "C:/Users/Acdai/OneDrive - polymtl.ca/Polytechnique/Session E2021/GCH8392 - Projet individuel de génie chimique/Data/cpp/"
path_export_data    = "C:/Users/Acdai/OneDrive - polymtl.ca/Polytechnique/Session E2021/GCH8392 - Projet individuel de génie chimique/Data/C++_python_comparison/"


n_file = ["1", "2", "3", "4", "8", "9", "15", "16", "17"]
detector_face_position = [0.15, 0, 0.17]

# Initialize dataframes
dataframe = pd.DataFrame(columns=["files", "particle_positions_x", "particle_positions_y", "particle_positions_z", "detector_id", "distance_face_detector", "counts_cpp", "counts_python", "abs_error", "rel_error"])
dataframe_tmp = pd.DataFrame(columns=dataframe.columns)

# Read all .csv file
for n in n_file:
    data_cpp = pd.read_csv(path_to_cpp_data + "Test" + n + ".csv", sep=" ")
    data_python = pd.read_csv(path_to_python_data + "Test" + n + ".csv", sep=",")

    # Reset temporary dataframe
    dataframe_tmp = pd.DataFrame(columns=dataframe_tmp.columns)

    # Fill temporary dataframe
    dataframe_tmp["files"] = pd.Series(int(n) * np.ones(len(data_cpp), dtype=int))
    dataframe_tmp["particle_positions_x"] = data_cpp["particle_positions_x"]
    dataframe_tmp["particle_positions_y"] = data_cpp["particle_positions_y"]
    dataframe_tmp["particle_positions_z"] = data_cpp["particle_positions_z"]
    dataframe_tmp["detector_id"] = data_cpp["detector_id"]
    dataframe_tmp["counts_cpp"] = data_cpp["counts"]
    dataframe_tmp["counts_python"] = data_python["counts"]
    dataframe_tmp["distance_face_detector"] = np.sqrt((data_cpp["particle_positions_x"] - detector_face_position[0])**2
                                                          + (data_cpp["particle_positions_y"] - detector_face_position[1])**2 +
                                                          (data_cpp["particle_positions_z"] - detector_face_position[
                                                              2]) ** 2)
    dataframe_tmp["abs_error"] = np.abs(data_python["counts"] - data_cpp["counts"])
    dataframe_tmp["rel_error"] = dataframe_tmp["abs_error"]/data_cpp["counts"]*100

     # Copy or append main dataframe with temporary dataframe
    if int(n) == 1:
        dataframe = dataframe_tmp
    else:
        dataframe = dataframe.append(dataframe_tmp)

# Export one csv file with count data for every particle position
dataframe.to_csv(path_export_data + "pythoncpp.csv", index=False)

