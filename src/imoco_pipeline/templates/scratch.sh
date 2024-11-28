singularity shell --nv --bind /mnt/scratch/Precision/BioStats/ASandhu/data/iMRH0100A/raw_data:/container_data /mnt/scratch/Precision/BioStats/ASandhu/images/imoco_gpu_latest.sif
source /usr/local/.gpu_venv/bin/activate
file_dir=/container_data
/usr/src/imoco_recon/imoco_py/
python recon_imoco.py ${file_dir}/MRI_Raw --reg_flag 1 
moco_npy/recon_imoco_npy.py ${file_dir}--reg_flag 1 --lambda_TV 0.01
python recon_imoco_npy.py ${file_dir} --reg_flag 1 --lambda_TV 0.01
python imoco_reimoco_npy/dicom_from_npy.py ${file_dir} ${orig_dicom_dir}

singularity shell --nv --bind /mnt/scratch/Precision/BioStats/ASandhu/imrh_warehouse/data/iMRH0039C/:/container_data /mnt/scratch/Precision/BioStats/ASandhu/images/imoco_gpu_latest.sif