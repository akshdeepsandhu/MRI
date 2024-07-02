import os
import shutil
import pandas as pd

class FileManager:
    
    def __init__(self, network_drive, scratch_space,):
        self.network_drive = network_drive
        self.scratch_space = scratch_space
        self.patient_id = network_drive.split('/')[-3]

    def copyFiles(self):
        print(f"Copying files for patient {self.patient_id} from {self.network_drive} to {self.scratch_space}.")

    def copyDICOM(self):
        print(f"Copying DICOM for patient {patient_id} from {source_path} to {dest_path}.")

    def delFiles(self):
        print(f"Deleting files for patient {patient_id} in {data_path}.")

if __name__ == "__main__":
    # test out File Manager
    # get file path to data
    csv_file_path = '/mnt/cifs/ash.sandhu/bcchruser/MRI/data/filtered_paths.csv' 
    network_drive_path = pd.read_csv(csv_file_path)['folder_path'][0]
    scratch_space_path = '/mnt/scratch/Precision/BioStats/ASandhu/data' 
    file_manager = FileManager(network_drive=network_drive_path, scratch_space=scratch_space_path)
    file_manager.copyFiles()
    