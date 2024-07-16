import pandas as pd
import logging 
from scan import Scan
from concurrent.futures import ThreadPoolExecutor, wait, as_completed

class Controller: 
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.scratch_path = "/mnt/scratch/Precision/BioStats/ASandhu/data"
        self.scans = []
    
    def load_scans_from_csv(self):
        try: 
            csv_paths = pd.read_csv(self.csv_file_path)
            for i, row in csv_paths.iterrows():
                raw_data_path = row['raw_data_path']
                scan_id = raw_data_path.split('/')[-3]
                scan = Scan(scan_id, raw_data_path, self.scratch_path)
                self.scans.append(scan)
            logging.info(f"Loaded {len(self.scans)} scans from CSV.")
        except FileNotFoundError as e:
            logging.error(f"CSV file not found: {self.csv_file_path}")
            raise
        except KeyError as e:
            logging.error(f"CSV file is missing required columns: {e}")
            raise
        
    def load_and_prepare_scans(self):
        self.load_scans_from_csv()
        for scan in self.scans:
            try:
                scan.prep()
            except Exception as e:
                logging.error(f"Error preparing scan {scan.scan_id}: {e}")
                raise

    def run_imoco(self):
        for scan in self.scans: 
            try:
                scan.run_imoco_script()
            except Exception as e: 
                logging.error(f"Error running imoco for scan {scan.scan_id}: {e}")
                raise


    def run_preprocess(self):
        for scan in self.scans:
            try: 
                scan.run_preprcess_script()    
            except Exception as e: 
                logging.error(f"Error running pre-processing for scan {scan.scan_id}: {e}")
                raise
    
    def copy_dcm(self):
        for scan in controller.scans: 
            try: 
                dest_path = '/mnt/cifs/ash.sandhu/bcchruser/MRI/data/imoco_processed_data/'
                scan.copy_dcm_files(dest_path)
            except Exception as e: 
                logging.error(f"Error transfering files for scan {scan.scan_id}: {e}")
                raise


if __name__ == "__main__":
    csv_file_path = "/mnt/cifs/ash.sandhu/bcchruser/MRI/data/mri_scan_paths.csv"
    controller = Controller(csv_file_path)
    controller.load_and_prepare_scans()
    #controller.run_preprocess()
    #controller.run_imoco()
    #controller.copy_dcm()
   