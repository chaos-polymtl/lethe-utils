#!/bin/bash
#SBATCH --account=def-bertrand
#SBATCH --ntasks-per-node=40
#SBATCH --cpus-per-task=1
#SBATCH --mem=80G
#SBATCH --nodes=1 #number of whole nodes used (each with up to 40 tasks-per-node)
#SBATCH --time=10:59:00 #maximum time for the simulation (hh:mm:ss)
#SBATCH --job-name=hopper_32
#SBATCH --output=hopper_32.out

export OMP_NUM_THREADS=1
source $HOME/.dealii
time mpirun -np 32 lethe-particles hopper_32.prm