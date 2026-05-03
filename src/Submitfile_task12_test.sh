#!/bin/bash

#BSUB -J Task12_test
#BSUB -q gpua100
#BSUB -W 2
#BSUB -R "rusage[mem=100MB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -o outputfiles/Task12_time_%J.out
#BSUB -e outputfiles/Task12_time_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python src/Task12.py 4
