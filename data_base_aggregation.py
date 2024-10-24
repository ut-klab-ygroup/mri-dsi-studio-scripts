import os
import json
import glob
import shutil
import subprocess
from datetime import datetime
from colorama import Fore, Style
from modalities.utilities.utils import list_projects, select_project

def load_configuration(config_file):
    """Load the configuration file (JSON)."""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        print(Fore.RED + f"Configuration file {config_file} not found." + Style.RESET_ALL)
        return None

def list_projects_from_config(config):
    """List projects from the configuration."""
    return list(config.get('projects', {}).keys())

def select_cohorts_from_config(cohorts):
    """Allow the user to select cohorts from the configuration."""
    print(Fore.CYAN + "Available cohorts:" + Style.RESET_ALL)
    for idx, cohort in enumerate(cohorts):
        print(f"{idx + 1}. {cohort}")
    
    selected = input(Fore.YELLOW + "Please enter the numbers of the cohorts you want to process (comma-separated): " + Style.RESET_ALL)
    selected_indices = [int(i.strip()) -1 for i in selected.split(',') if i.strip().isdigit()]
    selected_cohorts = [cohorts[i] for i in selected_indices if 0 <= i < len(cohorts)]
    return selected_cohorts

def select_subjects_from_cohort(subjects, cohort):
    """Allow the user to select subjects from a cohort."""
    print(Fore.CYAN + f"Available subjects in cohort '{cohort}':" + Style.RESET_ALL)
    for idx, subject in enumerate(subjects):
        print(f"{idx +1}. {subject}")
    selected = input(Fore.YELLOW + "Please enter the numbers of the subjects you want to process (comma-separated), or press Enter to select all: " + Style.RESET_ALL)
    if not selected.strip():
        return subjects  # Return all subjects
    else:
        selected_indices = [int(i.strip()) -1 for i in selected.split(',') if i.strip().isdigit()]
        selected_subjects = [subjects[i] for i in selected_indices if 0 <= i < len(subjects)]
        return selected_subjects

