import pandas as pd
import logging
from scan import Scan
from utils import setup_logging
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed

class Controller:
    def __init__(self, gpcc_scratch_path):
        self.gpcc_scratch_path = gpcc_scratch_path
        self.scans = []

    def load_scans_from_csv(self, csv_file_path):
        try:
            csv_paths = pd.read_csv(csv_file_path)
            for i, row in csv_paths.iterrows():
                raw_data_path = row['raw_data_path']
                scan_id = raw_data_path.split('/')[-3]
                scan = Scan(scan_id, raw_data_path, self.gpcc_scratch_path)
                self.scans.append(scan)
            logging.info(f"Loaded {len(self.scans)} scans from CSV.")
        except FileNotFoundError as e:
            logging.error(f"CSV file not found: {csv_file_path}")
            raise
        except KeyError as e:
            logging.error(f"CSV file is missing required columns: {e}")
            raise

    def process_scan(self, scan):
        logging.info(f"Processing scan {scan.scan_id}")
        scan.setup_dirs()
        scan.pcvipr()
        scan.imoco()

    def process_scans_in_batches(self, batch_size=2):
        for i in range(0, len(self.scans), batch_size):
            batch = self.scans[i:i + batch_size]
            with ThreadPoolExecutor(max_workers=batch_size) as executor:
                futures = [executor.submit(self.process_scan, scan) for scan in batch]
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        logging.error(f"An error occurred: {e}")



if __name__ == "__main__":
    # Load paths
    with open('imoco.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)
    setup_logging(yaml_data['logs'])
    controller = Controller(yaml_data['gpcc_scratch_path'])
    controller.load_scans_from_csv(yaml_data['csv_file_path'])
    controller.process_scans_in_batches(batch_size=2)