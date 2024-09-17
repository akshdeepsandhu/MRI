import logging
import os
import subprocess
from time import sleep

def setup_logging(log_file_path):

    logger = logging.getLogger()
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        fh = logging.FileHandler(log_file_path)
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

def generate_script(template_path, script_path, replacements):
        try:
            with open(template_path, 'r') as template_file:
                template_content = template_file.read()

            for placeholder, value in replacements.items():
                template_content = template_content.replace(placeholder, value)

            dir = os.path.dirname(script_path)

            if not os.path.exists(dir):
                os.makedirs(dir)

            with open(script_path, 'w') as script_file:
                script_file.write(template_content)

            os.chmod(script_path, 0o755)
            logging.info(f"Script generated at {script_path}")
        except IOError as e:
            logging.error(f"Error handling template file: {e}")
            raise

def generate_pcvipr_script(script_path, scan_data_path, h5_file_name):
    generate_script(
        template_path='templates/pcvipr_template.sh',
        script_path=script_path,
        replacements={
            '{SCAN_DATA_PATH}': scan_data_path,
            '{H5_FILE_NAME}': h5_file_name
        }
    )

def generate_imoco_script(script_path, scan_data_path):
    generate_script(
        template_path='templates/imoco_template.sh',
        script_path=script_path,
        replacements={
            '{SCAN_DATA_PATH}': scan_data_path
        }
    )

def generate_imoco_script_lammy(script_path, scan_data_path, lammy):
    generate_script(
        template_path='templates/imoco_template_lammy.sh',
        script_path=script_path,
        replacements={
            '{SCAN_DATA_PATH}' : scan_data_path,
            '{LAMMY}' : str(lammy),
        }
    )


def submit_slurm_job(script_path, cwd_path):
    try:
        result = subprocess.run(f'sbatch {script_path}',
                                cwd=cwd_path,
                                shell=True,
                                check=True,
                                capture_output=True,
                                text=True)
        logging.info(f"SLURM job submitted successfully. Output:\n{result.stdout}")
        job_id = result.stdout.strip().split()[-1]  # Extract job ID
        wait_for_job_completion(job_id)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error submitting SLURM job. Return code: {e.returncode}\nOutput:\n{e.output}\nError:\n{e.stderr}")
        raise

def wait_for_job_completion(job_id):
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
