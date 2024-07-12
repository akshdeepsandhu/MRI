#!/bin/bash
#SBATCH --job-name=controller_job   
#SBATCH --output=controller_job.out 
#SBATCH --error=controller_job.err  
#SBATCH --nodes=1                   
#SBATCH --cpus-per-task=4           
#SBATCH --mem=64GB                   

shopt -s expand_aliases
source /etc/profile.d/hpcenv.sh

module load gcc
module load conda

source /mnt/common/Precision/Miniconda3/miniconda/etc/profile.d/conda.sh
conda activate /mnt/common/Precision/Miniconda3/opt/miniconda3/envs/imoco_transfer

