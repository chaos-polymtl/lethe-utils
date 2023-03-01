"""
Summary: Script to launch all the Lethe simulations, one at a time locally.
"""

import os

PATH = os.getcwd()

# User input
PRM_FILE = 'cylinder.prm'
LETHE_EXEC = '../gls_navier_stokes_2d'

for root, directories, files in os.walk(PATH):

    if PRM_FILE in files:

        os.chdir(root)

        os.system(f'{LETHE_EXEC} {PRM_FILE}')