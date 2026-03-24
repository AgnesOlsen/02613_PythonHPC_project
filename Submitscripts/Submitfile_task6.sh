#!/bin/bash

#BSUB -J Task6
#BSUB -q hpc
#BSUB -W 60
#BSUB -R "rusage[mem=200MB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -n 16
#BSUB -R "span[hosts=1]"
#BSUB -o outputfiles/Task6_%J.out
#BSUB -e outputfiles/Task6_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python src/Task6.py 50
