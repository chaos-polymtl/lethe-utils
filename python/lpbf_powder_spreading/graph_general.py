#############################################################################
"""
Postprocessing automation tool.

By: Olivier Gaboriault
Date: January 13th, 2024
"""
#############################################################################
'''Importing Libraries'''
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from lethe_pyvista_tools import *

#############################################################################

# Take case path as argument
prm_file_names = np.array(
    [
     "75_01_05/75_01_05.prm",
     "75_01_10/75_01_10.prm",
     "75_01_20/75_01_20.prm",
     "75_03_05/75_03_05.prm",
     "75_03_10/75_03_10.prm",
     "75_03_20/75_03_20.prm"
     ])   # ./parameter.prm -->peut-[etre
plt.figure(figsize=(10, 6))

color_palette = ['blue', 'red', 'green', 'black', 'orange', 'purple',"cyan", "magenta", "yellow"]
# Loop over a
j = 0
for i in prm_file_names:

    prefix = i.split('/')[-1].split('.')[0]

    CRD = np.load('./00_binary/' + prefix + '_CRD.npy')
    LRD = np.load('./00_binary/' + prefix + '_LRD.npy')
    NLayer = np.load('./00_binary/' + prefix + '_number_of_layers.npy')

    print(CRD)
    plt.plot(np.arange(len(CRD))+1, CRD[0:],"--." ,label=f"Cumulative relative density - Geometry {j+1}", color=color_palette[j])
    plt.plot(np.arange(len(CRD))+1, LRD[0:],"-x"  ,label=f"Layer relative density - Geometry {j+1}", color=color_palette[j])
    j += 1

plt.grid()
#plt.title("Powder layer relative density (LRD) evolution compare to\n " + r"the cumulative relative density (CRD) for different blade geometry")
plt.xlabel("Layer number", fontsize=14)
plt.ylabel("Relative density (%)",fontsize=14)
plt.locator_params(axis='x', integer=True)
plt.xticks(np.arange(0, 15))
#plt.legend(loc='best',fontsize=14)
plt.show()
print("Job is done")
