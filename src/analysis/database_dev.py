# Scratch file to develop new database with all paths we want
import pandas as pd
import os


base_directory = '/Volumes/RespResearch/!RAYMENT/Active Studies/iMRH Registry/Data/'

# List to store all paths
all_paths = []

# Traverse the directory structure
for root, dirs, files in os.walk(base_directory):
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        if dir_path.endswith('_UTE'):
            all_paths.append(dir_path)
            print(dir_path)

# Create a DataFrame with the collected paths
all_paths_df = pd.DataFrame(all_paths, columns=['folder_path'])

# parallel version
import os
import pandas as pd
import ray

# Initialize Ray
ray.init(ignore_reinit_error=True)

# Define the base directory to start the search
base_directory = '/Volumes/RespResearch/!RAYMENT/Active Studies/iMRH Registry/Data/'

# List to store all paths
all_paths = []

@ray.remote
def find_ute_folders(path):
    ute_paths = []
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if dir_path.endswith('UTE'):
                ute_paths.append(dir_path)
    return ute_paths

# Collect all immediate subdirectories of the base directory
subdirs = [os.path.join(base_directory, subdir) for subdir in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, subdir))]

# Use Ray to parallelize the directory traversal
futures = [find_ute_folders.remote(subdir) for subdir in subdirs]

# Get the results
results = ray.get(futures)

# Flatten the list of lists
for result in results:
    all_paths.extend(result)

# Create a DataFrame with the collected paths
all_paths_df = pd.DataFrame(all_paths, columns=['folder_path'])

# Save the DataFrame to a CSV file
output_csv_path = 'data/all_ute_paths.csv'
all_paths_df.to_csv(output_csv_path, index=False)

print(f"Filtered paths have been written to {output_csv_path}")

# Shutdown Ray
ray.shutdown()

# now let's read the database csv and find all the ones in the excel that rachel shared
