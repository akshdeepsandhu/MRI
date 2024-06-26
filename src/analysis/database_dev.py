# Simple script to copy over data from network drive to userdrive for analysis
import pandas as pd
import shutil
import os

# Function to copy a directory from source to destination
def copy_directory(source_dir, destination_dir):
    try:
        shutil.copytree(source_dir, destination_dir)
        print(f"Successfully copied {source_dir} to {destination_dir}")
    except Exception as e:
        print(f"Error copying {source_dir} to {destination_dir}: {e}")

# Function to read CSV using pandas and initiate the copying process
def copy_directories_from_csv(csv_file_path, destination_base_path):
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        source_path = row[0]  
        folder_name = source_path.split('/')[-3]
        print("Starting copying folder:"  + folder_name)
        destination_path = os.path.join(destination_base_path, folder_name)
        copy_directory(source_path, destination_path)

# Example usage
csv_file_path = '/mnt/cifs/ash.sandhu/bcchruser/MRI/data/filtered_paths.csv'  # Path to your CSV file
destination_base_path = '/mnt/scratch/Precision/BioStats/ASandhu/data'  # Base destination folder
copy_directories_from_csv(csv_file_path, destination_base_path)
