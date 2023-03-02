"""
Summary: Script to generate different cases (as folders) of the same problem 
with one parameters being changed.

This script generates multiples folders of the example of the flow around a sphere.
In each folder, we change the input velocity (u) in the parameter file in order to 
have a different case of the same problem.
Because this script is made to generate the folders on a cluster, we add a shell script (.sh) 
to each folder, in order to launch a job according to the specified case.
"""

from jinja2 import Template
import os
import numpy as np
import shutil

PATH = os.getcwd()

# User input
CASE_PREFIX = 'cylinder_u_'
PRM_FILE = 'cylinder.prm'
MESH_FILE = 'cylinder-structured.msh'
SHELL_FILE = 'launch_lethe.sh'
number_of_cases = 20

# Generation of data points
first_velocity = 1
last_velocity = 10
velocity = np.linspace(1, 10, number_of_cases)

# Generation of different cases
for u in velocity:

    case_folder_name = f'{CASE_PREFIX}{u:.2f}'

    if os.path.exists(case_folder_name):
        shutil.rmtree(case_folder_name)

    # Open the parameter (prm) template file
    fic_prm = open(PRM_FILE, 'r')
    content_prm = fic_prm.read()
    # Insert the velocity in the prm template with Jinja2 and render it
    template = Template(content_prm)
    parameters = template.render(velocity_x = u)
    # Close the prm file
    fic_prm.close()

    # Create the folder of the case and put the prm template in it
    case_path = f'{PATH}/{case_folder_name}'
    os.mkdir(case_path)
    shutil.copy(f'{PATH}/{PRM_FILE}', f'{case_path}/{PRM_FILE}')
    
    # Copy the mesh file (in order to launch Lethe in seperate folders)
    shutil.copy(f'{PATH}/{MESH_FILE}', f'{case_path}/{MESH_FILE}')
    
    # Copy the shell script for the 
    shutil.copy(f'{PATH}/{SHELL_FILE}', f'{case_path}/{SHELL_FILE}')

    # Enter the case folder
    os.chdir(case_path)

    # Write a unique prm file with the prm template being updated
    write_prm = open(PRM_FILE, 'w')
    write_prm.write(parameters)
    write_prm.close()

    # Get out of the case path (in order to create another template for another case)
    os.chdir('../')