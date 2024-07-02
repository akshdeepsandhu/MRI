#!/bin/bash
#SBATCH --mem=128G
#SBATCH --cpus-per-task=4
#SBATCH --nodes=1
#SBATCH --partition=wasserman_gpu_q

module load singularity cuda11.4/toolkit/11.4.2
singularity shell --nv --bind /mnt/scratch/Precision/BioStats/ASandhu/data:/container_data /mnt/scratch/Precision/BioStats/ASandhu/images/imoco_gpu_latest.sif
source /usr/local/.gpu_venv/bin/activate
file_dir=/container_data/iMRH0100A/
imoco_dir=/usr/src/
python3 $imoco_dir/imoco_recon/imoco_py/recon_xdgrasp.py ${file_dir}/MRI_Raw
python3 $imoco_dir/imoco_recon/imoco_py/recon_imoco.py ${file_dir}/MRI_Raw --reg_flag 1 --device 0
python3 $imoco_dir/imoco_recon/imoco_py/dicom_creation.py ${file_dir}

pcvipr_recon_binary -dat_plus_dicom -f ScanArchive_604875MR750_20220907_085641943.h5 -export_kdata