#!/bin/bash
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4

# load modules
shopt -s expand_aliases
source /etc/profile.d/hpcenv.sh
unload_bcchr
load_cvmfs
module load apptainer

# execute pre-processing
apptainer exec --bind {SCRATCH_PATH}:/container_data /mnt/scratch/Precision/BioStats/ASandhu/images/pcvipr_latest.sif bash -c "
mkdir -p /container_data/processed_data
cd /container_data/processed_data
pcvipr_recon_binary -f ../{H5_FILE_NAME} -pils -dat_plus_dicom -resp_gate thresh -pregate_kdata -export_kdata
"