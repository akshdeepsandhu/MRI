import subprocess
import logging
from time import sleep

class JobManager:
    def __init__(self, scratch_path):
        self.scratch_path = scratch_path

    def submit_slurm_job(self, script_path):
        try:
            result = subprocess.run(f'sbatch {script_path}',
                                    cwd=self.scratch_path,
                                    shell=True,
                                    check=True,
                                    capture_output=True,
                                    text=True)
            logging.info(f"SLURM job submitted successfully. Output:\n{result.stdout}")
            job_id = result.stdout.strip().split()[-1]  # Extract job ID
            self.wait_for_job_completion(job_id)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error submitting SLURM job. Return code: {e.returncode}\nOutput:\n{e.output}\nError:\n{e.stderr}")
            raise

    def wait_for_job_completion(self, job_id):
        logging.info(f"Waiting for job {job_id} to complete.")
        while True:
            result = subprocess.run(f'squeue --job {job_id}', shell=True, capture_output=True, text=True)
            if job_id not in result.stdout:
                logging.info(f"Job {job_id} has completed.")
                break
            else:
                logging.info(f"Job {job_id} is still running. Checking again in 120 seconds.")
                sleep(120)


