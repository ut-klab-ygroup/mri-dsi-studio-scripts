"""
Created on 01/03/2024

@author: Andrii Gegliuk

"""


import glob
import os
import shutil
import subprocess
from datetime import datetime 

# def create_dsi_database(output_dir, database_dir_name="data_base"):
#     """
#     This function locates all .dti.fib.gz files in a given preprocessing directory,
#     copies them into a new database directory, and initiates DSI Studio to create
#     a database from these files. The database directory is created at the same 
#     level as the preprocessing directory.

#     Parameters:
#         - output_dir (str): The path to the preprocessing directory where the DTI files are initially processed and stored.
#         - database_dir_name (str, optional): The name of the directory to be created. Default is "data_base".

#     Outputs:
#         - A new directory at the DTI level containing the copied DTI files and a 
#         console output indicating the success or failure of the database creation process.
    
#     """
#     dti_base_dir = os.path.dirname(output_dir)  # This will navigate up from 'preprocessing' to 'DTI'
#     database_dir = os.path.join(dti_base_dir, database_dir_name)  # Create the database directory parallel to 'preprocessing'
#     os.makedirs(database_dir, exist_ok=True)

#     print(f"Preprocessing directory: {output_dir}")
#     print(f"Database directory: {database_dir}")

#     # Find all .dti.fib.gz files recursively in the preprocessing directory
#     dti_files = glob.glob(os.path.join(output_dir, "**", "*.dti.fib.gz"), recursive=True)

#     if not dti_files:
#         print("No .dti.fib.gz files found. Please check the preprocessing directory path and file names.")
#     else:
#         print(f"Found {len(dti_files)} files to copy.")

#     for src_path in dti_files: # copy files to data_base dir
#         dst_path = os.path.join(database_dir, os.path.basename(src_path))
#         shutil.copy(src_path, dst_path)
#         print(f"Copied {src_path} to {dst_path}")
        
#     current_date = datetime.now().strftime('%Y%m%d')

#     # DSI Studio command
#     # dsi_studio_cmd = f'dsi_studio --action=atl --cmd=db --source="{database_dir}" --template=1 --index_name=fa'
#     dsi_studio_cmd = f'dsi_studio --action=atl --cmd=db --source="{database_dir}" --output="{database_dir}/data_base_{current_date}.fa.db.fib.gz" --template=1 --index_name=fa'
    
#     try:
#         subprocess.run(dsi_studio_cmd, shell=True, check=True)
#         print("DSI Studio database creation completed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error during DSI Studio database creation: {e}")
