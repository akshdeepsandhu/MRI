import os
import shutil
import logging
from time import sleep

class FileHandler:
    def __init__(self, raw_data_path, scratch_path, scan_id):
        self.raw_data_path = raw_data_path
        self.scratch_path = os.path.join(scratch_path, scan_id)
        self.scan_id = scan_id

    def copy_raw_data(self):
        logging.info(f"Copying files for scan {self.scan_id} from {self.raw_data_path} to {self.scratch_path}.")
        if os.path.exists(self.scratch_path):
            logging.info(f"Folder already exists: {self.scratch_path}. Skipping copy.")
            return
        try:
            shutil.copytree(self.raw_data_path, self.scratch_path)
            logging.info(f"Successfully copied {self.raw_data_path} to {self.scratch_path}")
        except Exception as e:
            raise IOError(f"Error copying {self.raw_data_path} to {self.scratch_path}: {e}")

    def get_h5_file(self):
        try:
            for file in os.listdir(self.scratch_path):
                if file.endswith(".h5"):
                    logging.info(f"Found .h5 file: {file}")
                    return file
            logging.warning("No .h5 file found in the copied folder.")
            return None
        except FileNotFoundError as e:
            logging.error(f"Directory not found: {self.scratch_path}")
            raise

    def check_and_create_processed_data_folder(self):
        processed_data_folder_path = os.path.join(self.scratch_path, "processed_data")
        if not os.path.exists(processed_data_folder_path):
            os.makedirs(processed_data_folder_path)
            logging.info(f"Processed data folder created at {processed_data_folder_path}")
        else:
            logging.info(f"Processed data folder already exists at {processed_data_folder_path}")

    def copy_processed_dcm(self, destination_folder_path):
        processed_data_folder_path = os.path.join(self.scratch_path, "processed_data")
        if not os.path.exists(processed_data_folder_path):
             raise FileNotFoundError(f"Processed data folder does not exist: {processed_data_folder_path}")

        if not os.path.exists(destination_folder_path):
             raise FileNotFoundError(f"Destination folder does not exist: {destination_folder_path}")
        
        for file in os.listdir(processed_data_folder_path):
            if file.endswith(".DCM"): 
                source_file = os.path.join(processed_data_folder_path,file)
                destination_file = os.path.join(destination_folder_path,file)
                try: 
                    shutil.copy2(source_file,destination_file)
                    logging.info(f"Copied {source_file} to {destination_file}")
                except Exception as e: 
                    logging.error(f"Error copying {source_file} to {destination_file}: {e}")
                    raise
    
            

