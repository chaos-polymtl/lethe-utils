import numpy as np
import pyvista as vp
import time
import os


def translate_vtu_file(initial_filename, decimals, directory_vtu):
    """VTU file translation in an array ([x,y,z,r] for each particle)
    Inputs:
        - prm :
        - initial_filename : VTU file name that needs translation (name.vtu)
        - decimals : number of decimals in initial conditions equation
        - directory_vtu : VTU file directory
    Output :
        - Array with position and radius of each particle
            -data_table=[x,y,z,r]
    """
    # VTU file selection
    os.chdir(directory_vtu)

    if os.path.exists(initial_filename):
        # PYVISTA to translate VTU to array
        file = vp.read(initial_filename)
        particles_number = len(file.points)
        data_table = np.empty((particles_number, 4))
        data_table[:, 0:3] = file.points  # Position (x,y,z) for each particle
        data_table[:, 3] = file.point_data["Diameter"]
        data_table[:, 3] = data_table[:, 3] / 2  # Radius (r) for each particle

        # Decimal numbers for the initial conditions
        data_table = np.around(data_table, decimals=decimals)
    else:
        print(
            "Impossible to find the VTU file to determine the initial conditions equation"
        )
        exit()

    return data_table


def writing_initial_conditions(
    initial_filename,
    decimals=5,
    dimension="3D",
    directory_txt=os.path.abspath("."),
    directory_vtu=os.path.abspath("."),
):
    """Function to write initial conditions in a txt file (with indented if())
    Inputs:
            - prm :
            - initial_filename : VTU file name that needs translation (name.vtu)
            - decimals : Wished number of decimals in initial conditions equation
            - dimension : '3D' or '2D' (3D by default)
            - directory_txt : Wished txt file directory
            - directory_vtu : VTU file directory
    Output :
        - Initial conditions equation txt file
    """
    start_time = time.time()

    # VTU file traduction
    data_table = translate_vtu_file(initial_filename, decimals, directory_vtu)

    # Open/create file txt in the right directory (path_txt)

    os.chdir(directory_txt)
    txt_filename = initial_filename[:-4] + ".txt"  # replace .vtu extension to .txt
    file = open(txt_filename, "w", encoding="UTF-8")

    # Writing
    for i in range(len(data_table)):
        if dimension == "3D":
            file.write(
                "((x-%s)^2+(y-%s)^2+(z-%s)^2<(%s)^2?1:"
                % (
                    data_table[i, 0],
                    data_table[i, 1],
                    data_table[i, 2],
                    data_table[i, 3],
                )
            )
        if dimension == "2D":
            file.write(
                "((x-%s)^2+(y-%s)^2<(%s)^2?1:"
                % (data_table[i, 0], data_table[i, 1], data_table[i, 3])
            )
        i = i + 1

    file.write("0")

    for i in range(len(data_table)):
        file.write(")")

    file.close()

    # Writing time
    end_time = time.time()
    time_lapse = np.around(end_time - start_time, decimals=5)

    return print(
        "Initial conditions equation writing completed for %s in %s sec"
        % (txt_filename, time_lapse)
    )
