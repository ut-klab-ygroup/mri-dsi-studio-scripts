import os
import pandas as pd
import numpy as np
import shutil
import subprocess
from datetime import datetime
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS


def parse_demographics(file_path): # add condition for M and F
    """
    Parse the demographics file to generate comparison pairs based on unique conditions.
    
    Parameters:
        file_path (str): Path to the demographics file.
        
    Returns:
        list: A list of comparison pairs in the format 'Group1_vs_Group2' & 'Group2_vs_Group1'.
    """
    df = pd.read_csv(file_path)
    comparisons = []
    unique_groups = df['conditions'].unique()
    for i, group1 in enumerate(unique_groups):
        for group2 in unique_groups[i+1:]:
            comparisons.append(f"{group1}_vs_{group2}")
            comparisons.append(f"{group2}_vs_{group1}")
    return comparisons


def convert_html_to_pdf(comp_dir, group1, group2): # create new function because report does not look like we want
    """
    Convert the HTML report to a PDF file and save it in the 'reports' folder.

    Parameters:
        comp_dir (str): The directory containing the HTML report.
        group1 (str): The name of the first condition.
        group2 (str): The name of the second condition.
        t_threshold (float): The t-score threshold used in the analysis.
        length_threshold (int): The length threshold used in the analysis.
    """
    reports_dir = os.path.join(comp_dir, '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    html_file = os.path.join(comp_dir, 'group_analysis.report.html')
    if os.path.exists(html_file):
        current_date = datetime.now().strftime('%Y%m%d') # time is ok
        pdf_file_name = f"{current_date}_t2_vl_20_{group1}_vs_{group2}.pdf" # to fix this because treshold should be dinamic and vl as well.
        pdf_file_path = os.path.join(reports_dir, pdf_file_name) # path is working ok
        
        custom_css = """
            @page { size: A4; margin: 1in; }
            body { font-family: serif; font-size: 12pt; line-height: 1.5; }
            h1, h2, h3 { font-family: sans-serif; }
            h1 { font-size: 24pt; margin-bottom: 20px; }
            h2 { font-size: 18pt; margin-bottom: 15px; }
            h3 { font-size: 14pt; margin-bottom: 10px; }
            p { margin-bottom: 10px; }
            img { max-width: 100%; height: auto; margin-bottom: 10px; }
        """
        
        HTML(html_file).write_pdf(pdf_file_path, stylesheets=[CSS(string=custom_css)])


def update_html_report(comp_dir, group1, group2):
    """
    Dsi Studio generates statistical analysis report in HTML format. The problem is that it displays numerical conditions based on the .csv file. 
    Existing functiion updates the HTML report with the specified condition names from parse_demographics() function

    Parameters:
        comp_dir (str): The directory containing the HTML report.
        group1 (str): The name of the first condition.
        group2 (str): The name of the second condition.

    The function reads the HTML report, updates the condition names in the relevant sections, and writes the modified content back to the file.
    """
    
    html_file = os.path.join(comp_dir, 'group_analysis.report.html')
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Update the condition names in the relevant sections
        for tag in soup.find_all('h3'):
            if 'Tracks with higher FA in dsi_conditions 1' in tag.text:
                tag.string = f'Tracks with higher FA in {group1}'
            elif 'Tracks with higher FA in dsi_conditions 0' in tag.text:
                tag.string = f'Tracks with higher FA in {group2}'

        for tag in soup.find_all('p'):
            if 'The connectometry analysis found tracts showing higher FA in dsi_conditions 1' in tag.text:
                tag.string = tag.text.replace('dsi_conditions 1', group1)
            elif 'The connectometry analysis found tracts showing higher FA in dsi_conditions 0' in tag.text:
                tag.string = tag.text.replace('dsi_conditions 0', group2)

        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(str(soup))


def create_statistical_analysis_structure(base_dir, project_name, comparisons):
    """
    Create the directory structure for statistical analysis based on the given comparisons.

    Parameters:
        base_dir (str): The base directory where the project is located.
        project_name (str): The name of the project for which the analysis structure is being created.
        comparisons (list): A list of comparison strings, each representing a condition comparison (e.g., 'GH_vs_SI').

    Returns:
        str: The path to the created 'statistical_analysis' directory.

    The function creates a 'statistical_analysis' directory under the specified project's DTI directory.
    Within this directory, it creates subdirectories for each comparison in the comparisons list.
    """

    statistical_analysis_dir = os.path.join(base_dir, project_name, "DTI", "statistical_analysis")
    for comparison in comparisons:
        comparison_dir = os.path.join(statistical_analysis_dir, comparison)
        os.makedirs(comparison_dir, exist_ok=True)
    
    return statistical_analysis_dir

def copy_files_and_update_demographics(source_file, demographics_file, statistical_analysis_dir, comparisons):
    df = pd.read_csv(demographics_file)
    
    for comparison in comparisons:
        comp_dir = os.path.join(statistical_analysis_dir, comparison)
        shutil.copy(source_file, comp_dir)
        
        group1, group2 = comparison.split('_vs_')
        
        df['dsi_conditions'] = np.where(df['conditions'] == group1, 1, np.where(df['conditions'] == group2, 0, df['conditions']))
        comparison_demographics_file = os.path.join(comp_dir, "demographics.csv") # change a name based on the folder where it will be saved ddemographics_vs_.csv
        df.to_csv(comparison_demographics_file, index=False)

        # running analysis 
        comparison_source_file = os.path.join(comp_dir, os.path.basename(source_file))
        analysis_command = f"dsi_studio --action=cnt --source={comparison_source_file} --demo={comparison_demographics_file} --variable_list=2 --voi=2 --t_threshold=2 --fdr_threshold=0.05 --length_threshold=16 --output={os.path.join(comp_dir, 'group_analysis')} --no_tractogram=0"
        subprocess.run(analysis_command, shell=True, check=True)

        update_html_report(comp_dir, group1, group2) # updating pdf based on conditions inside the demographics

        convert_html_to_pdf(comp_dir, group1, group2) # convert to pdf and saving under reports folder


