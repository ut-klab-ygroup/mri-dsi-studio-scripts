import os
import shutil
import glob
import subprocess

def run_statistical_analysis(output_dir):
    """
    Automatically finds the .fa.db.fib.gz file in the data_base directory,
    copies it to a new directory for statistical analysis, and runs the analysis.
    
    Parameters:
    - output_dir (str): The base output directory where DTI and data_base directories are located.
    """
    database_dir = os.path.join(output_dir, "DTI", "data_base")
    statistical_analysis_dir = os.path.join(output_dir, "DTI", "statistical_analysis") # creating new dir called statistical_analysis
    
    os.makedirs(statistical_analysis_dir, exist_ok=True)
    
    db_fib_file = next(glob.glob(os.path.join(database_dir, "*.fa.db.fib.gz")), None) # looking for .fa.db.fib.gz
    if db_fib_file is None:
        print("No .fa.db.fib.gz file found in the database directory.")
        return

    shutil.copy(db_fib_file, statistical_analysis_dir)
    print(f"Copied {db_fib_file} to {statistical_analysis_dir}")
    
    # preparing the DSI Studio command
    source_file = os.path.join(statistical_analysis_dir, os.path.basename(db_fib_file))
    participants_file = os.path.join(output_dir, "participants_test.tsv")
    output_dir = os.path.join(statistical_analysis_dir, "group_analysis")

    command = f'dsi_studio --action=cnt --source="{source_file}" --demo="{participants_file}" --variable_list=0 --voi=0 --t_threshold=2 --length_threshold=16 --output="{output_dir}"'
    
    try:
        subprocess.run(command, shell=True, check=True)
        print("Statistical analysis completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during statistical analysis: {e}")
