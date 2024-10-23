import os
import pandas as pd
from colorama import Fore, Style, Back
import json
from datetime import datetime

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


def load_configuration(config_file):
    """Load the configuration file (JSON) or create a new one if it doesn't exist."""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {"projects": {}}

# save database based on extracted files
def save_configuration(config, config_file):
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)


def update_configuration(config, project_name, subject_name, cohort):
    if project_name not in config['projects']:
        config['projects'][project_name] = {"subjects_processed": {}, "cohorts": {}, "last_run": ""}

    config['projects'][project_name]['subjects_processed'][subject_name] = "processed"

    if cohort not in config['projects'][project_name]['cohorts']:
        config['projects'][project_name]['cohorts'][cohort] = []

    if subject_name not in config['projects'][project_name]['cohorts'][cohort]:
        config['projects'][project_name]['cohorts'][cohort].append(subject_name)

    # capturing date
    config['projects'][project_name]['last_run'] = datetime.now().strftime("%Y-%m-%d")

def ask_reconstruction():
    """Ask the user if they want to rerun reconstruction for all previously processed subjects."""
    while True:
        user_choice = input("Do you want to rerun the reconstruction for existing subjects? (yes/no): ").strip().lower()
        if user_choice in ['yes', 'y']:
            return True
        elif user_choice in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    input_dir = r"C:\preprocessing\raw_analysis"
    output_dir = r"C:\preprocessing\mri_analysis"
    
    projects = list_projects(input_dir)  # Listing all projects in the input directory
    
    if projects:
        selected_project = select_project(projects)  # Ask the user to select a project
        
        if selected_project:
            project_input_dir = os.path.join(input_dir, selected_project)
            project_output_dir = os.path.join(output_dir, selected_project, 'DTI', 'preprocessing')
            
            # define the config file location
            config_file = os.path.join(project_output_dir, 'pipeline_config.json')
            
            # load the existing configuration
            config = load_configuration(config_file)

            if not any(os.listdir(project_input_dir)):
                print(Fore.RED + Style.BRIGHT + f"The project directory '{selected_project}' is empty. Please add raw data from Paravision 360 to perform analysis." + Style.RESET_ALL)
            else:
                os.makedirs(project_output_dir, exist_ok=True)
                print(Back.GREEN + f"Processing data for project {selected_project}..." + Style.RESET_ALL)

                excel_file = os.path.join(project_input_dir, 'subjects.xlsx')  # load subjects from the Excel file
                if not os.path.exists(excel_file):
                    print(Fore.RED + f"No 'subjects.xlsx' found in the selected project '{selected_project}'!" + Style.RESET_ALL)
                else:
                    subjects_df = load_subjects_from_excel(excel_file)
                    if not subjects_df.empty:
                        subjects_by_condition = group_by_condition(subjects_df)  # grouping subjects by condition

                        # checking if any reconstructed files already exist based on filesystem
                        existing_reconstructions = []
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

                                subject_name = get_subject_name(subject_id)
                                subject_preprocessing_dir = os.path.join(condition_output_dir, subject_name)

                                # Checking if the reconstructed file already exists
                                reconstructed_file = os.path.join(subject_preprocessing_dir, f"{subject_name}.src.gz.dti.fib.gz")
                                if os.path.exists(reconstructed_file):
                                    existing_reconstructions.append(subject_name)

                        # display and ask user if they want to rerun reconstruction for existing subjects
                        if existing_reconstructions:
                            print(Fore.YELLOW + "Reconstructed files detected for the following subjects:" + Style.RESET_ALL)
                            for subj in existing_reconstructions:
                                print(Fore.YELLOW + f"- {subj}" + Style.RESET_ALL)
                            
                            # ask if the user wants to rerun reconstruction
                            rerun_reconstruction = ask_reconstruction()
                        else:
                            rerun_reconstruction = False

                        # processing each subject
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

                                subject_name = get_subject_name(subject_id)
                                subject_preprocessing_dir = os.path.join(condition_output_dir, subject_name)
                                reconstructed_file = os.path.join(subject_preprocessing_dir, f"{subject_name}.src.gz.dti.fib.gz")

                                # Check if the reconstructed file already exists
                                if os.path.exists(reconstructed_file):
                                    if not rerun_reconstruction:
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
                                    # STEP T2: Reconstruction process
                                    print(Fore.YELLOW + "Starting reconstruction process for .src.gz files..." + Style.RESET_ALL)
                                    process_src_files(subject_preprocessing_dir)
                                    print(Fore.GREEN + Style.BRIGHT + f"Processed files for subject '{subject_name_extracted}'." + Style.RESET_ALL)

                                    # Update the configuration with the processed subject
                                    # Assuming cohort information is extracted from subject_name (e.g., 'S123_HF4' where 'HF4' is the cohort) TODO: checking if this will work on project with no cohort ???
                                    cohort = subject_name.split('_')[1] if '_' in subject_name else 'default_cohort'
                                    update_configuration(config, selected_project, subject_name, cohort)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"Skipping reconstruction for '{subject_id}' due to previous errors." + Style.RESET_ALL)
                        
                        # save database TODO: check how it's writing new files
                        save_configuration(config, config_file)

                        print(Fore.GREEN + "Processing completed. Next step will be to create a database based on your conditions!" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "No subjects marked for processing in the Excel file." + Style.RESET_ALL)
        else:
            print(Fore.RED + Style.BRIGHT + "No valid project selected, exiting." + Style.RESET_ALL)
    else:
        print(Fore.RED + Style.BRIGHT + "No projects found, please check the input directory." + Style.RESET_ALL)


