#!/bin/bash

#BSUB -J 5016Task5_evn26
#BSUB -q hpc
#BSUB -W 120
#BSUB -R "rusage[mem=400MB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -n 16
#BSUB -R "span[hosts=1]"
#BSUB -o outputfiles/5016Task5_evn26_%J.out
#BSUB -e outputfiles/5016Task5_evn26_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026
python src/Task5.py 50
