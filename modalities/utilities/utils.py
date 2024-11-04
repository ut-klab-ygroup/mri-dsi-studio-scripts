"""
Created on 04/28/2024

@author: Andrii Gegliuk

"""
import os
import json
import pandas as pd

def load_config(config_path='conditions.json', section=None):
    """
        Loads configuration from a JSON file and optionally retrieves a specific section.

        Parameters:
        - config_path (str): Path to the configuration JSON file. Defaults to 'conditions.json'.
        - section (str, optional): Specific section of the configuration to retrieve. If None or
        not found, the entire configuration is returned.

        Returns:
        - dict: The entire configuration dictionary or a specific section of it.
    """
    # stucturing a path, since I suppose config will be part of main dir
    dir_path = os.path.dirname(os.path.realpath(__file__))
    absolute_config_path = os.path.join(dir_path, '..', '..', config_path)

    with open(absolute_config_path, 'r') as file:
        config = json.load(file)
    if section and section in config:
        return config[section]
    return config


def list_projects(input_dir):
    """
    Lists all subdirectories within a specified directory.
    
        Args:
            - input_dir (str): The directory from which to list subdirectories.

        Returns:
            - list: A list of subdirectory names, or an empty list if an error occurs.
    """
    try:
        dir_list=[d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
        return list(filter(lambda x:not os.path.basename(x).startswith("_"),dir_list))
    except OSError as e:
        print(f"Error accessing directory {input_dir}: {e}")
        return []

def select_project(projects):
    """
    Prompts the user to select a project from a list of projects.

        Args:
            - projects (list of str): A list of project names to choose from.

        Returns:
            - str: The selected project name, or None if the selection is invalid.
    """
    for idx, project in enumerate(projects):
        print(f"{idx + 1}: {project}")
    choice = int(input("Select a project number: ")) - 1
    if 0 <= choice < len(projects):
        return projects[choice]
    else:
        print("Invalid project. There is no project with this index.")
        return None
    


def select_file(files):
    """
    Prompt the user to select a file from a list of multiple files.

        Parameters:
            files (list): A list of file paths.

        Returns:
            str: The selected file path if a valid selection is made, otherwise None.
    """

    print("Multiple files found:")
    for i, file in enumerate(files, start=1):
        print(f"{i}: {file}")
    
    choice = input("Please select a file by entering the corresponding number: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(files):
            return files[index]
        else:
            print("Invalid selection. Exiting.")
            return None
    except ValueError:
        print("Invalid input. Exiting.")
        return None
    

def get_user_confirmation(): # This function needs to be updated
    """
    Prompt the user to confirm if the original demographics.csv file was modified after removing subjects.

        Returns:
            str: 'yes' if the user confirms the modification, 'no' otherwise.
    """

    while True:
        answer = input("Did you modify the original demographics.csv? (yes/no): ").strip().lower()
        if answer in ["yes", "no"]:
            return answer
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")



def load_subjects_from_excel(excel_file): # TODO: delete this function since it is integrated in main pipline by few lines of code
    """
    Load subjects from the Excel file, filter by the 'Include' column.

    Parameters:
        excel_file (str): Path to the subjects Excel file.

    Returns:
        DataFrame: Filtered DataFrame containing subjects marked as 'True' for inclusion.
    """
    df = pd.read_excel(excel_file)
    df_filtered = df[df['Include'] == True]  # Filter based on 'Include' column
    return df_filtered


def group_by_condition(df):
    """
    Group subjects by their Condition (Single, Group).

    Parameters:
        df (DataFrame): Filtered DataFrame of subjects.

    Returns:
        dict: Dictionary where keys are conditions (e.g., 'Single', 'Group') and values are lists of subject IDs.
    """
    grouped = df.groupby('Condition')['Subject ID'].apply(list).to_dict()
    return grouped



def get_subject_name(subject_id):
    """
    Extract the subject name from the subject ID. # This functions needs to be tested on more subjest (keeping for now)
    """
    # Split on '_1_' and take the first part
    subject_name_part = subject_id.split('_1_')[0] # spliting the subject_name_part into parts
    
    parts = subject_name_part.split('_') # Remove the first two parts if they are dates/times
    
    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
        parts = parts[2:]
    
    for i, part in enumerate(parts): # finding the first date in the remaining parts
        if len(part) == 8 and part.isdigit():
            date_index = i
            break
    else:
        date_index = 0
    
    subject_name_parts = parts[date_index:] # Subject name is from date_index to the end
    subject_name = '_'.join(subject_name_parts)
    return subject_name


# dsi_studio --action=cnt --source=4D_HF.fa.db.fib.gz --demo=participants_test.tsv --variable_list=0 --voi=0 --t_threshold=2 --length_threshold=16 --output=group_analysis