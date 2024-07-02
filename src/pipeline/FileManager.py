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
