![](https://mermaid.ink/svg/your-mermaid-code)
# Documentation for Correlation Tractography using DSI Studio (automatic pipline)

# Download DSI Studio

* [Download](https://dsi-studio.labsolver.org/download.html)

# Setup
* [Ubuntu](./doc/ubuntu_setup.md)
* [Windows](./doc/windows_setup.md)

# Main Components

## Preprocessing 
**preprocessing.py**

This is the main script to execute the preprocessing workflow. During its execution, the script performs several steps to process DTI (Diffusion Tensor Imaging) data obtained from ParaVision360. The script's functionality includes finding and converting Bruker `2dseq` files into `.src` files, reconstructing the data, and creating a DSI Studio database for further statistical analysis.

```mermaid
graph TD;
    A[preprocessing.py] --> B[extract_raw_data_bruker.py]
    A --> C[reconstruction.py]
    A --> D[data_base_creation.py]

    B --> B1[STEP T1: 
    Finds and convert Bruker 2dseq files 
    to SRC Files and creates directory 
    based on subject name]
    C --> C1[STEP T2 and STEP T3: 
    - Remove background signals or crop image volume;
    - check Check b-table; 
    motion correction, TOPUP/EDDY; 
    - correct image orientation 
    - fiber tracking file FIB creation]
    D --> D1[STEP C1: 
    Aggregates multiple FIB files into a 
    common template space that 
    allows group-level analysis]
```


## Statistical Analysis

**statistical_analysis.py**

This script perform the statistical analysis. It checks for the presence of required directories and files, processes the selected project, and organizes the data for statistical analysis based on demographic information.

```mermaid
graph TD;
    A[statistical_analysis.py] --> B[statistical_analysis_pipline.py]

    B --> B1[create_statistical_analysis_structure]
    B1 --> B1_info[Creates the directory 
    structure for the statistical analysis 
    based on the given comparisons.]

    B --> B2[parse_demographics]
    B2 --> B2_info[Parses the demographics.csv 
    file to generate comparison pairs 
    based on unique conditions.]

    B --> B3[copy_files_and_update_demographics]
    B3 --> B3_info[Copies the source files into 
    the appropriate directories, 
    updates demographics information, 
    runs analysis, and updates the report.]
```

# Usage Instructions