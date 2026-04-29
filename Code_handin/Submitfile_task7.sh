#!/bin/bash

#BSUB -J Task7
#BSUB -q hpc
#BSUB -W 45 
#BSUB -R "rusage[mem=10GB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -o outputfiles/Task7_evn2026_%J.out
#BSUB -e outputfiles/Task7_evn2026_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python src/Task7.py 10
python src/Task7.py 12
python src/Task7.py 14
python src/Task7.py 16
python src/Task7.py 18
python src/Task7.py 20
