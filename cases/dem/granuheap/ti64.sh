#!/bin/bash
#SBATCH --account=def-blaisbru #def-blaisbru
#SBATCH --ntasks-per-node=32
#SBATCH --nodes=1
#SBATCH --time=96:00:00
#SBATCH --mem=248G         
#SBATCH --job-name=granuheap
#SBATCH --output=granuheap.out
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=cleo.deletre@gmail.com

module load StdEnv/2020
module load gcc/9.3.0
module load openmpi/4.0.3
module load trilinos/13.4.1
module load parmetis/4.0.3
module load p4est/2.2
module load opencascade/7.5.2

source $HOME/.dealii
srun $HOME/lethe/inst/bin/lethe-particles granuheap_ti64.prm
