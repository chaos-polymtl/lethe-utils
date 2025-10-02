#!/bin/bash
#SBATCH --account=rrg-blaisbru 
#SBATCH --ntasks-per-node=192
#SBATCH --nodes={{N_NODES}}
#SBATCH --time=23:00:00        
#SBATCH --job-name=hopper_{{N_NODES}}
#SBATCH --output=hopper_{{N_NODES}}.out

source $HOME/.dealii
srun $HOME/lethe/inst/bin/lethe-particles hopper_{{N_NODES}}.prm
