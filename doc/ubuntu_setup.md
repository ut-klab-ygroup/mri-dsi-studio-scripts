###### NOTE: under development and testing

# DSI Studio Installation on Ubuntu 

## Prerequisites
<br>

**Operating System**: Ubuntu (version used during installation process should be specified, e.g., **20.04**).
Required Libraries and Tools: g++, git, Qt5, Boost, zlib, and additional development libraries.

### Prepare the Environment:

Ensure you're in the desired directory where you want to start the installation process.

`code`

### Check for DSI Studio Dependencies:

Before installing DSI Studio, check for any existing files or directories that you'll be working with.

`code`

### Install Required Packages:

Update your package lists to ensure you can install the latest versions of required packages.

```
sudo apt update
sudo apt upgrade
```

### Install G++ and GCC compilers. The commands also include setting up version 7 of G++, which may be required for compatibility with some of DSI Studio's components.

```
sudo apt install g++-7 gcc
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 10
sudo update-alternatives --config gcc
sudo update-alternatives --config g++
```

### Libraries and Development Tools:

Install necessary libraries including Qt5, Boost, and other dependencies required for compiling DSI Studio.

```
sudo apt install git libboost-all-dev zlib1g-dev libqt5charts5-dev libqt5opengl5-dev qt5-qmake qt5-default
```

### Cloning DSI Studio Repository

Create a directory for DSI Studio source code and clone the repository.

```
mkdir ~/dsistudio
cd ~/dsistudio
git clone -b master https://github.com/frankyeh/DSI-Studio.git src
```

Clone the TIPL (Template-based Image Processing Library) as required by DSI Studio. Ensure unzip is installed: `sudo apt-get install unzip` if not already installed.

```
wget https://github.com/frankyeh/TIPL/zipball/master -O TIPL.zip
unzip TIPL.zip
mv frankyeh-TIPL-* tipl
mv tipl src/
```

## Compilation

Prepare the build directory.

```
mkdir build
cd build
```

Generate makefiles using qmake.

```
/usr/lib/qt5/bin/qmake ../src
```

**Note**: Adjust the qmake path according to where it is installed on your system.

Compile the source code.

```
make
```

After compiling, you should have the DSI Studio executable within the build directory. You can now move this executable to a more permanent location or add it to your system's PATH for easier access.

## Running DSI Studio

Navigate to the directory containing the DSI Studio executable and run it:

```
./dsi_studio
```


https://www.nemotos.net/?p=1878


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

6 directories, 19 files