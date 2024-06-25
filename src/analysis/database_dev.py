import pandas as pd
import os 
import ray
# load csv paths that actually exist 
ute_folder_paths = pd.read_csv('data/filtered_paths.csv')['folder_path']
dir_path = ute_folder_paths[1]

SOURCE_DIR = '/Volumes/RespResearch/!RAYMENT/Active Studies/iMRH Registry/Data/iMRH0100/iMRH0100A/pfiles/Exam9126_Series8_UTE/'
BASE_DEST_DIR = '/Volumes/ash.sandhu/data/'

sub_folder = SOURCE_DIR.split('/')[-3]
destination_path = os.path.join(BASE_DEST_DIR, sub_folder)


def copy_directory(source, destination):
    command = ["rsync", "-avz", source, destination]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Directory copy successful: {source} to {destination}")
    else:
        print(f"Directory copy failed: {source} to {destination}\n{result.stderr}")

copy_directory(source=SOURCE_DIR,destination=destination_path)