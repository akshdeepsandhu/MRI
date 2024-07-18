#!/bin/bash
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4
#SBATCH --nodes=1
#SBATCH --partition=wasserman_gpu_q
shopt -s expand_aliases
source /etc/profile.d/hpcenv.sh
unload_bcchr
load_cvmfs
module load singularity cuda11.4/toolkit/11.4.2
singularity shell --nv --bind /mnt/scratch/Precision/BioStats/ASandhu/data:/container_data /mnt/scratch/Precision/BioStats/ASandhu/images/imoco_gpu_latest.sif
source /usr/local/.gpu_venv/bin/activate
file_dir=/container_data/iMRH0100A/processed_data
imoco_dir=/usr/src/imoco_recon/imoco_py/
python3 $imoco_dir/convert_uwute.py ${file_dir}/MRI_Raw
python3 $imoco_dir/recon_xdgrasp.py ${file_dir}/MRI_Raw
python3 $imoco_dir/recon_imoco.py ${file_dir}/MRI_Raw --reg_flag 1 --lambda_TV 0.01
python3 $imoco_dir/imoco_recon/imoco_py/dicom_creation.py ${file_dir}

# scratch - pcvipr recon: 
apptainer shell --bind /mnt/scratch/Precision/BioStats/ASandhu/data/iMRH0100A:/container_data:/container_data /mnt/scratch/Precision/BioStats/ASandhu/images/pcvipr_latest.sif bash -c "
pcvipr_recon_binary -f raw_data/ScanArchive_604875MR750_20220907_085641943.h5 -pils -dat_plus_dicom -resp_gate thresh -pregate_kdata -export_kdata
