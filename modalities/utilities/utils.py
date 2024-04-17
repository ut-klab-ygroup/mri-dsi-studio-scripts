"""
Created on 04/28/2024

@author: Andrii Gegliuk

"""
import os
import json

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
        return [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
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
        print("Invalid selection.")
        return None



# dsi_studio --action=cnt --source=4D_HF.fa.db.fib.gz --demo=participants_test.tsv --variable_list=0 --voi=0 --t_threshold=2 --length_threshold=16 --output=group_analysis   