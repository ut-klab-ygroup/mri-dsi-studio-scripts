"""
Created on 15/02/2024

@author: Andrii Gegliuk

"""


import os
import subprocess
from colorama import init, Fore, Style


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
                command = f'dsi_studio --action=rec --source="{src_file_path}" --method=1 --param0=0.6 --cmd="[Step T2a][Remove Background]" --check_btable=1 --record_odf=1'
    
                try:
                    subprocess.run(command, shell=True, check=True)
                    print(f"Processing completed for {base_name}")
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {base_name}: {e}")
    return 'Recostruction completed!'

