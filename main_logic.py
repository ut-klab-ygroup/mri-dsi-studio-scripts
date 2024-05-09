import os
import csv

from modalities.extract_raw_data_bruker import create_and_process_dti_dirs
from modalities.utilities.utils import list_projects, select_project
from modalities.reconstruction import process_src_files
from modalities.data_base_creation import create_dsi_database
from modalities.statistical_analysis import run_statistical_analysis


if __name__ == "__main__":
    input_dir = "/home/sharapova/raw"
    output_dir = "/home/sharapova/raw_analysis"

    # function listing all directories within input folder (input folder expected to have only raw data under the specified project name)
    projects = list_projects(input_dir)

    if projects:
        # processing data based on the project that was selected
        selected_project = select_project(projects)

        if selected_project:
            project_input_dir = os.path.join(input_dir, selected_project)

            if not any(os.listdir(project_input_dir)):
                print(f"The project directory '{selected_project}' is empty. Please add raw data from Paravision 360 to perform analysis.")
            else:

                project_output_dir = os.path.join(output_dir, selected_project, 'DTI', 'preprocessing')
                os.makedirs(project_output_dir, exist_ok=True)
                print(f"Processing data for project {selected_project}...")
                
                # STEP T1: Data extraction and preparation
                create_and_process_dti_dirs(project_input_dir, project_output_dir)
                
                # STEP T2: Reconstruction process
                print("Starting the reconstruction of .src.gz files...")
                reconstruction_message = process_src_files(project_output_dir)
                print(reconstruction_message)

                # STEP C1: Creating database after 
                print("Starting the creation of the DSI Studio database...")
                create_dsi_database(project_output_dir)

                # # STEP C1: Creating database after 
                # print("Starting the creation of the DSI Studio database...")
                # run_statistical_analysis(project_output_dir)
                
                print("Processing completed. Please open database in DSI Studio to check if there is any artifacts or missregistration to remove some subjects!")
        else:
            print("No valid project selected, exiting.")
    else:
        print("No projects found, please check the input directory.")



"""initial"""
# if __name__ == "__main__":
#     input_dir = "/home/sharapova/raw"
#     output_dir = "/home/sharapova/raw_analysis"

#     projects = list_projects(input_dir)
#     if projects:
#         selected_project = select_project(projects)
#         if selected_project:
#             project_input_dir = os.path.join(input_dir, selected_project)
#             project_output_dir = os.path.join(output_dir, selected_project, 'DTI', 'preprocessing')
#             os.makedirs(project_output_dir, exist_ok=True) 
#             print(f"Processing data for project {selected_project}...")
#             create_and_process_dti_dirs(project_input_dir, project_output_dir)
#             print("Processing completed.")
#         else:
#             print("No project selected.")
#     else:
#         print("No projects found.")

"""modified"""
# if __name__ == "__main__":
#     input_dir = "/home/sharapova/raw"
#     output_dir = "/home/sharapova/raw_analysis"

#     # function listing all directories within input folder (input folder expected to have only raw data under the specified project name)
#     projects = list_projects(input_dir) 
#     if projects:
#         # processing data based on the project that was selected
#         selected_project = select_project(projects)
#         if selected_project:
#             project_input_dir = os.path.join(input_dir, selected_project)
#             project_output_dir = os.path.join(output_dir, selected_project, 'DTI', 'preprocessing')
#             os.makedirs(project_output_dir, exist_ok=True) 
#             print(f"Processing data for project {selected_project}...")

#             # STEP T1: Data extraction and preparation
#             create_and_process_dti_dirs(project_input_dir, project_output_dir)

#             # STEP T2: Reconstruction process
#             print("Starting the reconstruction of .src.gz files...")
#             reconstruction_message = process_src_files(project_output_dir)
#             print(reconstruction_message)

#             print("Processing completed.")
#         else:
#             print("No project selected.")
#     else:
#         print("No projects found.")