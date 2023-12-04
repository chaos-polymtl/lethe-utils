"""
LPBF case generation automation tool.

By: Olivier Gaboriault
Date: October 30th, 2023
"""
import numpy as np
import jinja2
from datetime import datetime
import os


# Simulation parameters
# ---------------------
# These parameters will be written at the start of the prm file for the post-processing python code
blade_speed = 0.100              # Speed of the blades
delta_starting_time = 0.7        # delta between two departure time of the blades in proportion of time_per_layer. Usually 0.7 to 0.8.
number_of_layers = 15            # Number of layer. We do +2 in the code for layer -1 and 0.
delta_b_p = 100E-6               # Distance between the tip of the blade and the transfert plate
delta_miss = 0.                  # Miss-match between the build-plate and the seperators
delta_o = 500E-6                 # Thickness of the first layer
delta_n = 300E-6                 # Thickness of the following layers
GAP = 500E-6                     # Void around the build plate
first_layer_extrusion = 2000E-6  # Extrusion of the first layer
other_layer_extrusion = 600E-6   # Extrusion of the following layers
alloy                 = "Y72e5"  # Powder type
first_starting_time = 0.3        # First departure time (Blade #-1)


# These parameters are not needed in the post_processing code but need to be defined
diameters_list = 100E-6          # List of all the diameters we want to use
domain_lenght = 0.03072          # Lenght of the domain. Is use to compute the time it takes the blades to move
plates_speed = 0.01              # Y reference speed of both plate
insertion_seed = 18

# Particles properties
young_particle = 72e5
poisson_ratio  = 0.3
density        = 2670
G              = young_particle / (2 * (1 + poisson_ratio))
dem_time_step  = 0.15 * ( 0.5 * np.pi * diameters_list * np.sqrt(density/G) * (1./(0.1631 * poisson_ratio + 0.8766)) )

# Wall propreties
young_wall = young_particle


# Frequencies
delta_insert_time        = 0.024
insert_frequency         = int(np.ceil(delta_insert_time / dem_time_step))
output_frequency         = int(insert_frequency/5.)
Restant_frequency        = insert_frequency * 2
load_balancing_frequency = insert_frequency + 1


### Case generator ###
# Time it takes for the plates to move for every new layers
plate_displacement_time = delta_n/plates_speed
### NUMBER OF CELL PER DIRECTION
#... stuff need to be made
#...
### Next step

# Starts at 4, takes into account the feeder, the build plate and the two seperators
solid_obj_id = 4
number_of_layers = number_of_layers + 2   # We add 2 for the layer #-1 and #0
total_solid_objects = 4 + number_of_layers

# Finding the departure time of all the blades
every_starting_time = np.empty(number_of_layers)
every_starting_time[0] = first_starting_time

# Times it takes for a blade to cross the domain in the X direction
time_per_layer = domain_lenght / blade_speed

# Find the departure time of every blade
for i in range(1,number_of_layers):
    every_starting_time[i] = every_starting_time[i-1] + time_per_layer * delta_starting_time


end_time = (every_starting_time[solid_obj_id - 4] + time_per_layer + 0.02)

# Initializing the string
# First coater is for the leveling of the reservoir. The 0.02 is to make sure thje blade exist the triangulation
coater_function = f"if(t>= {every_starting_time[solid_obj_id - 4]:.5}, if(t<= {(every_starting_time[solid_obj_id - 4] + time_per_layer + 0.02):.5}, {blade_speed:.5}, 0), 0)"
all_coater= (f"   subsection solid object {solid_obj_id} \n"
             f"      subsection mesh \n"
             f"         set type                = gmsh \n"
             f"         set file name           = ./gmsh/Blade.msh\n"
             f"         set simplex             = true\n"
             f"         set initial refinement  = 0\n"
             f"         set initial translation = -0.001, 0, 0\n"
             f"      end\n"
             f"      subsection translational velocity\n"
             f"         set Function expression = {coater_function}; 0; 0\n"
             f"      end\n"
             f"   end\n")
solid_obj_id += 1

# This while loop is use to generate the translational velocity functions and to create
# the string that is going to be replacing the "Blades" symbol in the parameter file.
while solid_obj_id - 4 < number_of_layers:
    end_time = (every_starting_time[solid_obj_id - 4] + time_per_layer + 0.02)
    coater_function = f"if(t>= {every_starting_time[solid_obj_id - 4]:.5}, if(t<= {(every_starting_time[solid_obj_id - 4] + time_per_layer + 0.02):.5}, {blade_speed:.5}, 0), 0)"

    coater_param = (f"   subsection solid object {str(solid_obj_id)} \n"
    f"subsection mesh \n"
    f"         set type                = gmsh \n"
    f"         set file name           = ./gmsh/Blade.msh\n"
    f"         set simplex             = true\n"
    f"         set initial refinement  = 0\n"
    f"         set initial translation = -0.0005, 0, 0\n"
    f"      end\n"
    f"      subsection translational velocity\n"
    f"         set Function expression = {coater_function}; 0; 0\n"
    f"      end\n"
    f"   end\n")

    solid_obj_id += 1
    all_coater = all_coater + coater_param

# Here, we create the displacement function for the reservoir plate and build plate.
reservoir_func   = str()
build_plate_func = str()

# The first one is special, since we want more powder on the first layer (usually 2.0 mm). --> Layer number = 0
# It's the same as what you can find in the while loop right after.

# We dont want big acceleration, thus de do the displacement over a longer period (3 times longer then a normal
# displacement). Also, 0.01 is the translation displacement of the first Seperator (HARD CODED)
t1 = every_starting_time[0] + 0.01 * 1.08 / blade_speed
t2 = t1 + plate_displacement_time * 3.

