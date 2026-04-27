#!/bin/bash

#BSUB -J Task4_evn2026
#BSUB -q hpc
#BSUB -W 4
#BSUB -R "rusage[mem=1GB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -o Task4_evn2026_%J.out
#BSUB -e Task4_evn2026_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

kernprof -l Task4.py 4
python -m line_profiler Task4.py.lprof
