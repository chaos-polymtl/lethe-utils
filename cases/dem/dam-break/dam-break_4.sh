#!/bin/bash
#SBATCH --account=rrg-blaisbru
#SBATCH --ntasks-per-node=40
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1 #number of whole nodes used (each with up to 40 tasks-per-node)
#SBATCH --time=5:59:00 #maximum time for the simulation (hh:mm:ss)
#SBATCH --mem=128G
#SBATCH --job-name=dam-break_4
#SBATCH --output=dam-break_4.out

export OMP_NUM_THREADS=1
source $HOME/.dealii
time mpirun -np 4 $HOME/lethe/inst/bin/dem_3d dam-break_4.prm