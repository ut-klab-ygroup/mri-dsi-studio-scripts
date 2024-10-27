import os
import json
from datetime import datetime


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


def update_configuration(config, project_name, subject_name, cohort): # TODO: docstring
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