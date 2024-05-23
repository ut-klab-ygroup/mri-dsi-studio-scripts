# mri

# Setup
* [Ubuntu](./doc/ubuntu_setup.md)
* [Windows](./doc/windows_setup.md)






```
.
├── conditions.json                     # contains setup for the project such as name and condition for stat analysis
├── doc
│   ├── ubuntu_setup.md                 # documentation for ubuntu (under development and testing)
│   └── windows_setup.md                # documentation windows
├── main.py                             # main.py at the moment running automatic scrips based on extract_raw_data_bruker.py & reconstruction.py & db_creation.py
└── modalities
    ├── __init__.py
    ├── convert_3D_to_4D.py             # this file helps to conver 3D .nii files into 4D files.
    ├── data_base_creation.py           # STEP3: This is database creation logic 
    ├── extract_raw_data_bruker.py      # STEP1: This is first step of existing pipline where raw data from ParaVision360 extracted into preprocessing folder
    ├── reconstruction.py               # STEP2: This reconstruction step, takes .src file, topup/eddy, rotation to the template, b-table check (main preprocessing logic)
    ├── statistical_analysis.py         # STEP4: Correlation Tractography statistical analysis
    └── utilities
        └── utils.py                    # helper function for loading condition based on conditions.json file
```
