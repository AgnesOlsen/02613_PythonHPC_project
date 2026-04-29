#!/bin/bash

#BSUB -J Task8_time
#BSUB -q c02613
#BSUB -W 30
#BSUB -R "rusage[mem=200MB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -o outputfiles/Task8_time_%J.out
#BSUB -e outputfiles/Task8_time_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python src/Task8.py 10
python src/Task8.py 12
python src/Task8.py 14
python src/Task8.py 16
python src/Task8.py 18
python src/Task8.py 20

