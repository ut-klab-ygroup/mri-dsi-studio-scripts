"""
Created on 02/15/2024

@author: Andrii Gegliuk

"""

import os
import re
import subprocess
import argparse
from modalities.extract_raw_data_bruker import create_and_process_dti_dirs # STEP1: geting a data from bruker file
from modalities.reconstruction import process_src_files                    # STEP2: reconstruction (masking, motion correction, b-table check, TOPUP/EDDY)
from modalities.data_base_creation import create_dsi_database              # STEP3: creating database for connectometry analysis. Registering and normalizing all subjects to the common temlate.

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Process DTI directories and data.")
    
    parser.add_argument('-i', '--input_dir', required=True, type=str, help='The root directory to search for DTI data directories.') # input_dir
    parser.add_argument('-o', '--output_dir', required=True, type=str, help='The directory where processed data should be saved.') # output_dir
    
    args = parser.parse_args()
    
    # Step 1: Process raw DTI directories
    create_and_process_dti_dirs(args.input_dir, args.output_dir)

    # Step 2: Reconstruction process on processed src files
    process_src_files(args.output_dir)  # after create_and_process_dti_dirs .src.gz files should be part of output_dir

    # Step 3: DB creation
    create_dsi_database(args.output_dir)
    