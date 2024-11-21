"""
Summary: Script to launch all the Lethe simulations, one at a time locally.
"""

import os

PATH = os.getcwd()

# User input
CASE_PREFIX = 'wetsand_'
PRM_FILE = 'granuheap_wetsand.prm'
LETHE_EXEC = 'lethe-particles'

for root, directories, files in os.walk(PATH):

    if CASE_PREFIX in root:

        os.chdir(root)

        os.system(f'srun $HOME/lethe/inst/bin/{LETHE_EXEC} {PRM_FILE}')
        
