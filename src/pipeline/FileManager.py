import os
import shutil
import pandas as pd

class FileManager:
    
    def __init__(self, network_drive, scratch_space,):
        self.network_drive = network_drive
        self.patient_id = network_drive.split('/')[-3]
        self.scratch_space = scratch_space + "/" + self.patient_id 

    def copyFiles(self):
        print(f"Copying files for patient {self.patient_id} \nFrom: {self.network_drive} \nTo: {self.scratch_space}.")
        try:
            shutil.copytree(self.network_drive, self.scratch_space)
            print(f"Successfully copied {self.network_drive} to {self.scratch_space}")
        except Exception as e:
            print(f"Error copying {self.network_drive} to {self.scratch_space}: {e}")

    def copyDICOM(self):
        print(f"Copying DICOM for patient {patient_id} from {source_path} to {dest_path}.")

    def delFiles(self):
        print(f"Deleting files for patient {self.patient_id} in {self.scratch_space}.")
        shutil.rmtree(self.scratch_space) 

if __name__ == "__main__":
    # test out File Manager
    csv_file_paths = pd.read_csv('/mnt/cifs/ash.sandhu/bcchruser/MRI/data/filtered_paths.csv')
    for row in csv_file_paths.iterrows():
        network_drive_path = row[1]['folder_path']
        scratch_space_path = '/mnt/scratch/Precision/BioStats/ASandhu/data' 
        file_manager = FileManager(network_drive=network_drive_path, scratch_space=scratch_space_path)
        file_manager.copyFiles()
        file_manager.delFiles()
    
    