def create_dsi_database(project_output_dir, selected_project, selected_cohorts, selected_subjects_by_cohort, database_dir_name):
    """
    Create a DSI Studio database based on selected cohorts and subjects.

    Parameters:
        - project_output_dir (str): Path to the project's preprocessing directory.
        - selected_project (str): The selected project name.
        - selected_cohorts (list): List of selected cohorts.
        - selected_subjects_by_cohort (dict): Dictionary of selected subjects by cohort.
        - database_dir_name (str): The name of the database directory to create.
    """
    dti_base_dir = os.path.dirname(project_output_dir)
    database_base_dir = os.path.join(dti_base_dir, 'data_base')
    os.makedirs(database_base_dir, exist_ok=True)
    database_dir = os.path.join(database_base_dir, database_dir_name)
    os.makedirs(database_dir, exist_ok=True)
    
    print(Fore.CYAN + f"Preprocessing directory: {project_output_dir}" + Style.RESET_ALL)
    print(Fore.CYAN + f"Database directory: {database_dir}" + Style.RESET_ALL)

    # Collect .dti.fib.gz files
    dti_files = []
    for cohort in selected_cohorts:
        subjects = selected_subjects_by_cohort[cohort]
        for condition in ['Group', 'Single']:
            condition_path = os.path.join(project_output_dir, condition)
            if os.path.exists(condition_path):
                for subject_name in subjects:
                    subject_dir = os.path.join(condition_path, subject_name)
                    if os.path.exists(subject_dir):
                        fib_files = glob.glob(os.path.join(subject_dir, "*.dti.fib.gz"))
                        if fib_files:
                            dti_files.extend(fib_files)
                        else:
                            print(Fore.RED + f"No .dti.fib.gz files found for subject {subject_name} in {condition}" + Style.RESET_ALL)
                    else:
                        print(Fore.YELLOW + f"Subject directory {subject_dir} does not exist in {condition}. Skipping." + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"Condition directory {condition_path} does not exist. Skipping." + Style.RESET_ALL)
    if not dti_files:
        print(Fore.RED + "No .dti.fib.gz files found in the selected subjects." + Style.RESET_ALL)
        return
    else:
        print(Fore.GREEN + f"Found {len(dti_files)} files to copy to the database directory." + Style.RESET_ALL)
    
    # Copy files to database directory
    for src_path in dti_files:
        dst_path = os.path.join(database_dir, os.path.basename(src_path))
        shutil.copy(src_path, dst_path)
        print(Fore.GREEN + f"Copied {src_path} to {dst_path}" + Style.RESET_ALL)
    
    # run DSI Studio
    current_date = datetime.now().strftime('%Y%m%d')
    dsi_studio_cmd = f'dsi_studio --action=atl --cmd=db --source="{database_dir}" --output="{database_dir}/data_base_{current_date}.fa.db.fib.gz" --template=1 --index_name=fa'
    
    try:
        subprocess.run(dsi_studio_cmd, shell=True, check=True)
        print(Fore.GREEN + "DSI Studio database creation completed successfully." + Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error during DSI Studio database creation: {e}" + Style.RESET_ALL)
    
    # Log the actions
    log_file = os.path.join(database_dir, f"database_creation_log_{current_date}.txt")
    with open(log_file, 'w') as f:
        f.write(f"Database created on {datetime.now()}\n")
        f.write(f"Project: {selected_project}\n")
        f.write(f"Cohorts: {', '.join(selected_cohorts)}\n")
        f.write("Subjects:\n")
        for cohort in selected_cohorts:
            f.write(f"  Cohort {cohort}:\n")
            for subject in selected_subjects_by_cohort[cohort]:
                f.write(f"    - {subject}\n")
    print(Fore.GREEN + f"Actions logged in {log_file}" + Style.RESET_ALL)

if __name__ == "__main__":
    input_dir = r"C:\preprocessing\mri_analysis"  # Base directory where projects are stored

    projects = list_projects(input_dir)  # List all projects in the input directory

    if projects:
        selected_project = select_project(projects)  # Ask user to select a project

        if selected_project:
            project_output_dir = os.path.join(input_dir, selected_project, 'DTI', 'preprocessing')

            # Load configuration file from the project's preprocessing directory
            config_file = os.path.join(project_output_dir, 'pipeline_config.json')
            config = load_configuration(config_file)

            if config:
                project_config = config['projects'].get(selected_project)
                if not project_config:
                    print(Fore.RED + f"No configuration found for project '{selected_project}' in the configuration file." + Style.RESET_ALL)
                else:
                    if not os.path.exists(project_output_dir):
                        print(Fore.RED + f"The preprocessing directory for project '{selected_project}' does not exist." + Style.RESET_ALL)
                    else:
                        cohorts = list(project_config.get('cohorts', {}).keys())
                        if cohorts:
                            selected_cohorts = select_cohorts_from_config(cohorts)
                            if selected_cohorts:
                                selected_subjects_by_cohort = {}
                                for cohort in selected_cohorts:
                                    subjects = project_config['cohorts'][cohort]
                                    selected_subjects = select_subjects_from_cohort(subjects, cohort)
                                    selected_subjects_by_cohort[cohort] = selected_subjects
                                # Create a new folder inside data_base with the selected cohort names
                                database_name = "_".join(selected_cohorts)
                                print(Fore.GREEN + f"Creating DSI database for cohorts: {selected_cohorts}" + Style.RESET_ALL)
                                create_dsi_database(project_output_dir, selected_project, selected_cohorts, selected_subjects_by_cohort, database_name)
                            else:
                                print(Fore.RED + "No cohorts selected, exiting." + Style.RESET_ALL)
                        else:
                            print(Fore.RED + "No cohorts found in the configuration for this project." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Failed to load configuration." + Style.RESET_ALL)
        else:
            print(Fore.RED + "No valid project selected, exiting." + Style.RESET_ALL)
    else:
        print(Fore.RED + "No projects found, please check the input directory." + Style.RESET_ALL)
