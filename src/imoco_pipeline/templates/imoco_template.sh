#!/bin/bash
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4
#SBATCH --partition=wasserman_gpu_q

# load modules
shopt -s expand_aliases
source /etc/profile.d/hpcenv.sh
module load singularity cuda11.4/toolkit/11.4.2

# execute imoco pipeline
singularity exec --nv --bind {SCRATCH_PATH}:/container_data /mnt/scratch/Precision/BioStats/ASandhu/images/imoco_gpu_latest.sif bash -c "
source /usr/local/.gpu_venv/bin/activate
file_dir=/container_data/{SCAN_ID}/processed_data
imoco_dir=/usr/src/
python3 $imoco_dir/imoco_recon/imoco_py/convert_uwute.py ${file_dir}/MRI_Raw
python3 $imoco_dir/imoco_recon/imoco_py/recon_xdgrasp.py ${file_dir}/MRI_Raw
python3 $imoco_dir/imoco_recon/imoco_py/recon_imoco.py ${file_dir}/MRI_Raw --reg_flag 1 --device 0
python3 $imoco_dir/imoco_recon/imoco_py/dicom_creation.py ${file_dir}
"