import os
import subprocess

class Reconstruction:
    def __init__(self, scratch_space):
        self.scratch_space = scratch_space

    def imocoRecon(self, patient_id):
        data_path = os.path.join(self.scratch_space, patient_id)
        print(f"Running MRI reconstruction for patient {patient_id} on data in {data_path}.")

        # SLURM allocation command
        salloc_command = "salloc --mem=128G --cpus-per-task=4 --nodes=1 --partition=wasserman_gpu_q"
        self.run_command(salloc_command)

        # Load necessary modules
        module_command = "module load singularity cuda11.4/toolkit/11.4.2"
        self.run_command(module_command)

        # Run Singularity shell with binding
        singularity_command = (
            "singularity shell --nv --bind "
            f"{self.scratch_space}:/container_data "
            "/mnt/scratch/Precision/BioStats/ASandhu/images/imoco_gpu_latest.sif"
        )
        self.run_command(singularity_command)

        # Activate virtual environment
        activate_command = "source /usr/local/.gpu_venv/bin/activate"
        self.run_command(activate_command)

        # Define file and directory paths
        file_dir = "/container_data/" + patient_id
        imoco_dir = "/usr/src/"

        # Run the reconstruction scripts
        recon_xdgrasp_command = f"python3 {imoco_dir}/imoco_recon/imoco_py/recon_xdgrasp.py {file_dir}/MRI_Raw"
        self.run_command(recon_xdgrasp_command)

        recon_imoco_command = f"python3 {imoco_dir}/imoco_recon/imoco_py/recon_imoco.py {file_dir}/MRI_Raw --reg_flag 1 --device 0"
        self.run_command(recon_imoco_command)

        dicom_creation_command = f"python3 {imoco_dir}/imoco_recon/imoco_py/dicom_creation.py {file_dir}"
        self.run_command(dicom_creation_command)

    def run_command(self, command):
        """Utility method to run a shell command."""
        print(f"Executing command: {command}")
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"Error executing command: {command}\n{result.stderr.decode('utf-8')}")
        else:
            print(result.stdout.decode('utf-8'))

# Example usage
if __name__ == "__main__":
    scratch_space = "/mnt/scratch/Precision/BioStats/ASandhu/data"
    reconstruction = Reconstruction(scratch_space)
    patient_id = "iMRH0074B"
    reconstruction.imocoRecon(patient_id)