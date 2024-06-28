###### NOTE: under development and testing

# DSI Studio Installation on Ubuntu 

## Prerequisites
<br>

**Operating System**: Ubuntu (version used during installation process should be specified, e.g., **20.04**).
Required Libraries and Tools: g++, git, Qt5, Boost, zlib, and additional development libraries.

### Step 1: Install Required Dependencies

Before downloading and setting up DSI Studio, you need to ensure that all the required dependencies are installed on your system.

```
sudo apt-get update
sudo apt-get install -y libxcb-xinerama0 unzip curl cmake ninja-build git zlib1g-dev libglu1-mesa-dev qt6-base-dev libqt6charts6-dev libqt6opengl6-dev qt6-image-formats-plugins
```

### Step 2: Download and Extract DSI Studio

Choose a directory where you want to store DSI Studio. This could be your home directory or another directory where you keep your applications.

```
mkdir dsistudio
```

**Download the DSI Studio zip file:**

Ensure you have the DSI Studio zip file (dsi_studio_ubuntu2204.zip) in your chosen directory.

**Unzip the DSI Studio package:**

```
unzip dsi_studio_ubuntu2204.zip
```

### Step 3: Move to the DSI Studio Directory

Navigate to the extracted DSI Studio directory:

```
cd dsi-studio/
```



https://www.nemotos.net/?p=1878
