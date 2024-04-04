"""
Created on 02/01/2024

@author: Andrii Gegliuk

"""

import os
import re
from .utilities.utils import load_config
import subprocess


def extract_subject_name(subject_file_path):
    """
    Extracts the subject name from a given file.

        This function opens a file specified by `subject_file_path`, searches for a specific pattern
        indicating the subject study name within the file's content, and returns the name after
        performing certain transformations. The transformation includes replacing dashes ('-') with
        underscores ('_'), provided that the extracted name does not already contain underscores. If
        the pattern is not found, or the file cannot be read, the function returns None.

        Parameters:
            - subject_file_path (str): The path to the file from which the subject name is to be extracted.

        Returns:
            - str or None: The extracted and transformed subject name, or None if the name could not be
            extracted or the file could not be read.

        Exceptions:
            - Prints an error message if the file specified by `subject_file_path` cannot be opened or read.

        Note:
            - The function is designed to parse a specific format where the subject study name is enclosed
            in angle brackets ('<', '>') and prefixed with a specific pattern ('##$SUBJECT_study_name=').
            This format is required to get information inside the `subject` file from Bruker 11.7.
    """
    subject_name = None
    try:
        with open(subject_file_path, 'r') as file:
            content = file.read()
            match = re.search(r'##\$SUBJECT_study_name=\(\s*\d+\s*\)\s*<([^>]+)>', content, re.MULTILINE)
            if match:
                # subject_name = match.group(1).replace('-', '_')
                extracted_name = match.group(1)
                subject_name = extracted_name.replace('-', '_') if '_' not in extracted_name else extracted_name
    except Exception as e:
        print(f"Error reading {subject_file_path}: {e}")
    return subject_name


def find_dti_directories(root_dir):
    """
    Searches for directories containing DTI (Diffusion Tensor Imaging) data within a given root directory.

        This function recursively traverses all directories starting from `root_dir`. It looks for directories
        containing a file named 'method'. For each 'method' file found, the function reads its content to check
        for the presence of strings "DTI" or "DtiEpi", which indicate the directory contains DTI data. If such
        indications are found, the directory is considered a DTI directory, and its path is added to a list.

        Parameters:
            - root_dir (str): The path to the root directory from which the search for DTI directories begins.

        Returns:
            - list: A list of paths to directories that contain DTI data. If no DTI directories are found, an empty
            list is returned.

        Note:
            - The function assumes a specific file naming and content convention to identify DTI directories. This
            means it may not find DTI data formatted or organized differently.
            - This function does not validate the content beyond the presence of "DTI" or "DtiEpi" in the 'method'
            files. It is assumed that the presence of these strings accurately indicates DTI data.
    """
    dti_dirs = []
    for subdir, dirs, files in os.walk(root_dir):
        if 'method' in files:
            with open(os.path.join(subdir, 'method'), 'r') as f:
                content = f.read()
                if "DTI" in content or "DtiEpi" in content:
                    dti_dirs.append(subdir)
    return dti_dirs


def create_and_process_dti_dirs(root_dir, output_dir):
    """
    Identifies DTI directories, extracts subject names, and processes DTI data by executing external commands.

        This function finds directories containing DTI data under `root_dir`, extracts subject names from
        a sibling 'subject' file, and then processes each DTI directory. Processing involves creating a
        subject-specific preprocessing directory and executing a shell command with `subprocess.run` to
        handle the DTI data (e.g., creating a .src.gz file with dsi_studio).

        Parameters:
            - root_dir (str): The root directory to search for DTI data directories.

        Note:
            - Creates a 'preprocessing' directory under `output_dir` to store processed data.
            - Relies on 'method' and 'subject' files to identify and process DTI directories.
            - Prints the path of processed directories and any errors encountered during processing.
    """
    config = load_config(section='preprocessing')
    condition = config.get('condition', 'default_condition')
    preprocessing_dir = os.path.join(output_dir, condition, 'preprocessing')
    os.makedirs(preprocessing_dir, exist_ok=True)
    
    dti_dirs = find_dti_directories(root_dir)
    print(dti_dirs)
    
    for dti_dir in dti_dirs:
        subject_file_path = os.path.join(dti_dir, '..', 'subject')
        subject_name = extract_subject_name(subject_file_path)
        print(subject_name)
        
        if subject_name:
            subject_preprocessing_dir = os.path.join(preprocessing_dir, subject_name)
            os.makedirs(subject_preprocessing_dir, exist_ok=True)
            
            source_path = os.path.join(dti_dir, 'pdata', '1', '2dseq')
            output_path = os.path.join(subject_preprocessing_dir, f"{subject_name}.src.gz")

            command = f'dsi_studio --action=src --source="{source_path}" --output="{output_path}"'
            
            try:
                subprocess.run(command, shell=True, check=True)
                print(f"Processing completed for {subject_name}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to execute command for {subject_name}: {e}")
        else:
            print(f"No subject name extracted for DTI directory: {dti_dir}")


# root_directory = '/home/sharapova/mri_management_tool/testing_DSI' 
# create_and_process_dti_dirs(root_directory)