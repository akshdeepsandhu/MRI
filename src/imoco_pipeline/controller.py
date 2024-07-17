import pandas as pd
import logging 
from scan import Scan
from utils import setup_logging

class Controller: 
    def __init__(self, gpcc_scartch_path):
        self.gpcc_scartch_path = gpcc_scartch_path
        self.scans = []
    
    def load_scans_from_csv(self,csv_file_path):
        try: 
            csv_paths = pd.read_csv(csv_file_path)
            for i, row in csv_paths.iterrows():
                raw_data_path = row['raw_data_path']
                scan_id = raw_data_path.split('/')[-3]
                scan = Scan(scan_id, raw_data_path,self.gpcc_scartch_path)
                self.scans.append(scan)
            logging.info(f"Loaded {len(self.scans)} scans from CSV.")
        except FileNotFoundError as e:
            logging.error(f"CSV file not found: {csv_file_path}")
            raise
        except KeyError as e:
            logging.error(f"CSV file is missing required columns: {e}")
            raise
    
    def copy_scan_data(self):
        for scan in self.scans: 
            logging.info(f"Setting up directories for {scan.scan_id}")
            scan.setup_dirs()
    
    def run_pcvipr(self):
        for scan in self.scans: 
            scan.pcvipr()



if __name__ == "__main__":
    setup_logging('logs/imoco_processing.log')
    csv_file_path = "/mnt/cifs/ash.sandhu/bcchruser/MRI/data/mri_scan_paths.csv"
    gpcc_scratch_path = "/mnt/scratch/Precision/BioStats/ASandhu/data/"
    controller = Controller(gpcc_scratch_path)
    controller.load_scans_from_csv(csv_file_path)
    controller.copy_scan_data()
    controller.run_pcvipr()


   