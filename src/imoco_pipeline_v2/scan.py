import os 
import subprocess
from time import sleep
from setup_logging import logger


class Scan: 
    def __init__(self, scan_id, data_path):
        self.scan_id = scan_id
        self.data_path = data_path
        self.h5_file_path = self._set_h5_file_path()


    def _set_h5_file_path(self) -> str: 
        for file in os.listdir(self.data_path):
            if file.endswith('.h5') and not file.endswith('Raw.h5'):
                logging.info(f"Found .h5 file: {file}")
                return f'{self.data_path}/{file}'
            else: 
                logging.warning("No .h5 file found in the copied folder.")
                return None
            

    def make_script_content(self, template_path: str, replacements: dict) -> str:

        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        for placeholder, value in replacements.items():
            template_content = template_content.replace(placeholder, value)

        return template_content

    def write_pcvipr_script(self, write_to_file=True) -> None:

        self.pcvipr_script_name = f"{self.scan_id}_pcvipr.sh"

        script_content = self.make_script_content(
            template_path="templates/pcvipr_template.sh",
            replacements={
                '{SCAN_DATA_PATH}': self.data_path,
                '{H5_FILE_NAME}': self.h5_file_path
            }
        )

        if write_to_file:
            script_path = os.path.join(self.data_path, self.pcvipr_script_name)
            with open(script_path, 'w') as script_file:
                script_file.write(script_content)
            os.chmod(script_path, 0o755)
            logging.info(f"Script written to file: {script_path}")

    

    def submit_slurm_job(self) ->  None:
        try:
            result = subprocess.run(f'sbatch {self.pcvipr_script_name}',
                                    cwd=self.data_path,
                                    shell=True,
                                    check=True,
                                    capture_output=True,
                                    text=True)
            logging.info(f"SLURM job submitted successfully. Output:\n{result.stdout}")
            job_id = result.stdout.strip().split()[-1]  
            self.wait_for_job_completion(job_id)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error submitting SLURM job. Return code: {e.returncode}\nOutput:\n{e.output}\nError:\n{e.stderr}")
            raise
    
    def wait_for_job_completion(self, job_id: str) -> None:
        logging.info(f"Waiting for job {job_id} to complete.")
        while True:
            result = subprocess.run(f'squeue --job {job_id}', shell=True, capture_output=True, text=True)
            if job_id not in result.stdout:
                logging.info(f"Job {job_id} has completed.")
                break
            else:
                wait_time = 200
                logging.info(f"Job {job_id} is still running. Checking again in {wait_time} seconds.")
                sleep(wait_time)

if __name__ == '__main__':
    data_path = '/mnt/scratch/Precision/BioStats/ASandhu/imrh_warehouse/data/iMRH0039C'
    test_scan = Scan('iMRH0039C', data_path)
    print(test_scan.h5_file_path)
    test_scan.write_pcvipr_script(write_to_file=True)