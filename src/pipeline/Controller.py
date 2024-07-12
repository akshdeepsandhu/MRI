import csv
import os
import subprocess
import logging
from Scan import Scan
import pandas as pd

class Controller:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.scratch_path = "/mnt/scratch/Precision/BioStats/ASandhu/data"
        self.scans = []
        self.slurm_array_script = "slurm_array_job.sh"
        self.array_template_path = "arrary_job_template.sh"

    def load_scans_from_csv(self):
        try:
            csv = pd.read_csv(self.csv_file_path)
            for index, row in csv.iterrows():
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
    
    def prepare_scans(self):
        for scan in self.scans:
            try: 
                scan.prep()
            except Exception as e: 
                logging.error(f"Error preparing scan {scan.scan_id}: {e}")
                raise

    def run_preprocessing(self):
        for scan in self.scans:
            try: 
                scan.submit_slurm_job()
            except Exception as e: 
                logging.error(f"Error preparing scan {scan.scan_id}: {e}")
                raise
    
    

if __name__ == "__main__":
    csv_file_path = "/mnt/cifs/ash.sandhu/bcchruser/MRI/data/mri_scan_paths.csv"    
    controller = Controller(csv_file_path)
    controller.load_scans_from_csv()
    controller.prepare_scans()
    controller.run_preprocessing() 
    
