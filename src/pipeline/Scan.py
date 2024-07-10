import os
import shutil
import pandas as pd

class Scan:
    def __init__(self, scan_id, raw_data_path, scratch_path):
        self.scan_id = scan_id
        self.raw_data_path = raw_data_path
        self.scratch_path = scratch_path + "/" + self.scan_id 
        self.processed_data_path = None

    def copyRawData(self):
        '''
        Function to copy raw data from network drive to scratch drive
        '''
        print(f"Copying files for scan {self.scan_id} \nFrom: {self.raw_data_path} \nTo: {self.scratch_path}.")
        try:
            shutil.copytree(self.raw_data_path, self.scratch_path)
            print(f"Successfully copied {self.raw_data_path} to {self.scratch_path}")
        except Exception as e:
            print(f"Error copying {self.raw_data_path} to {self.scratch_path}: {e}")
    




if __name__ == "__main__":
    raw_data_path = "/mnt/cifs/ash.sandhu/fs/RespResearch/!RAYMENT/Active Studies/iMRH Registry/Data/iMRH0100/iMRH0100B/pfiles/Exam9396_Series3_UTE"
    scan_id = raw_data_path.split('/')[-3]
    scratch_path = "/mnt/scratch/Precision/BioStats/ASandhu/data"
    test_scan = Scan(scan_id=scan_id,raw_data_path=raw_data_path,scratch_path=scratch_path)
    test_scan.copyRawData()