#!/bin/bash

#BSUB -J Task10prof1
#BSUB -q c02613
#BSUB -W 30
#BSUB -R "rusage[mem=200MB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -o Task10prof1_time_%J.out
#BSUB -e Task10prof1_time_%J.err

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

#nsys profile --force-overwrite true -o prof_data_filetask10_ python Task9.py 4
nsys profile --force-overwrite true --wait=all -o prof_data_filetask10_ python Task9.py 4
sleep 2
nsys stats prof_data_filetask10_.nsys-rep 

