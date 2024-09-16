import os
import logging
import shutil
import subprocess
import glob

from utils import generate_pcvipr_script, generate_imoco_script, generate_imoco_script_lammy, submit_slurm_job
class Scan:
    def __init__(self, scan_id, raw_data_path, gpcc_scratch_path):
        self.scan_id = scan_id
        self.raw_data_path = raw_data_path
        self.gpcc_scratch_path = gpcc_scratch_path
        self.scan_data_path = os.path.join(gpcc_scratch_path,scan_id,"raw_data")

        # vars for later
        self.h5_file_name = None
        self.pcvipr_script = os.path.join(gpcc_scratch_path,scan_id,"scripts","pcvipr.sh")
        self.imoco_script = os.path.join(gpcc_scratch_path,scan_id,"scripts","imoco.sh")

    def copy_raw_data(self):
        logging.info(f"Copying files from {self.raw_data_path} to {self.scan_data_path}.")
        if os.path.exists(self.scan_data_path):
            logging.info(f"Folder already exists: {self.scan_data_path}. Skipping copy.")
            return
        try:
            shutil.copytree(self.raw_data_path, self.scan_data_path)
            logging.info(f"Successfully copied {self.raw_data_path} to {self.scan_data_path}")
        except Exception as e:
            raise IOError(f"Error copying {self.raw_data_path} to {self.scan_data_path}: {e}")
    
    def get_h5_file(self):
        try:
            for file in os.listdir(self.scan_data_path):
                if file.endswith(".h5"):
                    logging.info(f"Found .h5 file: {file}")
                    return file
            logging.warning("No .h5 file found in the copied folder.")
            return None
        except FileNotFoundError as e:
            logging.error(f"Directory not found: {self.scan_data_path}")
            raise
    
    def setup_dirs(self):
        self.copy_raw_data()
        self.h5_file_name = self.get_h5_file()
        if not self.h5_file_name:
            raise FileNotFoundError("No .h5 file found in the copied folder. Aborting process.") 
    
    def pcvipr(self):
        # run pcvipr
        # make script 
        logging.info(f"Creating pcvipr script for {self.scan_id}")
        generate_pcvipr_script(script_path=self.pcvipr_script,
                               scan_data_path=self.scan_data_path,
                               h5_file_name=self.h5_file_name)
        logging.info(f"Running pcvipr script for {self.scan_id}")
        # submit script
        submit_slurm_job(script_path=self.pcvipr_script,
                         cwd_path=self.scan_data_path)
    
    def imoco(self):
        # run imoco 
        # make script
        logging.info(f"Creating imoco script for {self.scan_id}")
        generate_imoco_script(script_path=self.imoco_script,
                             scan_data_path=self.scan_data_path)
        logging.info(f"Running imoco script for {self.scan_id}")
        # submit script
        submit_slurm_job(script_path=self.imoco_script,
                         cwd_path=self.scan_data_path)
    
    def imoco_lammy(self):
        # run imoco 
        # make script
        logging.info(f"Creating imoco script for {self.scan_id}")
        lammy_list = [0,0.01,0.025,0.05,0.075,0.1]
        for lammy in lammy_list:
            generate_imoco_script_lammy(script_path=self.imoco_script,
                                scan_data_path=self.scan_data_path, 
                                lammy=lammy
                                )
            logging.info(f"Running imoco script for {self.scan_id} with {lammy} regularization")
            # submit script
            submit_slurm_job(script_path=self.imoco_script,
                            cwd_path=self.scan_data_path)


