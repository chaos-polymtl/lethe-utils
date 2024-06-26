#!/bin/bash
#SBATCH --account=def-blaisbru
#SBATCH --ntasks-per-node=40
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1 #number of whole nodes used (each with up to 40 tasks-per-node)
#SBATCH --time=23:59:00 #maximum time for the simulation (hh:mm:ss)
#SBATCH --mem=128G
#SBATCH --job-name=hopper_8
#SBATCH --output=hopper_8.out

export OMP_NUM_THREADS=1
source $HOME/.dealii
time mpirun -np 8 lethe-particles hopper_8.prm
