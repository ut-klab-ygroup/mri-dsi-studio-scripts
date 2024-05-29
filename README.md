![](https://mermaid.ink/svg/your-mermaid-code)

# Documentation for Correlation Tractography using DSI Studio (automatic pipline)

# Setup
* [Ubuntu](./doc/ubuntu_setup.md)
* [Windows](./doc/windows_setup.md)


Designed to process MRI raw data from ParaVision360, reconstruct files, create a DSI Studio database and perform statistical analysis

# Main Components

**preprocessing.py**

This is the main script to execute the processing workflow. Durring this script it will find respective DTI 2dseq file inside raw folder from ParaVision360 convert it to .src file reconstructing files, and creating a DSI Studio database.

```mermaid
graph TD;
    A[preprocessing.py] --> B[extract_raw_data_bruker.py]
    A --> C[reconstruction.py]
    A --> D[data_base_creation.py]

    B --> B1[STEP T1: 
    Finds 2dseq file in raw data and creates directory based on subject name]
    C --> C1[STEP T2 and STEP T3: 
    Masking, motion correction, rotation and fiber tracking file creation]
    D --> D1[STEP C1: 
    Agregate fiber tracking files after STEP T3 to create a database]
```


# Usage Instructions