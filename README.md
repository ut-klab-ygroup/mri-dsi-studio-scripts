![](https://mermaid.ink/svg/your-mermaid-code)

# Documentation for Correlation Tractography using DSI Studio (automatic pipline)

---

# Setup
* [Ubuntu](./doc/ubuntu_setup.md)
* [Windows](./doc/windows_setup.md)

---

# Download DSI Studio

* [Download](https://dsi-studio.labsolver.org/download.html)

---

# Main Components

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


# Usage Instructions