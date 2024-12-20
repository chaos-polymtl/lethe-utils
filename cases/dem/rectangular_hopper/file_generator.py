case_name = "hopper"
prm_template = f"{case_name}_template.prm"
sh_template = f"{case_name}_template.sh"
tab = "  "
width = 0.0056
d = 0.00112

n_cores = [1, 2, 4,8,16,32,40,80,120,160,200]
n_particle = 6790
n_particle_per_step = 485


# Create a new file .prm with the new parameters
# Read prm file
with open(prm_template, 'r') as f:
    lines = f.readlines()

copy_lines = lines.copy()

for core in n_cores:
    for line in copy_lines:
        # Replace the mesh file
        param_msh = f"{tab}set file name"
        if line.startswith(param_msh):
            n_space = line[len(param_msh):].count(' ') - 1
            line_replacement = line.replace(line, f"{param_msh}{n_space*' '}= meshes/hopper_structured_{str(core*2)}.msh\n")
            copy_lines[copy_lines.index(line)] = line_replacement

        # Replace the number of particles
        param_n_particle = f"{tab}{tab}set number of particles"
        if line.startswith(param_n_particle):
            n_space = line[len(param_n_particle):].count(' ') - 1
            line_replacement = line.replace(line, f"{param_n_particle}{n_space*' '}= {2*core*n_particle}\n")
            copy_lines[copy_lines.index(line)] = line_replacement

        # Replace the number of particles inserted
        param_part_step = f"{tab}set inserted number of particles at each time step"
        if line.startswith(param_part_step):
            n_space = line[len(param_part_step):].count(' ') - 1
            line_replacement = line.replace(line, f"{param_part_step}{n_space*' '}= {str(2*core*n_particle_per_step)}\n")
            copy_lines[copy_lines.index(line)] = line_replacement

        # Replace the z axis insertion box value
        param_insert_box = f"{tab}set insertion box points coordinates"
        if line.startswith(param_insert_box):
            n_space = line[len(param_insert_box):].count(' ') - 1
            string_to_insert = ("-0.06, 0.10644, .00112 : 0.06,  0.16020, "+str(2*core*width-d))
            line_replacement = line.replace(line, f"{param_insert_box}{n_space*' '}= {string_to_insert}\n")
            copy_lines[copy_lines.index(line)] = line_replacement

        # Replace the output path
        param_output = f"{tab}set output path"
        if line.startswith(param_output):
            n_space = line[len(param_output):].count(' ') - 1
            line_replacement = line.replace(line, f"{param_output}{n_space*' '}= ./output_{str(core)}/\n")
            copy_lines[copy_lines.index(line)] = line_replacement

    with open(f"{case_name}_{str(core)}.prm", 'w') as f:
        f.writelines(copy_lines)


# Create the script .sh
with open(sh_template, 'r') as f:
    lines = f.readlines()

copy_lines = lines.copy()

for i, core in enumerate(n_cores):
    if i == 0:
        prev_core = 1
    else:
        prev_core = n_cores[i-1]

    for line in copy_lines:
        param_mpi = f"time mpirun -np"

        if line.startswith(param_mpi):
            line_replacement = line.replace(f"-np {prev_core}", f"-np {str(core)}")
            line_replacement = line_replacement.replace(f"{case_name}_{prev_core}", f"{case_name}_{str(core)}")
            copy_lines[copy_lines.index(line)] = line_replacement

        # Replace the output and job name
        param_name = f"#SBATCH --job-name="
        param_log = f"#SBATCH --output="
        if line.startswith(param_name) or line.startswith(param_log):
            line_replacement = line.replace(f"{case_name}_{prev_core}", f"{case_name}_{str(core)}")
            copy_lines[copy_lines.index(line)] = line_replacement


    with open(f"{case_name}_{str(core)}.sh", 'w', newline='\n') as f:
        f.writelines(copy_lines)



