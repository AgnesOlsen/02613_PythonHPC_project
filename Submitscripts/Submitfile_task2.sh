#!/bin/bash

#BSUB -J Task2_evn2026_newtime
#BSUB -q hpc
#BSUB -W 120
#BSUB -R "rusage[mem=10GB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -o Task2_evn2026_newtime_%J.out
#BSUB -e Task2_evn2026_newtime_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python src/Task2.py 10
python src/Task2.py 12
python src/Task2.py 14
python src/Task2.py 16
python src/Task2.py 18
python src/Task2.py 20

