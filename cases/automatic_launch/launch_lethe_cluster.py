"""
Summary: Script to launch all the Lethe simulations on a cluster, one job for every cases.
"""

import os

PATH = os.getcwd()

# User input
PRM_FILE = 'cylinder.prm'
SHELL_FILE = 'launch_lethe.sh'

for root, directories, files in os.walk(PATH):

    if PRM_FILE in files and root != PATH:

        os.chdir(root)

        path_name = root.split('/')[-1]
        os.system(f'sbatch -J {path_name} {SHELL_FILE}')