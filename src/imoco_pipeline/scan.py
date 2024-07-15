import logging
import os
from file_handler import FileHandler
from script_generator import ScriptGenerator
from  job_manager import JobManager 

class Scan:
    def __init__(self, scan_id, raw_data_path, scratch_path):
        self.scan_id = scan_id
        self.raw_data_path = raw_data_path
        self.setup_logging()
        self.file_handler = FileHandler(raw_data_path, scratch_path, scan_id)
        self.scratch_path = self.file_handler.scratch_path
        self.h5_file_name = None
        self.script_generator = None
        self.job_manager = JobManager(self.scratch_path)
    

    def setup_logging(self):
        logger = logging.getLogger()
        if not logger.hasHandlers():
            logger.setLevel(logging.INFO)

            fh = logging.FileHandler(f'logs/mri_processing_{self.scan_id}.log')
            fh.setLevel(logging.INFO)

            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            logger.addHandler(fh)
            logger.addHandler(ch)

    def copy_dcm_files(self,dest_path):
        self.file_handler.copy_processed_dcm(dest_path)
    
    def prep(self):
        self.file_handler.copy_raw_data()
        self.h5_file_name = self.file_handler.get_h5_file()
        if not self.h5_file_name:
            raise FileNotFoundError("No .h5 file found in the copied folder. Aborting process.")
        self.file_handler.check_and_create_processed_data_folder()

        self.script_generator = ScriptGenerator(self.scratch_path, self.h5_file_name, self.scan_id)
        preprocess_script_path = os.path.join(self.scratch_path, f"run_{self.scan_id}_pre_process.sh")
        self.script_generator.generate_preprocess_script(preprocess_script_path)

        imoco_script_path = os.path.join(self.scratch_path, f"run_{self.scan_id}_imoco_process.sh")
        self.script_generator.generate_imoco_script(imoco_script_path)



