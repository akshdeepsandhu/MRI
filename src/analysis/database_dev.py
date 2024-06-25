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

# UPDATED SCRIPT

import os
import subprocess
import ray
import time

# Initialize Ray
ray.init()

# Source and base destination directories
SOURCE_DIR = '/Volumes/RespResearch/!RAYMENT/Active Studies/iMRH Registry/Data/iMRH0100/iMRH0100A/pfiles/Exam9126_Series8_UTE'
BASE_DEST_DIR = '/path/to/network/destination'

@ray.remote
def copy_directory(source, destination):
    start_time = time.time()
    command = ["rsync", "-avz", source, destination]
    result = subprocess.run(command, capture_output=True, text=True)
    end_time = time.time()
    duration = end_time - start_time

    if result.returncode == 0:
        print(f"Directory copy successful: {source} to {destination} in {duration:.2f} seconds")
    else:
        print(f"Directory copy failed: {source} to {destination}\n{result.stderr}")

def main():
    # Extract 'iMRH0100A' from the source path
    part_to_preserve = SOURCE_DIR.split('/')[-3]

    # Construct the destination path
    destination_path = os.path.join(BASE_DEST_DIR, part_to_preserve)

    # Ensure source directory ends with a slash to copy contents
    if not SOURCE_DIR.endswith('/'):
        source_path = SOURCE_DIR + '/'
    else:
        source_path = SOURCE_DIR

    # Ensure destination directory ends with a slash
    if not destination_path.endswith('/'):
        destination_path = destination_path + '/'
    else:
        destination_path = destination_path

    # Create destination directory if it does not exist
    os.makedirs(destination_path, exist_ok=True)

    # Use Ray to parallelize the directory copy if needed
    task = copy_directory.remote(source_path, destination_path)
    
    # Wait for the task to complete
    ray.get(task)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total script execution time: {end_time - start_time:.2f} seconds")
