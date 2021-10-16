# -*- coding: utf-8 -*-
"""
Script used to prepare multiple simulations subdirectories and modify .prm according to a varying parameter.
Python version: 3.5 and above.
First version: 15/10/2021 by Jeanne Joachim
Last modification: 15/10/2021 by Jeanne Joachim
-------------------
Preparation: put an initial .prm file along with needed .msh and .sh in a directory.
Note: You can run this python code from anywhere.
-------------------
Input (under "# User INPUT") :
 * dir_ini: string giving the path of the directory containing the initial .prm, .sh and .msh (if needed).
 * prm_old_line: string giving the COMPLETE (with left spaces) parameter line, to be modified in the .prm.
 * prm_name: string giving the parameter name used in sub-directory.
    NB: if this string contains spaces, they will be changed with "-".
 * prm_val: list or range of values taken by the .prm. Elements of the list can be numbers of string.
   NB: used in the sub-directory name.
 * prm_pre: string prefix for parameter in .prm, put before prm_val values. Useful if varied parameter is a mesh name.
 * prm_suf: string suffix for parameter in .prm, put after prm_val values. Useful if varied parameter is a mesh name.
    ex/ multiple mesh to test : "mesh_1.msh", "mesh_2.msh". prm_val = [1,2] ; prm_pre = "mesh_" and prm_suf = ".msh"
    NB: for now, all mesh files tested will be copied in sub-directories.

Output :
 * subdirectories with simulation files needed and modified .prm
 * printed changed lines in .prm for verification purposes
 * cluster's command to be copied/pasted in the terminal
"""

import os
from tempfile import mkstemp
from shutil import move, copymode, copyfile

# User INPUT
dir_ini = "/home/jeannej/Softwares/lethe/post-traitements/test_auto"
prm_old_line = "		set file name	= PBT_N05_3D.msh"
prm_name = "N"
prm_val = ["1", "2"]
prm_pre = "PBT_N"
prm_suf = ".msh"

# Preparation
dir_prm = "-".join(prm_name.split(" "))  # we do not want spaces in directory name
prm_old_line += "\n"
cluster_cmd = []
modif_prm = []

# Loop over the parameter's list
for v in list(prm_val):
    subdir = "_".join([dir_prm, str(v)])
    dir_v = os.path.join(dir_ini, subdir)

    # create directories
    os.mkdir(dir_v)
    # copy all simulation files
    os.system("cp " + dir_ini + "/*.prm " + dir_ini + "/*.sh " + dir_ini + "/*.msh " + dir_v)

    # modify .prm
    file_prm = [f for f in os.listdir(dir_v) if f.endswith(".prm")][0]
    prm_new_line = prm_old_line.split("=")[0]+" = " + prm_pre + str(v) + prm_suf + " \n"
    # create temporary file
    fh, abs_path = mkstemp()
    path_prm = os.path.join(dir_v, file_prm)
    with os.fdopen(fh, 'w') as new_file:
        with open(path_prm) as old_file:
            nbl = 0
            for line in old_file:
                if prm_old_line in line:
                    nbl += 1
                    filesample = file_prm
                new_file.write(line.replace(prm_old_line, prm_new_line))
        # check if file has been modified at least once
        if nbl != 0:
            modif_prm += ["PRM modified with: " + prm_new_line]
            file_sh = [f for f in os.listdir(dir_v) if f.endswith(".sh")][0]
            cluster_cmd += ["sbatch "+os.path.join(dir_v, file_sh)]
    # copy the file permissions from the old file to the new file
    copymode(path_prm, abs_path)
    # remove original file
    os.remove(path_prm)
    # move new file
    move(abs_path, path_prm)

# Commands to print
print("".join(modif_prm))
print("Cluster commands to copy/paste on terminal:")
print(" & ".join(cluster_cmd))
