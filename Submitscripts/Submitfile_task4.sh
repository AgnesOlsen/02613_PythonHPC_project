#!/bin/bash

#BSUB -J Task4
#BSUB -q hpc
#BSUB -W 4
#BSUB -R "rusage[mem=1GB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -o Task4_%J.out
#BSUB -e Task4_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613
cd .. 
cd src
kernprof -l Task4.py 1
python -m line_profiler -rmt "Task4.py.lprof" 