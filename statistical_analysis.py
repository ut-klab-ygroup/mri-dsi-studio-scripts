import os

from modalities.utilities.utils import list_projects, select_project
from modalities.statistical_analysis import run_statistical_analysis


if __name__ == "__main__":
    working_dir = "/home/sharapova/raw_analysis"

    projects = list_projects(working_dir)

    if projects:
        # processing data based on the project that was selected
        selected_project = select_project(projects)

        if selected_project:
            project_input_dir = os.path.join(working_dir, selected_project)

            if not any(os.listdir(project_input_dir)):
                print(f"The project directory '{selected_project}' is empty. Please add raw data from Paravision 360 to perform analysis.")
            else:
                pass