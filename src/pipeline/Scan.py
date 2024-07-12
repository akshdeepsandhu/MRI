import os
import shutil
import subprocess
import logging
from time import sleep

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler('log/mri_processing.log')
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

setup_logging()

class Scan:
    def __init__(self, scan_id, raw_data_path, scratch_path):
        self.scan_id = scan_id
        self.raw_data_path = raw_data_path
        self.scratch_path = os.path.join(scratch_path, self.scan_id)
        self.processed_data_folder_path = os.path.join(self.scratch_path, "processed_data")
        self.slurm_script_path = os.path.join(self.scratch_path, f"run_{self.scan_id}_pre_process.sh")
        self.h5_file_name = None

    def copy_raw_data(self):
        logging.info(f"Copying files for scan {self.scan_id} from {self.raw_data_path} to {self.scratch_path}.")
        if os.path.exists(self.scratch_path):
            logging.info(f"Folder already exists: {self.scratch_path}. Skipping copy.")
            return
        
        retry_count = 3
        for attempt in range(retry_count):
            try:
                shutil.copytree(self.raw_data_path, self.scratch_path)
                logging.info(f"Successfully copied {self.raw_data_path} to {self.scratch_path}")
                break
            except Exception as e:
                if attempt < retry_count - 1:  # Retry logic
                    logging.error(f"Error copying {self.raw_data_path} to {self.scratch_path}: {e}. Retrying...")
                    sleep(2 ** attempt)  # Exponential backoff
                else:
                    logging.error(f"Failed after {retry_count} attempts.")
                    raise IOError(f"Error copying {self.raw_data_path} to {self.scratch_path}: {e}")
    
    def get_h5_file(self):
        try:
            for file in os.listdir(self.scratch_path):
                if file.endswith(".h5"):
                    self.h5_file_name = file
                    logging.info(f"Found .h5 file: {self.h5_file_name}")
                    return file
            logging.warning("No .h5 file found in the copied folder.")
            return None
        except FileNotFoundError as e:
            logging.error(f"Directory not found: {self.scratch_path}")
            raise

    def check_and_create_processed_data_folder(self):
        if not os.path.exists(self.processed_data_folder_path):
            os.makedirs(self.processed_data_folder_path)
            logging.info(f"Processed data folder created at {self.processed_data_folder_path}")
        else:
            logging.info(f"Processed data folder already exists at {self.processed_data_folder_path}")


    def generate_slurm_script(self):
        template_path = 'slurm_template.sh'
        try:
            with open(template_path, 'r') as template_file:
                template_content = template_file.read()
            
            script_content = template_content.replace('{SCRATCH_PATH}', self.scratch_path).replace('{H5_FILE_NAME}', self.h5_file_name)
            
            with open(self.slurm_script_path, 'w') as script_file:
                script_file.write(script_content)
            
            os.chmod(self.slurm_script_path, 0o755)
            logging.info(f"SLURM script generated at {self.slurm_script_path}")
        except IOError as e:
            logging.error(f"Error handling template file: {e}")
            raise

    def submit_slurm_job(self):
        try:
            result = subprocess.run(f'sbatch {self.slurm_script_path}',
                                    cwd=self.scratch_path,
                                    shell=True,
                                    check=True,
                                    capture_output=True,
                                    text=True)
            logging.info(f"SLURM job submitted successfully. Output:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error submitting SLURM job. Return code: {e.returncode}\nOutput:\n{e.output}\nError:\n{e.stderr}")
            raise
        
    def prep(self):
        self.copy_raw_data()
        h5_file = self.get_h5_file()
        if not h5_file:
            raise FileNotFoundError("No .h5 file found in the copied folder. Aborting process.")
        self.check_and_create_processed_data_folder()
        self.generate_slurm_script()

