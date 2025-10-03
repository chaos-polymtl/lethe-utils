# SPDX-FileCopyrightText: Copyright (c) 2025 The Lethe Authors
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception OR LGPL-2.1-or-later

import numpy as np
import gmsh
import jinja2
import os

## This code generates the parameter files and the solid surfaces meshes required 
# for the DEM weak scaling test cases.

# Number of nodes used for each run
n_proc = [1,2,3,4,5,10,15,20, 25, 30, 35, 40, 45, 50]

# Number of particles per nodes
n_part = 1_920_000

# Domain dept in z per nodes
z_dept =  1.583505

def solid_surface(z_max, output_mesh_file):
    gmsh.initialize()
    x_min_0 = -0.06272
    x_max_0 = -0.012544
    
    x_min_1 = 0.012544
    x_max_1 = 0.06272
    
    z_min = 0
    
    points_0 = []
    points_1 = []
    
    lines_0 = []
    lines_1 = []
    
    line_loops_0 = []
    line_loops_1 = []
    
    # Left
    points_0.append(gmsh.model.geo.addPoint(x_min_0, 0.0, z_min, meshSize=1.))
    points_0.append(gmsh.model.geo.addPoint(x_max_0, 0.0, z_min, meshSize=1.))
    points_0.append(gmsh.model.geo.addPoint(x_min_0, 0.0, z_max, meshSize=1.))
    points_0.append(gmsh.model.geo.addPoint(x_max_0, 0.0, z_max, meshSize=1.))
    
    points_1.append(gmsh.model.geo.addPoint(x_min_1, 0.0, z_min, meshSize=1.))
    points_1.append(gmsh.model.geo.addPoint(x_max_1, 0.0, z_min, meshSize=1.))
    points_1.append(gmsh.model.geo.addPoint(x_min_1, 0.0, z_max, meshSize=1.))
    points_1.append(gmsh.model.geo.addPoint(x_max_1, 0.0, z_max, meshSize=1.))
    
    # Left 
    lines_0.append(gmsh.model.geo.add_line(points_0[0],points_0[1]))
    lines_0.append(gmsh.model.geo.add_line(points_0[1],points_0[2]))
    lines_0.append(gmsh.model.geo.add_line(points_0[2],points_0[0]))
    lines_0.append(gmsh.model.geo.add_line(points_0[2],points_0[3]))
    lines_0.append(gmsh.model.geo.add_line(points_0[3],points_0[1]))
    
    # Right
    lines_1.append(gmsh.model.geo.add_line(points_1[0],points_1[1]))
    lines_1.append(gmsh.model.geo.add_line(points_1[1],points_1[2]))
    lines_1.append(gmsh.model.geo.add_line(points_1[2],points_1[0]))
    lines_1.append(gmsh.model.geo.add_line(points_1[2],points_1[3]))
    lines_1.append(gmsh.model.geo.add_line(points_1[3],points_1[1]))
    
    # Left 
    line_loops_0.append(gmsh.model.geo.addCurveLoop([lines_0[0],lines_0[1], lines_0[2]]))
    line_loops_0.append(gmsh.model.geo.addCurveLoop([lines_0[1],lines_0[3], lines_0[4]]))
    
    # Right
    line_loops_1.append(gmsh.model.geo.addCurveLoop([lines_1[0],lines_1[1], lines_1[2]]))
    line_loops_1.append(gmsh.model.geo.addCurveLoop([lines_1[1],lines_1[3], lines_1[4]]))
    
    plane_surfaces = [gmsh.model.geo.addPlaneSurface([line_loops_0[0]]),
                     gmsh.model.geo.addPlaneSurface([line_loops_0[1]]),
                     gmsh.model.geo.addPlaneSurface([line_loops_1[0]]),
                     gmsh.model.geo.addPlaneSurface([line_loops_1[1]])]
    
    gmsh.model.geo.synchronize()
    gmsh.model.addPhysicalGroup(2, plane_surfaces)
    gmsh.model.geo.synchronize()

    # Generate mesh:
    gmsh.model.mesh.generate(2)
    # Write mesh data:
    gmsh.write(output_mesh_file)
    
# Case generator
PATH = os.getcwd()
PRM_FILE_HOPPER = 'hopper.tpl'
PRM_FILE_SBATCH = 'sbatch.tpl'

templateLoader = jinja2.FileSystemLoader(searchpath=PATH)
templateEnv = jinja2.Environment(loader=templateLoader)
template_hopper = templateEnv.get_template(PRM_FILE_HOPPER)
template_sbatch = templateEnv.get_template(PRM_FILE_SBATCH)

for val in n_proc:
    gmsh_string = f"gmsh/mesh_{val}.msh"
    
    this_z_dept = val * z_dept
    
    solid_surface(this_z_dept, gmsh_string)
    
    output_text_hopper = template_hopper.render(N_NODES=f"{val}",
                                                N_REFINEMENT_Z=f"{val* 15}",
                                                N_PARTICLES=f"{val * n_part }", 
                                                INSERT_Z=f"{val * z_dept - 0.0004}", 
                                                Z_DEPT=f"{this_z_dept}",
                                                GMSH = gmsh_string )
    
    output_text_sbatch = template_sbatch .render(N_NODES=f"{val}")
    
    
    prm_file_name = f"hopper_{val}.prm"
    sbatch_file_name = f"hopper_{val}.sh"

    # Write the output text to the prm file
    output_file_path = os.path.join("./", prm_file_name)
    with open(output_file_path, 'w') as f:
        f.write(output_text_hopper)
        
    with open(sbatch_file_name, 'w') as f:
        f.write(output_text_sbatch)
        
