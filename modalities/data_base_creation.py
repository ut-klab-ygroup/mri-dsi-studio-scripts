"""
Created on 01/03/2024

@author: Andrii Gegliuk

"""


import os
import shutil
import subprocess
from glob import glob

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


def create_dsi_database(output_dir, database_dir_name="data_base"):
    """
    Creates a DSI Studio database from .dti.fib.gz files found in a determined preprocessing directory
    within the output directory, then stores the database in a newly created directory at the same level as
    the preprocessing directory. This assumes that the output directory's structure will always include
    a uniquely named condition-specific folder (e.g., 'Cuprizone') containing a 'preprocessing' folder.

        Parameters:
            - output_dir (str): The parent directory containing condition-specific subdirectory with the 'preprocessing' folder.
            - database_dir_name (str): Name for the new database directory to be created alongside 'preprocessing'.
    """
    # looking for preprocessing iside main condition folder
    condition_dir = next(os.walk(output_dir))[1][0]
    condition_path = os.path.join(output_dir, condition_dir)


    preprocessing_dir = os.path.join(condition_path, "preprocessing")  # Define the paths for the preprocessing and new database directories
    database_dir = os.path.join(condition_path, database_dir_name)

    os.makedirs(database_dir, exist_ok=True) # Ensure the database directory is created

    # looking for all .dti.fib.gz files within the pross directory
    dti_files = glob(os.path.join(preprocessing_dir, "**", "*.dti.fib.gz"), recursive=True)

    # copying files
    for src_path in dti_files:
        dst_path = os.path.join(database_dir, os.path.basename(src_path))
        shutil.copy(src_path, dst_path)

    # database DSI studio command: prameters --temlate=1 refers to C57BL6 mouse and --index_name=fa to the fa images which we need to create DB
    dsi_studio_cmd = f'dsi_studio --action=atl --cmd=db --source="{database_dir}" --template=1 --index_name=fa' 
    
    try:
        subprocess.run(dsi_studio_cmd, shell=True, check=True)
        print("DSI Studio database creation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during DSI Studio database creation: {e}")
