#!/bin/bash

#BSUB -J Task9_timenew
#BSUB -q c02613
#BSUB -W 30
#BSUB -R "rusage[mem=200MB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -o Task9_timenew_%J.out
#BSUB -e Task9_timenew_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python Task9.py 10
python Task9.py 12
python Task9.py 14
python Task9.py 16
python Task9.py 18
python Task9.py 20
