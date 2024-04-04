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



# dsi_studio --action=cnt --source=4D_HF.fa.db.fib.gz --demo=participants_test.tsv --variable_list=0 --voi=0 --t_threshold=2 --length_threshold=16 --output=group_analysis   