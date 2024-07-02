import os
import shutil
import pandas as pd

class FileManager:
    
    def __init__(self, network_drive, scratch_space,):
        self.network_drive = network_drive
        self.scratch_space = scratch_space

    def copyFiles(self, patient_id):
        print(f"Copying files for patient {patient_id} from {source_path} to {dest_path}.")

    def copyDICOM(self, patient_id):
        print(f"Copying DICOM for patient {patient_id} from {source_path} to {dest_path}.")

    def delFiles(self, patient_id):
        print(f"Deleting files for patient {patient_id} in {data_path}.")


class Reconstruction:
    def __init__(self, scratch_space):
        self.scratch_space = scratch_space

    def imocoRecon(self, patient_id):
        print(f"Running MRI reconstruction for patient {patient_id} on data in {data_path}.")

    def saveOutput(self, patient_id):
        print(f"Saving output from MRI reconstruction for patient {patient_id} to {data_path}.")
        

class Pipeline:
    def __init__(self, network_drive, scratch_space):
        self.file_manager = FileManager(network_drive, scratch_space)
        self.reconstruction = Reconstruction(scratch_space)

    def startpipeline(self):
        print("Pipeline initialized.")
        

    def processPatient(self, patient_id):
        self.file_manager.copyFiles(patient_id)
        self.reconstruction.imocoRecon(patient_id)
        self.reconstruction.saveOutput(patient_id)
        self.file_manager.copyDICOM(patient_id)
        self.file_manager.delFiles(patient_id)

    def exitCheck(self):
        print("Running garbage collection and cleanup.")
        

    def endPipeline(self):
        print("Pipeline ended.")
        


if __name__ == "__main__":
    csv_file_path = '/mnt/cifs/ash.sandhu/bcchruser/MRI/data/filtered_paths.csv' 
    file_path = pd.read_csv(csv_file_path)
    network_drive = "/path/to/network_drive"
    scratch_space = "/path/to/scratch_space"

    pipeline = Pipeline(network_drive, scratch_space)
    pipeline.startpipeline()
    patient_id = "patient_001"

    pipeline.processPatient(patient_id)
    pipeline.exitCheck()
    pipeline.endPipeline()
