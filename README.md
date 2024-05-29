# Documentation for Correlation Tractography using DSI Studio (automatic pipline)

# Setup
* [Ubuntu](./doc/ubuntu_setup.md)
* [Windows](./doc/windows_setup.md)


### Designed to process MRI raw data from ParaVision360, reconstruct files, create a DSI Studio database and perform statistical analysis

# Main Components

**preprocessing.py**

This is the main script to execute the processing workflow. It includes importing necessary modules, setting input and output directories, listing available projects, selecting a project, processing data, reconstructing files, and creating a DSI Studio database.

```
graph TD;
    A[preprocessing.py] --> B[extract_raw_data_bruker.py]
    A --> C[reconstruction.py]
    A --> D[data_base_creation.py]
    A --> E[utils.py]

    B --> B1[create_and_process_dti_dirs]
    C --> C1[process_src_files]
    D --> D1[create_dsi_database]
    E --> E1[list_projects]
    E --> E2[select_project]
```


# Usage Instructions