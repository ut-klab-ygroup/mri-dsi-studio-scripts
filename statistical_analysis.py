import os
import glob

from modalities.utilities.utils import list_projects, select_project, select_file
from modalities.statistical_analysis_pipline import create_statistical_analysis_structure, get_user_confirmation


if __name__ == "__main__":
    working_dir = "/home/sharapova/raw_analysis"

    projects = list_projects(working_dir)

    if projects:
        selected_project = select_project(projects) # processing data based on the project that was selected

        if selected_project:
            project_input_dir = os.path.join(working_dir, selected_project)

            if not any(os.listdir(project_input_dir)):
                print(f"The project directory '{selected_project}' is empty. Please add raw data from Paravision 360 to perform analysis.")
            else:
                data_base_dir = os.path.join(project_input_dir, "DTI", "data_base") # checking for presence of data_base
                demographics_file = os.path.join(project_input_dir, "DTI", "demographics.csv") # checking for presence of demographics.csv


                if not os.path.exists(data_base_dir):
                    print(f"The 'data_base' directory does not exist in '{project_input_dir}'.")
                elif not os.path.exists(demographics_file):
                    print(f"The 'demographics.csv' file does not exist in '{project_input_dir}'.")
                else:
                    source_files = glob.glob(os.path.join(data_base_dir, "*.fa.db.fib.gz"))            
                    if not source_files:
                        print(f"No source file found in '{data_base_dir}'.")
                    elif len(source_files) > 1:
                        source_file = select_file(source_files)
                        if not source_file:
                            exit(1) 
                    else:
                        source_file = source_files[0]

                    if source_file:
                        statistical_analysis_dir = create_statistical_analysis_structure(working_dir, selected_project)