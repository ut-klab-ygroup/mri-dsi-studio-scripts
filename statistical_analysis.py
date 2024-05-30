import os
import glob
import pandas as pd
import numpy as np
from colorama import init, Fore, Style

from modalities.utilities.utils import list_projects, select_project, select_file, get_user_confirmation
from modalities.statistical_analysis_pipline import create_statistical_analysis_structure, parse_demographics, copy_files_and_update_demographics
from modalities.utilities.parameters import *


if __name__ == "__main__":
    working_dir = ANALYSIS_DATA

    projects = list_projects(working_dir)

    if not projects:
        exit()

    selected_project = select_project(projects) # processing data based on the project that was selected

    if not selected_project:
        exit()
    project_input_dir = os.path.join(working_dir, selected_project)

    if not any(os.listdir(project_input_dir)):
        print(Fore.RED + Style.BRIGHT + f"The project directory '{selected_project}' is empty. Please add raw data from Paravision 360 to perform analysis." + Style.RESET_ALL)
        exit()
        
    data_base_dir = os.path.join(project_input_dir, "DTI", "data_base") # checking for presence of data_base
    demographics_file = os.path.join(project_input_dir, "DTI", "demographics.csv") # checking for presence of demographics.csv

    if not os.path.exists(data_base_dir):
        print(Fore.RED + Style.BRIGHT +f"The 'data_base' directory does not exist in '{project_input_dir}'." + Style.RESET_ALL)
    elif not os.path.exists(demographics_file):
        print(Fore.RED + Style.BRIGHT + f"The 'demographics.csv' file does not exist in '{project_input_dir}'." + Style.RESET_ALL)
    else:
        user_confirmation = get_user_confirmation() # this function asking user if he excluded some samples in data_base file did they ammend demographics.csv 
        if user_confirmation == "no":
                print(Fore.RED + Style.BRIGHT + "Please amend the demographics.csv file to reflect the changes and try again." + Style.RESET_ALL) # if the answer is no script stops execution
        else:
            source_files = glob.glob(os.path.join(data_base_dir, "*.fa.db.fib.gz")) # if the answer is yes scripts checks how many data_base files are there and give options to user to choose            
            if not source_files:
                print( Fore.RED + Style.BRIGHT + f"No source file found in '{data_base_dir}'." + Style.RESET_ALL)
            elif len(source_files) > 1:
                source_file = select_file(source_files)
                if not source_file:
                    exit(1) 
            else:
                source_file = source_files[0] # but if there is only one file there is no option to choose and script will run 

            if source_file:
                comparisons = parse_demographics(demographics_file) # demographics creates folders based on 'conditons' column
                statistical_analysis_dir = create_statistical_analysis_structure(working_dir, selected_project, comparisons) # creates data structure for the statistical analysis

                copy_files_and_update_demographics(source_file, demographics_file, statistical_analysis_dir, comparisons) # running statistical analysis script based on each condition

                print(Fore.GREEN + Style.BRIGHT + f"Completed! Results are stored in '{statistical_analysis_dir}'" + Style.RESET_ALL)