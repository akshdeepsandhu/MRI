import csv
import os
import subprocess
import logging
from Scan import Scan
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, wait, as_completed

class Controller:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.scratch_path = "/mnt/scratch/Precision/BioStats/ASandhu/data"
        self.scans = []
        self.slurm_array_script = "slurm_array_job.sh"
        self.array_template_path = "arrary_job_template.sh"

    def load_scans_from_csv(self):
        try:
            csv_data = pd.read_csv(self.csv_file_path)
            for index, row in csv_data.iterrows():
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

    def prepare_scan(self, scan):
        try:
            scan.prep()
        except Exception as e:
            logging.error(f"Error preparing scan {scan.scan_id}: {e}")
            raise

    def run_preprocessing(self):
        batch_size = 5
        futures = []

        def submit_job(scan):
            try:
                scan.submit_slurm_job()
            except Exception as e:
                logging.error(f"Error submitting SLURM job for scan {scan.scan_id}: {e}")
                raise

        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            for i, scan in enumerate(self.scans):
                future = executor.submit(submit_job, scan)
                futures.append(future)

                if (i + 1) % batch_size == 0 or (i + 1) == len(self.scans):
                    wait(futures)
                    for future in futures:
                        try:
                            future.result()  
                        except Exception as e:
                            logging.error(f"Error in scan job: {e}")
                    futures = []

    def load_and_prepare_scans(self):
        self.load_scans_from_csv()
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.prepare_scan, scan): scan for scan in self.scans}
            for future in as_completed(futures):
                scan = futures[future]
                try:
                    future.result()
                    logging.info(f"Prepared scan {scan.scan_id}")
                except Exception as e:
                    logging.error(f"Error preparing scan {scan.scan_id}: {e}")

if __name__ == "__main__":
    csv_file_path = "/mnt/cifs/ash.sandhu/bcchruser/MRI/data/mri_scan_paths.csv"
    controller = Controller(csv_file_path)
    controller.load_and_prepare_scans()
    controller.run_preprocessing()
