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
import re
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
            if dir_path.endswith('_UTE'):
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


def load_tri_mri_ids(path_to_csv):
    df = pd.read_csv(path_to_csv)
    melted_df = pd.melt(df, id_vars=['id', 'visits'], 
                        value_vars=['visit1_date', 'visit2_date'], 
                        var_name='visit_number', 
                        value_name='visit_date')
    
    melted_df['visit'] = melted_df.apply(
        lambda row: row['visits'].split(',')[0] if row['visit_number'] == 'visit1_date' else row['visits'].split(',')[1], 
        axis=1
    )
    
    melted_df['visit_id'] = melted_df['id'] + melted_df['visit']
    melted_df = melted_df.drop(columns=['visits', 'visit_number', 'visit'])
    melted_df = melted_df.sort_values(by='id').reset_index(drop=True)
    
    return melted_df


def filter_paths_by_visit_ids(paths, visit_ids):
    filtered_paths = [path for path in paths if any(re.search(visit_id, path) for visit_id in visit_ids)]
    return filtered_paths

# now let's read the database csv and find all the ones in the excel that rachel shared
all_paths = pd.read_csv('data/all_ute_paths.csv')
tri_mri_ids = load_tri_mri_ids('data/trimri_ute_list.csv')
# get visit ids
visit_ids = tri_mri_ids['visit_id'].tolist()
all_ute_paths = all_paths['folder_path'].to_list()
# only paths that exist 
filtered_paths = filter_paths_by_visit_ids(all_ute_paths, visit_ids)
