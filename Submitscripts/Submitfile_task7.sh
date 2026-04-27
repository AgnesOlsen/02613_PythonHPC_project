#!/bin/bash

#BSUB -J Task7
#BSUB -q hpc
#BSUB -W 5
#BSUB -R "rusage[mem=10GB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -o outputfiles/Task7_%J.out
#BSUB -e outputfiles/Task7_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

time python src/Task7.py 5
time python src/Task7.py 5
