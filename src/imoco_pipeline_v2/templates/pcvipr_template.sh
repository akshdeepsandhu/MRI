#!/bin/bash
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8

# load modules
shopt -s expand_aliases
source /etc/profile.d/hpcenv.sh
unload_bcchr
load_cvmfs
module load apptainer

# execute pre-processing
apptainer exec --bind {SCAN_DATA_PATH}:/container_data /mnt/scratch/Precision/BioStats/ASandhu/images/pcvipr_latest.sif bash -c "
cd {SCAN_DATA_PATH}
pcvipr_recon_binary -f {H5_FILE_NAME} -pils -dat_plus_dicom -resp_gate thresh -pregate_kdata -export_kdata
rm *.txt
rm *.dat
rm *.complex
"