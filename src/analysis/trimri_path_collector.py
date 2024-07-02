import os
import pandas as pd
import ray
import re

@ray.remote
def find_ute_folders(path):
    ute_paths = []
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if dir_path.endswith('_UTE'):
                ute_paths.append(dir_path)
    return ute_paths

def collect_all_paths(base_directory):
    subdirs = [os.path.join(base_directory, subdir) for subdir in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, subdir))]
    futures = [find_ute_folders.remote(subdir) for subdir in subdirs]
    results = ray.get(futures)
    
    all_paths = []
    for result in results:
        all_paths.extend(result)
    
    return all_paths

def save_paths_to_csv(paths, output_csv_path):
    all_paths_df = pd.DataFrame(paths, columns=['folder_path'])
    all_paths_df.to_csv(output_csv_path, index=False)
    print(f"Filtered paths have been written to {output_csv_path}")

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

def main():
    # Initialize Ray
    ray.init(ignore_reinit_error=True)
    
    base_directory = '/Volumes/RespResearch/!RAYMENT/Active Studies/iMRH Registry/Data/'
    output_csv_path = 'data/all_ute_paths.csv'
    tri_mri_ids_csv = 'data/trimri_ute_list.csv'

    # Collect all paths and save to CSV
    all_paths = collect_all_paths(base_directory)
    save_paths_to_csv(all_paths, output_csv_path)
    
    # Load the tri_mri_ids data
    tri_mri_ids = load_tri_mri_ids(tri_mri_ids_csv)
    
    # Get visit ids
    visit_ids = tri_mri_ids['visit_id'].tolist()
    
    # Read the database csv
    all_paths_df = pd.read_csv(output_csv_path)
    all_ute_paths = all_paths_df['folder_path'].tolist()
    
    # Filter paths
    filtered_paths = filter_paths_by_visit_ids(all_ute_paths, visit_ids)
    filtered_paths_df = pd.DataFrame(filtered_paths, columns=['folder_path'])
    filtered_paths_df.to_csv('data/filtered_paths.csv', index=False)
    print(filtered_paths_df)

    # Shutdown Ray
    ray.shutdown()

if __name__ == "__main__":
    main()
