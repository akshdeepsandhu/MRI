# Resources overview

This is markdown file with useful links to resources on Pulmonary MRI imaging 

# List of resources 
- https://github.com/PulmonaryMRI/
- https://github.com/PulmonaryMRI/imoco_recon


# Running interactive shell 

1. Allocate mem and run on HPC: `salloc --mem=64G --cpus-per-task=8 --nodes=1`
2. Run Apptainer Container with Mounted Directory: `apptainer exec --bind /mnt/common/Precision/Biostats/asandhu/data:/container_data /mnt/scratch/Precision/BioStats/ASandhu/images/imoco_cpu_1.0.sif /bin/bash`


# Running imoco recon: 

1. Once apptainer shell is active, activate virtual env with all the packages we need: `source /.venv/bin/activate`
2. 

