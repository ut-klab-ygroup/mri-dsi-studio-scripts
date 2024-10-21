import os
import pandas as pd
from colorama import Fore, Style, Back

from modalities.extract_raw_data_bruker import create_and_process_dti_dirs
from modalities.utilities.utils import (
    list_projects,
    select_project,
    load_subjects_from_excel,
    group_by_condition,
    get_subject_name
)
from modalities.reconstruction import process_src_files
from modalities.data_base_creation import create_dsi_database



if __name__ == "__main__":
    input_dir = r"C:\preprocessing\raw_analysis"    
    output_dir = r"C:\preprocessing\mri_analysis"   

    
    projects = list_projects(input_dir) # listing  all projects in the input directory
 
    if projects:
        
        selected_project = select_project(projects) # Prompt the user to select a project for initializing extraction

        if selected_project:
            project_input_dir = os.path.join(input_dir, selected_project)
            project_output_dir = os.path.join(output_dir, selected_project, 'DTI', 'preprocessing')

            if not any(os.listdir(project_input_dir)):
                print(Fore.RED + Style.BRIGHT + f"The project directory '{selected_project}' is empty. Please add raw data from Paravision 360 to perform analysis." + Style.RESET_ALL)
            else:
                os.makedirs(project_output_dir, exist_ok=True)
                print(Back.GREEN + f"Processing data for project {selected_project}..." + Style.RESET_ALL)

                
                excel_file = os.path.join(project_input_dir, 'subjects.xlsx') # Load subjects from the Excel file
                if not os.path.exists(excel_file):
                    print(Fore.RED + f"No 'subjects.xlsx' found in the selected project '{selected_project}'!" + Style.RESET_ALL)
                else:
                    subjects_df = load_subjects_from_excel(excel_file)
                    if not subjects_df.empty:
                        
                        subjects_by_condition = group_by_condition(subjects_df) # grouping subjects by condition TODO:

                        # checking if reconstruction has already been done in order to save time and not return reconstuction each time
                        reconstruction_needed = True
                        existing_reconstructions = []

                        # checking if any reconstructed files already exist based on file extention .src.gz.dti.fib.gz and existing data structure 
                        for condition in subjects_by_condition.keys():
                            condition_output_dir = os.path.join(project_output_dir, condition)
                            if os.path.exists(condition_output_dir):
                                for subject_folder in os.listdir(condition_output_dir):
                                    subject_dir = os.path.join(condition_output_dir, subject_folder)
                                    if os.path.isdir(subject_dir):
                                        reconstructed_file = os.path.join(subject_dir, f"{subject_folder}.src.gz.dti.fib.gz")
                                        if os.path.exists(reconstructed_file):
                                            existing_reconstructions.append(subject_folder)

                        if existing_reconstructions:
                            print(Fore.YELLOW + "Reconstructed files detected for the following subjects:" + Style.RESET_ALL)
                            for subj in existing_reconstructions:
                                print(Fore.YELLOW + f"- {subj}" + Style.RESET_ALL)
                            while True:
                                user_choice = input("Do you want to rerun the reconstruction for existing subjects? (yes/no): ").strip().lower()
                                if user_choice in ['yes', 'y']:
                                    reconstruction_needed = True
                                    break
                                elif user_choice in ['no', 'n']:
                                    reconstruction_needed = False
                                    break
                                else:
                                    print("Please enter 'yes' or 'no'.")

                        # processing each subject based on their condition extracted from excel file subjects.xlsx
                        for condition, subjects in subjects_by_condition.items():
                            condition_output_dir = os.path.join(project_output_dir, condition)
                            os.makedirs(condition_output_dir, exist_ok=True)

                            for subject_id in subjects:
                                subject_input_dir = os.path.join(project_input_dir, subject_id)
                                if not os.path.exists(subject_input_dir):
                                    print(Fore.RED + f"Subject directory '{subject_id}' not found." + Style.RESET_ALL)
                                    continue

                                if not any(os.listdir(subject_input_dir)):
                                    print(Fore.RED + f"The subject directory '{subject_id}' is empty. Please add raw data." + Style.RESET_ALL)
                                    continue

                                # getting subject_name
                                subject_name = get_subject_name(subject_id)
                                subject_preprocessing_dir = os.path.join(condition_output_dir, subject_name)

                                # checking if the reconstructed file already exists
                                reconstructed_file = os.path.join(subject_preprocessing_dir, f"{subject_name}.src.gz.dti.fib.gz")
                                if os.path.exists(reconstructed_file):
                                    if not reconstruction_needed:
                                        print(Fore.GREEN + f"Reconstructed file already exists for subject '{subject_name}'. Skipping data extraction and reconstruction." + Style.RESET_ALL)
                                        continue
                                    else:
                                        print(Fore.YELLOW + f"Reconstructed file already exists for subject '{subject_name}'. Rerunning reconstruction as per user choice." + Style.RESET_ALL)
                                else:
                                    print(Fore.YELLOW + f"No reconstructed file found for subject '{subject_name}'. Performing data extraction and reconstruction." + Style.RESET_ALL)

                                print(Back.CYAN + f"\nProcessing subject {subject_id} under condition '{condition}'..." + Style.RESET_ALL)

                                # STEP T1: Data extraction and preparation
                                print(Fore.YELLOW + "Starting data extraction and preparation..." + Style.RESET_ALL)
                                subject_preprocessing_dir, subject_name_extracted = create_and_process_dti_dirs(subject_input_dir, condition_output_dir)
                                # Ensure subject_name matches subject_name_extracted

                                if subject_preprocessing_dir and subject_name_extracted:
                                # STEP T2: Reconstruction process (rotation, checking b-values, etc.)
                                    print(Fore.YELLOW + "Starting reconstruction process for .src.gz files..." + Style.RESET_ALL)
                                    process_src_files(subject_preprocessing_dir)
                                    print(Fore.GREEN + Style.BRIGHT + f"Processed files for subject '{subject_name_extracted}'." + Style.RESET_ALL)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"Skipping reconstruction for '{subject_id}' due to previous errors." + Style.RESET_ALL)

                        # STEP C1: Creating database (normalization & registration for group-level analysis) # this process is moving to new file
                        # print(Back.GREEN + "Starting the creation of the DSI Studio database..." + Style.RESET_ALL)
                        # create_dsi_database(project_output_dir) TODO: registration needs to be done separatelly

                        print(Fore.GREEN + "Processing completed. Next step will be to create a databased based on your conditions!" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "No subjects marked for processing in the Excel file." + Style.RESET_ALL)
        else:
            print(Fore.RED + Style.BRIGHT + "No valid project selected, exiting." + Style.RESET_ALL)
    else:
        print(Fore.RED + Style.BRIGHT + "No projects found, please check the input directory." + Style.RESET_ALL)
