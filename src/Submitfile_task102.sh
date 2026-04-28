#!/bin/bash

#BSUB -J Task10fix_time
#BSUB -q c02613
#BSUB -W 30
#BSUB -R "rusage[mem=200MB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -o Task10fix_time_%J.out
#BSUB -e Task10fix_time_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

time python Task10.py 10
time python Task10.py 12
time python Task10.py 14
time python Task10.py 16
time python Task10.py 18
time python Task10.py 20
time python Task10.py 40
time python Task10.py 60
time python Task10.py 100
time python Task10.py 500
time python Task10.py 1000