#!/bin/bash

#BSUB -J Task8
#BSUB -q c02613
#BSUB -W 1
#BSUB -R "rusage[mem=100MB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -o outputfiles/Task8_%J.out
#BSUB -e outputfiles/Task8_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

time python src/Task8.py 2
