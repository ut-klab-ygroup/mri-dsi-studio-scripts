import os
import csv
from colorama import init, Fore, Style, Back

from modalities.extract_raw_data_bruker import create_and_process_dti_dirs
from modalities.utilities.utils import list_projects, select_project
from modalities.reconstruction import process_src_files
from modalities.data_base_creation import create_dsi_database
from modalities.utilities.parameters import *


if __name__ == "__main__":
    input_dir = RAW_DATA
    output_dir = ANALYSIS_DATA

    # function listing all directories within input folder (input folder expected to have only raw data under the specified project name)
    projects = list_projects(input_dir)

    if projects:
        # processing data based on the project that was selected
        selected_project = select_project(projects)

        if selected_project:
            project_input_dir = os.path.join(input_dir, selected_project)

            if not any(os.listdir(project_input_dir)):
                print(Fore.RED + Style.BRIGHT + f"The project directory '{selected_project}' is empty. Please add raw data from Paravision 360 to perform analysis." + Style.RESET_ALL)
            else:

                project_output_dir = os.path.join(output_dir, selected_project, 'DTI', 'preprocessing')
                os.makedirs(project_output_dir, exist_ok=True)
                print(Back.GREEN + f"Processing data for project {selected_project}..." + Style.RESET_ALL )
                
                # STEP T1: Data extraction and preparation
                create_and_process_dti_dirs(project_input_dir, project_output_dir)
                
                # STEP T2: Reconstruction process
                print(Back.GREEN + "Starting the reconstruction of .src.gz files..." + Style.RESET_ALL)
                reconstruction_message = process_src_files(project_output_dir)
                print(reconstruction_message)

                # STEP C1: Creating database (normalization & registration for group-level analysis) 
                print(Back.GREEN + "Starting the creation of the DSI Studio database..." + Style.RESET_ALL)
                create_dsi_database(project_output_dir)
                
                print(Fore.GREEN + "Processing completed. Please open database in DSI Studio to check if there is any artifacts or missregistration to remove some subjects!" + Style.RESET_ALL)
        else:
            print(Fore.RED + Style.BRIGHT + "No valid project selected, exiting." + Style.RESET_ALL)
    else:
        print(Fore.RED + Style.BRIGHT + "No projects found, please check the input directory." + Style.RESET_ALL)


