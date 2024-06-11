# Resources overview

This is markdown file with useful links to resources on Pulmonary MRI imaging 

# HPC info: 
- User mounted data at: `/mnt/cifs/ash.sandhu/bcchruser/`


# List of resources 
- https://github.com/PulmonaryMRI/
- https://github.com/PulmonaryMRI/imoco_recon
- https://larsonlab.github.io/MRI-education-resources/Introduction.html

# Running interactive shell (GPU)
1. Allocate mem and run on HPC: `salloc --mem=128G --cpus-per-task=4 --nodes=1 --partition=wasserman_gpu_q`
2. Run Apptainer sif with mounted dir: `singularity shell --nv \ 
													--bind /mnt/common/Precision/Biostats/asandhu/data/:/container_data \ 
													/mnt/scratch/Precision/BioStats/ASandhu/images/imoco_gpu.sif`

# Running imoco recon (GPU: 
1. Once shell is active, activate virutal env `source /usr/local/.venv/bin/activate`
2. Define useful variable: `imoco_dir=/usr/src/` ; `file_dir=/container_data/iMRHXXX/` 
3. Convert raw .h5 file into correct format: `python3 imoco_recon/imoco_py/convert_uwute.py ${file_dir}/MRI_Raw`
4. Run recon: 
	a. xd-grasp reconstruction: `python3 imoco_recon/imoco_py/recon_xdgrasp.py ${file_dir}/MRI_Raw`
	b. mocolor reconstruction: `python3 imoco_recon/imoco_py/recon_imoco.py ${file_dir}/MRI_Raw --reg_flag 1 --lambda_TV 0.01`

# Script: (once in GPU node)
`
module load singularity cuda11.4/toolkit/11.4.2
singularity shell --nv --bind /mnt/common/Precision/Biostats/asandhu/data/:/container_data /mnt/scratch/Precision/BioStats/ASandhu/images/imoco_gpu.sif

`

# Running interactive shell (CPU)

1. Allocate mem and run on HPC: `salloc --mem=128G --cpus-per-task=12 --nodes=1`
2. Run Apptainer Container with Mounted Directory: `singularity exec --bind /mnt/common/Precision/Biostats/asandhu/data/:/container_data /mnt/scratch/Precision/BioStats/ASandhu/images/imoco_cpu_1.0.sif /bin/bash`

# Running imoco recon (CPU):

1. Once apptainer shell is active, activate virtual env with all the packages we need: `source /.venv/bin/activate`
2. Run recon (w/ field derivation): `python3 imoco_recon/imoco_py/recon_imoco.py /container_data/lung_mri/MRI_Raw --reg_flag 1 --device -1`
3. Run recon (w/out field derivation): `python3 imoco_recon/imoco_py/recon_xdgrasp.py /container_data/lung_mri/MRI_Raw --device -1`

