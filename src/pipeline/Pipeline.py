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