# 0.0241 is the initial translational displacement of the second separator.
t3 = every_starting_time[0] + 0.0241 * 1.05 / blade_speed
t4 = t3 + plate_displacement_time * 1.

const_first_layer_extrusion  = first_layer_extrusion / ( (1/3) * (t2**3 - t1**3) + 0.5 * (t1+t2) * (t1**2 - t2**2) + (t1*t2) * (t2 - t1) )
const_first_layer_build_plate = delta_o              / ( (1/3) * (t4**3 - t3**3) + 0.5 * (t3+t4) * (t3**2 - t4**2) + (t3*t4) * (t4 - t3) )

reservoir_func   = reservoir_func   + f"if(t>= {t1:.5}, if(t<= {t2:.5}, { const_first_layer_extrusion:.5} * (t - {t1:.5}) * (t - {t2:.5}), "
build_plate_func = build_plate_func + f"if(t>= {t3:.5}, if(t<= {t4:.5}, {-const_first_layer_build_plate:.5} * (t - {t3:.5}) * (t - {t4:.5}), "

for i in range(1,number_of_layers):
    # HARD CODED
    t1 = every_starting_time[i] + 0.01 * 1.08 / blade_speed
    t2 = t1 + plate_displacement_time * 1.                 # The reservoir moves...

    # HARD CODED
    t3 = every_starting_time[i] + 0.0241 * 1.05 / blade_speed
    t4 = t3 + plate_displacement_time * 1.

    # This constant can be find by integrating the speed function we define. This speed function is a second degree polynomial.
    # The integral must be equal to the layer height
    const = delta_n / ( (1/3) * (t2**3 - t1**3) + 0.5 * (t1+t2) * (t1**2 - t2**2) + (t1*t2) * (t2 - t1) )

    # Concatenate the displacement functions for all the layers.
    reservoir_func   = reservoir_func   + f"if(t>= {t1:.5}, if(t<= {t2:.5}, {(const * other_layer_extrusion/delta_n):.5} * (t - {t1:.5}) * (t - {t2:.5}), "
    build_plate_func = build_plate_func + f"if(t>= {t3:.5}, if(t<= {t4:.5}, {-const:.5} * (t - {t3:.5}) * (t - {t4:.5}), "

# Ending the functions
reservoir_func   = reservoir_func   + "0) "
build_plate_func = build_plate_func + "0) "
for i in range(1, number_of_layers):
    reservoir_func   = reservoir_func   + ", 0) )"
    build_plate_func = build_plate_func + ", 0) )"
reservoir_func   = reservoir_func   + ", 0)"
build_plate_func = build_plate_func + ", 0)"

# Initial translation for the powder reservor and domain
initial_trans = f"{-(number_of_layers)        * other_layer_extrusion - first_layer_extrusion :.5}"
y_min         = f"{-(number_of_layers + 0.05) * other_layer_extrusion - first_layer_extrusion :.5}"

# Post_processing string for the post-processing python code
post_processing = (f"# This file was created on :  {datetime.now()}\n"
f"# ----- Post processing parameters ----- #\n"
f"# Number of layers        = {number_of_layers - 2}\n"
f"# Blade speed             = {blade_speed:.5}\n"
f"# Delta_b_p               = {delta_b_p:.5}\n"
f"# Delta_0                 = {delta_o  :.5}\n"
f"# Delta_n                 = {delta_n  :.5}\n"
f"# Delta_miss_match        = {delta_miss:.5}\n"
f"# GAP                     = {GAP:.5}\n"
f"# First layer extrusion   = {first_layer_extrusion:.5}\n"
f"# N layer extrusion       = {other_layer_extrusion:.5}\n"
f"# Type of powder          = {alloy:.5}\n"
f"# First starting time     = {first_starting_time} \n"
f"# Diff. between two blade = {delta_starting_time} \n"
f"#"
                   )


## File names ##
# Name of the .prm file created
CASE_PREFIX = f"lpbf_{alloy}"

# Name of the output folder
output_folder = f"out_{alloy}_{datetime.now().date()}"

# Name of the restart files
restart_file = f"restart_{alloy}_{datetime.now().date()}"

# Name of the original .prm file being modified
PRM_FILE = 'lpbf_coating.prm'

# jinja2
PATH = os.getcwd()
templateLoader = jinja2.FileSystemLoader(searchpath=PATH)
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template(PRM_FILE)

# Replacing the symbols in the parameter file with the right expression
output_text = template.render(Post_processing = post_processing,
                              Delta_t = str(dem_time_step),
                              End_time = end_time,
                              Log_freq = str(insert_frequency-1),
                              Output_freq = str(output_frequency),
                              Out = output_folder,
                              Restant_freq = str(Restant_frequency),
                              Restart_name = restart_file,
                              Load_Bal_freq=str(load_balancing_frequency),
                              Young_particle=str(young_particle),
                              Young_wall=str(young_wall),
                              Insert_freq = str(insert_frequency),
                              Seed = insertion_seed,
                              Y_min = y_min,
                              X_max = domain_lenght,
                              Initial_translation = initial_trans,
                              Reservoir_function = reservoir_func,
                              Build_plate_function = build_plate_func,
                              Total_solid_objects = str(total_solid_objects),
                              Coaters = all_coater,
                              Diameters_List = diameters_list
                              )

prm_file_name = CASE_PREFIX + ".prm"
output_file_path = os.path.join("./", prm_file_name)
with open(output_file_path, 'w') as f:
    f.write(output_text)

print(f"{prm_file_name} has been written.")
