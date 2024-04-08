"""
Created on 01/03/2024

@author: Andrii Gegliuk

"""


import glob
import os
import shutil
import subprocess

def create_dsi_database(output_dir, database_dir_name="data_base"):
    condition_dir = next(os.walk(output_dir))[1][0]
    condition_path = os.path.join(output_dir, condition_dir)

    preprocessing_dir = os.path.join(condition_path, "DTI", "preprocessing")
    database_dir = os.path.join(condition_path, "DTI", database_dir_name)

    os.makedirs(database_dir, exist_ok=True)

    print(f"Preprocessing directory: {preprocessing_dir}")
    print(f"Database directory: {database_dir}")

    dti_files = glob.glob(os.path.join(preprocessing_dir, "**", "*.dti.fib.gz"), recursive=True)

    if not dti_files:
        print("No .dti.fib.gz files found. Please check the preprocessing directory path and file names.")
    else:
        print(f"Found {len(dti_files)} files to copy.")

    for src_path in dti_files:
        dst_path = os.path.join(database_dir, os.path.basename(src_path))
        shutil.copy(src_path, dst_path)
        print(f"Copied {src_path} to {dst_path}")  # Confirm each copy operation

    dsi_studio_cmd = f'dsi_studio --action=atl --cmd=db --source="{database_dir}" --template=1 --index_name=fa'
    
    try:
        subprocess.run(dsi_studio_cmd, shell=True, check=True)
        print("DSI Studio database creation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during DSI Studio database creation: {e}")


#### old original function 

# def db_preparation(root_dir, database_dir_suffix="Data_Base"):
#     database_dir = os.path.join(root_dir, database_dir_suffix)
#     os.makedirs(database_dir, exist_ok=True)

#     for root, dirs, files in os.walk(root_dir):
#         for file in files:
#             if file.endswith(".dti.fib.gz"):
#                 full_file_path = os.path.join(root, file)
#                 shutil.copy(full_file_path, database_dir)
#                 # count number of files?
#                 print(f"Moved: {full_file_path} -> {database_dir}")

# db_preparation('/home/sharapova/mri_management_tool/DTI_test_data/minori/preprocessing')