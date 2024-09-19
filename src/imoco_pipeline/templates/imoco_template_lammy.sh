#!/bin/bash
#SBATCH --mem=16G
#SBATCH --cpus-per-task=8
#SBATCH --partition=wasserman_gpu_q

# load modules
shopt -s expand_aliases
source /etc/profile.d/hpcenv.sh
module load singularity cuda11.4/toolkit/11.4.2

# execute imoco pipeline
cd {SCAN_DATA_PATH}
singularity exec --nv /mnt/scratch/Precision/BioStats/ASandhu/images/imoco_gpu_latest.sif bash -c "
source /usr/local/.gpu_venv/bin/activate
file_dir={SCAN_DATA_PATH}
imoco_dir=/usr/src/imoco_recon/imoco_py
echo '----- Starting Conversion -----'
python3 \$imoco_dir/convert_uwute.py MRI_Raw
echo '----- Starting XD-Grasp -----'
python3 \$imoco_dir/recon_xdgrasp.py MRI_Raw 
echo '----- Starting IMOCO-Recon -----'
python3 \$imoco_dir/recon_imoco.py MRI_Raw --reg_flag 1 --lambda_TV {LAMMY}
echo '----- Converting to DICOM -----'
python3 \$imoco_dir/dicom_creation.py \$file_dir
"



