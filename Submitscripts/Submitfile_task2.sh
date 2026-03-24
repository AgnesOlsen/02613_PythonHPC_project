#!/bin/bash

#BSUB -J Task2
#BSUB -q hpc
#BSUB -W 120
#BSUB -R "rusage[mem=10GB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -o Task2_%J.out
#BSUB -e Task2_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

time python Original_python_script.py 10
time python Original_python_script.py 12
time python Original_python_script.py 14
time python Original_python_script.py 16
time python Original_python_script.py 18
time python Original_python_script.py 20

