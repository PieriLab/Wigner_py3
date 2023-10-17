#!/bin/bash

#SBATCH -p elipierilab
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -J wignerbatch2hhtda
#SBATCH --mem=50G
#SBATCH -t 10:00:00
#SBATCH --constraint=[h100]
#SBATCH --qos gpu_access
#SBATCH --gres=gpu:1

#Load necessary modules

#srun run.sh
module load tc/23.08

python3 wignerbatch2hhtda.py
