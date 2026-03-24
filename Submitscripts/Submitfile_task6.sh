#!/bin/bash

#BSUB -J Task6
#BSUB -q hpc
#BSUB -W 10
#BSUB -R "rusage[mem=1GB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -o outputfiles/Task6_%J.out
#BSUB -e outputfiles/Task6_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python src/parallelize.py 20
