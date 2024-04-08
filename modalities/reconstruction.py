"""
Created on 15/02/2024

@author: Andrii Gegliuk

"""


import os
import re
import subprocess


def process_src_files(root_dir):
    """
    Perform reconstruction and orientation correction on .src.gz files within a given directory.

        This function walks through the `root_dir` and its subdirectories, identifies .src.gz files,
        and applies a series of DSI Studio commands to each. These commands include image reconstruction,
        orientation correction by flipping the image on the Z axis, and background removal. It also checks
        the b-table, records ODF information, and generates various diffusion metrics.

        Parameters:
            - root_dir (str): The root directory to search for .src.gz files.

        Returns:
            - str: A message indicating the completion of the reconstruction process.
    """

    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".src.gz"):
                src_file_path = os.path.join(subdir, file)
                file_dir = os.path.dirname(src_file_path)
                base_name = os.path.basename(src_file_path).replace('.src.gz', '')

                # TODO: add parameters to find phase encoded image and run topup/eddy correction
                # TODO: if there is no phase encoded durring scan acquisition only run EDDY correction
                
                # before this step please check rotation of sample and check to adjust [Step T2][Edit][Image flip z]+[Step T2a][Remove Background] - based on current rotation fliping on Z axis is enought
                command = f'dsi_studio --action=rec --source="{src_file_path}" --method=1 --param0=0.6 --cmd="[Step T2][Edit][Image flip z]+[Step T2a][Remove Background]" --check_btable=1 --record_odf=1'
    
                try:
                    subprocess.run(command, shell=True, check=True)
                    print(f"Processing completed for {base_name}")
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {base_name}: {e}")
    return 'Recostruction completed!'



# this function is under development right now, since I want to be able to extract all values such as MD, RD, AD, color_FA and FA, looking for the best structure

# def generate_diffusion_metrics_and_nifti(root_dir):
#     """
#     Generate various diffusion metrics and NIFTI files for each subject using DSI Studio.

#     This function walks through all subdirectories under the specified root directory, identifies .src.gz files,
#     and processes them with DSI Studio to generate FA, AD, RD, MD, and other specified metrics along with a NIFTI file.

#     Parameters:
#     - root_dir (str): The root directory where preprocessing folders and .src.gz files are located.
#     """

#     for subdir, dirs, files in os.walk(root_dir):
#         for file in files:
#             if file.endswith(".src.gz"):
#                 src_file_path = os.path.join(subdir, file)
#                 subject_name = os.path.basename(src_file_path).replace('.src.gz', '')
                
#                 metrics_dir = os.path.join(subdir, f"{subject_name}_metrics")
#                 os.makedirs(metrics_dir, exist_ok=True)
                
#                 command = (
#                     f"dsi_studio "
#                     f"--action=rec "
#                     f"--source={src_file_path} "
#                     f"--output={os.path.join(metrics_dir, subject_name)}.nii.gz "
#                     f"--other_output=fa,ad,rd,md,nqa,iso,rdi,nrdi "
#                     f"--param0=0.6 "
                    
#                 )
#                 print(f"Executing command for {subject_name}: {command}")
                
#                 try:
#                     subprocess.run(command, shell=True, check=True)
#                     print(f"Diffusion metrics and NIFTI file generation completed for {subject_name}.")
#                 except subprocess.CalledProcessError as e:
#                     print(f"Error processing {subject_name}: {e}")

#     return 'Diffusion metrics and NIFTI file generation process completed!'
