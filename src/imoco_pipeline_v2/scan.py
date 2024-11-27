import os 
import subprocess
from time import sleep
from setup_logging import logger
import numpy as np


class Scan: 
    def __init__(self, scan_id, data_path):
        self.scan_id = scan_id
        self.data_path = data_path
        self.h5_file_path = self._set_h5_file_path()


    def _set_h5_file_path(self) -> str: 
        for file in os.listdir(self.data_path):
            if file.endswith('.h5') and not file.endswith('Raw.h5'):
                logger.info(f"Found .h5 file: {file}")
                return f'{self.data_path}/{file}'
            else: 
                logger.warning("No .h5 file found in the copied folder.")
                return 
            

    def _make_script_content(self, template_path: str, script_path: str, replacements: dict) -> bool:
        try: 
            with open(template_path, 'r') as template_file:
                template_content = template_file.read()

            for placeholder, value in replacements.items():
                template_content = template_content.replace(placeholder, value)

            with open(script_path, 'w') as script_file:
                script_file.write(template_content)

            os.chmod(script_path, 0o755)
            logger.info(f"Script written to file: {script_path}")

        except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                raise
    

    def _submit_slurm_job(self, job_script : str, job_dir: str) ->  None:
        try:
            result = subprocess.run(f'sbatch {job_script}',
                                    cwd=job_dir,
                                    shell=True,
                                    check=True,
                                    capture_output=True,
                                    text=True)
            logger.info(f"SLURM job submitted successfully. Output: {result.stdout}")
            job_id = result.stdout.strip().split()[-1]  
            self._wait_for_job_completion(job_id)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error submitting SLURM job. Return code: {e.returncode}\nOutput:\n{e.output}\nError:\n{e.stderr}")
            raise
    

    def _wait_for_job_completion(self, job_id: str) -> None:
        logger.info(f"Waiting for job {job_id} to complete.")
        while True:
            result = subprocess.run(f'squeue --job {job_id}', shell=True, capture_output=True, text=True)
            if job_id not in result.stdout:
                logger.info(f"Job {job_id} has completed.")
                break
            else:
                wait_time = 180
                logger.info(f"Job {job_id} is still running. Checking again in {wait_time} seconds.")
                sleep(wait_time)
    

    def _write_pcvipr_script(self) -> str:

        pcvipr_script_name = f"{self.scan_id}_pcvipr.sh"
        pcvipr_script_path = os.path.join(self.data_path, pcvipr_script_name)

        self._make_script_content(
            template_path="templates/pcvipr_template.sh",
            script_path=pcvipr_script_path,
            replacements={
                '{SCAN_DATA_PATH}': self.data_path,
                '{H5_FILE_NAME}': self.h5_file_path
            }
        )

        return pcvipr_script_name
    

    def _write_imoco_script(self, lammy) -> str: 
        
        imoco_script_name = f"{self.scan_id}_imoco_lammy_{lammy}.sh"
        imoco_script_path = os.path.join(self.data_path, imoco_script_name)
        self._make_script_content(
            template_path="templates/imoco_lammy_template.sh",
            script_path=imoco_script_path,
            replacements={
                '{SCAN_DATA_PATH}': self.data_path,
                 '{LAMMY}' : str(lammy),
            }
        )

        return imoco_script_name

    def run_pcvipr_job(self) -> None: 
        pcvipr_script = self._write_pcvipr_script()
        self._submit_slurm_job(job_script=pcvipr_script,job_dir=self.data_path)
        
    def run_imoco_job(self, lammy_lst: np.array ) -> None: 
        for lammy in lammy_lst:
            imoco_script = self._write_imoco_script(lammy=np.round(lammy,4))
            self._submit_slurm_job(job_script=imoco_script,job_dir=self.data_path)
            

if __name__ == '__main__':
    data_path = '/mnt/scratch/Precision/BioStats/ASandhu/imrh_warehouse/data/iMRH0039C/'
    test_scan = Scan('iMRH0039C', data_path)
    #test_scan.run_pcvipr_job()
    test_scan._write_pcvipr_script()
    lammy_list = np.linspace(0,0.05,5)
    test_scan._write_imoco_script(lammy=0.05)

