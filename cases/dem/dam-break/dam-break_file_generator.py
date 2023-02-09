# Name of the case (for filenames)
case_name = "dam-break"

# Path to the .prm & .sh template files
prm_template = f"{case_name}_template.prm"
sh_template = f"{case_name}_template.sh"
tab = "  "

# Path to save generated files
path_save = f"./"

# Relevant parameters for the case for modifications
n_particle = 15000
n_particle_per_step = 15000
width = 0.05
d = 0.01
n_cores = [1, 2, 4, 8, 16, 32, 40]
solmsh_name = "square"


# Create a new file with the new parameters
# Read prm file
with open(prm_template, 'r') as f:
    lines = f.readlines()

copy_lines = lines.copy()

for core in n_cores:
    for line in copy_lines:
        # Replace the mesh (mesh > grid arguments)
        param_msh = f"{tab}set grid arguments"
        if line.startswith(param_msh):
            n_space = line[len(param_msh):].count(' ') - 1
            line_replacement = line.replace(line, f"{param_msh}{n_space*' '}= 40,16,{core} : 0,0,0 : 2.0,0.8,{core*width} : true\n")
            copy_lines[copy_lines.index(line)] = line_replacement

        # Replace the solid mesh file (solid objects > solid object 0 > mesh > file name)
        param_solmsh = f"{3*tab}set file name"
        if line.startswith(param_solmsh):
            n_space = line[len(param_solmsh):].count(' ') - 1
            line_replacement = line.replace(line, f"{param_solmsh}{n_space*' '}= meshes/{solmsh_name}_{core}.msh\n")
            copy_lines[copy_lines.index(line)] = line_replacement

        # Replace the number of particles (lagrangian physical properties > particle type 0 > number)
        param_n_particle = f"{2*tab}set number"
        if line.startswith(param_n_particle):
            n_space = line[len(param_n_particle):].count(' ') - 1
            line_replacement = line.replace(line, f"{param_n_particle}{n_space*' '}= {core*n_particle}\n")
            copy_lines[copy_lines.index(line)] = line_replacement

        # Replace the number of particles inserted (insertion info > inserted number of particles at each time step)
        param_part_step = f"{tab}set inserted number of particles at each time step"
        if line.startswith(param_part_step):
            n_space = line[len(param_part_step):].count(' ') - 1
            line_replacement = line.replace(line, f"{param_part_step}{n_space*' '}= {core*n_particle_per_step}\n")
            copy_lines[copy_lines.index(line)] = line_replacement

        # Replace the z axis insertion box value (insertion info > insertion box maximum z)
        param_z_max_box = f"{tab}set insertion box maximum z"
        if line.startswith(param_z_max_box):
            n_space = line[len(param_z_max_box):].count(' ') - 1
            line_replacement = line.replace(line, f"{param_z_max_box}{n_space*' '}= {core*width-d/4.}\n")
            copy_lines[copy_lines.index(line)] = line_replacement

        # Replace the output path
        param_output = f"{tab}set output path"
        if line.startswith(param_output):
            n_space = line[len(param_output):].count(' ') - 1
            line_replacement = line.replace(line, f"{param_output}{n_space*' '}= ./output_{core}/\n")
            copy_lines[copy_lines.index(line)] = line_replacement

    with open(f"{path_save}/{case_name}_{str(core)}.prm", 'w') as f:
        f.writelines(copy_lines)


# Create a new file with the new parameters
# Read prm file
with open(sh_template, 'r') as f:
    lines = f.readlines()

copy_lines = lines.copy()

for i, core in enumerate(n_cores):
    if i == 0:
        prev_core = 1
    else:
        prev_core = n_cores[i-1]

    for line in copy_lines:
        # Replace the number of cores
        param_mpi = f"time mpirun -np"
        if line.startswith(param_mpi):
            line_replacement = line.replace(f"-np {prev_core}", f"-np {str(core)}")
            line_replacement = line_replacement.replace(f"{case_name}_{prev_core}", f"{case_name}_{str(core)}")
            copy_lines[copy_lines.index(line)] = line_replacement

        # Replace the number of particles
        param_name = f"#SBATCH --job-name="
        param_log = f"#SBATCH --output="
        if line.startswith(param_name) or line.startswith(param_log):
            line_replacement = line.replace(f"{case_name}_{prev_core}", f"{case_name}_{str(core)}")
            copy_lines[copy_lines.index(line)] = line_replacement


    with open(f"{path_save}/{case_name}_{str(core)}.sh", 'w', newline='\n') as f:
        f.writelines(copy_lines)



