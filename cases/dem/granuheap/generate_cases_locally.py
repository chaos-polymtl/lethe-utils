"""
Summary: Script to generate different cases (as folders) of the same problem 
with one parameters being changed.

This script generates multiples folders of the example of the flow around a cylinder.
In each folder, we change the input velocity (u) in the parameter file in order to 
have a different case of the same problem.
"""

import jinja2
import os
import numpy as np
import itertools
import shutil
import os
import csv
from pyDOE import *
import matplotlib.pyplot as plt

points = lhs(2, samples=10, criterion='center')


# Define the target interval [m, n]
x_min = 0.0002
x_max = 0.0004
y_min = 0.2
y_max = 0.4

# Calculate the scale factor
x_scale = x_min - x_max
y_scale = y_min - y_max

# Transform each point to the [m, n] interval
x = x_max + points[:, 0] * x_scale
y = y_max + points[:, 1] * y_scale

np.append(x,x_min)
np.append(y,y_min)

np.append(x,x_min)
np.append(y,y_max)


np.append(x,x_max)
np.append(y,y_min)


np.append(x,x_max)
np.append(y,y_max)

x = [round(val, 7) for val in x]
y = [round(val, 3) for val in y]


rows = zip(x, y)

with open('points.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['parameter1', 'parameter2'])
    writer.writerows(rows)
        
# Plot the points
plt.figure(figsize=(6, 6))  # Optional: adjust figure size
plt.scatter(x, y, color='b', marker='o')
plt.title('Distribution de points LSH')
plt.xlabel('X')
plt.ylabel('Y')
plt.xlim(x_min, x_max)  # Optional: adjust limits if necessary
plt.ylim(y_min, y_max)  # Optional: adjust limits if necessary
plt.grid(True)
plt.savefig('parameter_lsh_distribution.png')



PATH = os.getcwd()

# User input
CASE_PREFIX = 'ti64_'
PRM_FILE = 'granuheap_ti64.prm'
MESH_FILE_1 = 'support.msh'
MESH_FILE_2 = 'cylinder.msh'
number_of_cases = 4

# Generation of data points
energy = x

rolling_friction = y

# Create Jinja template
templateLoader = jinja2.FileSystemLoader(searchpath=PATH)
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template(PRM_FILE)

# Generation of different cases
for v, u in zip(rolling_friction, energy):

        case_folder_name = f'{CASE_PREFIX}{u:.7f}_{v:.3f}'

        if os.path.exists(case_folder_name) and os.path.isdir(case_folder_name):
            shutil.rmtree(case_folder_name)
        
        # Insert the velocity in the prm template with Jinja2 and render it
        parameters = template.render(energy = u, rolling_friction = v)

        # Create the folder of the case and put the prm template in it
        case_path = f'{PATH}/{case_folder_name}'
        os.mkdir(case_path)
        shutil.copy(f'{PATH}/{PRM_FILE}', f'{case_path}/{PRM_FILE}')
        
        # Copy the mesh file (in order to launch Lethe in seperate folders)
        shutil.copy(f'{PATH}/{MESH_FILE_1}', f'{case_path}/{MESH_FILE_1}')
        shutil.copy(f'{PATH}/{MESH_FILE_2}', f'{case_path}/{MESH_FILE_2}')
        shutil.copy(f'{PATH}/ti64.sh', f'{case_path}/ti64.sh')
        shutil.copy(f'{PATH}/particles.input', f'{case_path}/particles.input')

        # Write a unique prm file with the prm template being updated
        with open(f'{case_path}/{PRM_FILE}', 'w') as f:
            f.write(parameters)

        print(f'{case_folder_name} generated successfully!')
