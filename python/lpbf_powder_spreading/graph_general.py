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
        # "25_01_05/25_01_05.prm",
        # "25_01_10/25_01_10.prm",
        # "25_01_20/25_01_20.prm",
        # "25_03_05/25_03_05.prm",
        # "25_03_10/25_03_10.prm",
        # "25_03_20/25_03_20.prm",
        # "25_03_100/25_03_100.prm",
        # "25_03_200/25_03_200.prm",
        # "50_01_05/50_01_05.prm",
        # "50_01_10/50_01_10.prm",
        # "50_01_20/50_01_20.prm",
        # "50_03_05/50_03_05.prm",
        # "50_03_10/50_03_10.prm",
        # "50_03_20/50_03_20.prm",
         "50_03_100/50_03_100.prm",
         "50_03_200/50_03_200.prm",
        # "75_01_10/75_01_05.prm",
        # "75_01_10/75_01_10.prm",
        # "75_01_20/75_01_20.prm",
        # "75_03_05/75_03_05.prm",
        # "75_03_10/75_03_10.prm",
        # "75_03_20/75_03_20.prm",
        # "75_03_100/75_03_100.prm",
        # "75_03_200/75_03_200.prm"
    ])     # ./parameter.prm
plt.figure(figsize=(10, 6))


# Experimental data
# M100_V100
M100_V100_R1 = np.array(
    [55.4264, 60.6019, 59.5303, 59.9635, 59.5759, 59.0971, 59.5759, 59.3251, 60.1003, 60.2599, 60.7843, 61.3315,
     62.4031, 63.4747, 65.0023, 66.8947, 67.0771, 68.6959, 67.9207, 65.1847])/100.
M100_V100_R2 = np.array(
    [56.2927, 59.8267, 59.4163, 59.7127, 59.2339, 59.3707, 59.3707, 59.8267, 59.9179, 59.8267, 60.8527, 61.7191,
     62.7451, 64.8427, 67.0999, 68.1715, 68.5135, 68.0119, 65.8687, 64.0219])/100.

M100_V100_R3 = np.array(
    [53.8076, 59.7583, 59.2795, 59.7127, 58.8919, 59.4847, 59.7583, 59.6215, 60.1687, 60.3055, 60.8983, 61.9243,
     63.0415, 64.4551, 66.5983, 68.4907, 68.6503, 68.5135, 66.6439, 64.7515])/100.
M100_V100_AVG = (M100_V100_R1 + M100_V100_R2 + M100_V100_R3) / 3
M100_V100_MIN = np.min([M100_V100_R1, M100_V100_R2, M100_V100_R3], axis=0)
M100_V100_MAX = np.max([M100_V100_R1, M100_V100_R2, M100_V100_R3], axis=0)
M100_V100_ERR = [M100_V100_AVG - M100_V100_MIN, M100_V100_MAX - M100_V100_AVG]
plt.errorbar(np.arange(1, len(M100_V100_AVG)+1), M100_V100_AVG, yerr=M100_V100_ERR, fmt="-s", label=r"Experimental, V=100 $\frac{mm}{s}$, L=100 $\mu m$", markersize=5, capsize=5)


color_palette = ['blue', 'red',  'black', 'orange', 'purple',"cyan", "magenta", "yellow",'green']
# Loop over a
j = 0
for i in prm_file_names:

    prefix = i.split('/')[-1].split('.')[0]

    CRD = np.load('./00_binary/' + prefix + '_CRD.npy')
    LRD = np.load('./00_binary/' + prefix + '_LRD.npy')
    NLayer = np.load('./00_binary/' + prefix + '_number_of_layers.npy')

    #plt.plot(np.arange(len(CRD))+1, CRD[0:],"--." ,label=f"Cumulative relative density - Geometry {j+1}", color=color_palette[j])
    label_input = prefix.split('_')

    plt.plot(np.arange(len(CRD))+1, LRD[0:],"-x", label=rf"$\mu_T$=0.{label_input[0]}, $\mu_R$={float(label_input[1])/10}, $\gamma$={label_input[2]}e-6 , layer", color=color_palette[j])
    #plt.plot(np.arange(len(CRD))+1, CRD[0:],"--", label=rf"$\mu_T$=0.{label_input[0]}, $\mu_R$={float(label_input[1])/10}, $\gamma$={label_input[2]}e-6 , cumulative", color=color_palette[j])
    j += 1

plt.grid()
#plt.title("Powder layer relative density (LRD) evolution compare to\n " + r"the cumulative relative density (CRD) for different blade geometry")
plt.xlabel("Layer number", fontsize=14)
plt.ylabel("Relative density (%)",fontsize=14)
plt.locator_params(axis='x', integer=True)
plt.xticks(np.arange(0, 21))
plt.legend(loc='best',fontsize=12)
plt.savefig('./00_figures/'+"50_03_200"+'.svg')
plt.show()

print("Job is done")
