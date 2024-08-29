###### NOTE: under development and testing

# DSI Studio Installation on Ubuntu 

### Step 1: Install DSI_Studio:

Please install compiled version `dsi_studio_ubuntu2204.zip` form DSI Studio web site

[Download](https://dsi-studio.labsolver.org/download.html)

### Step 2: Install Required Dependencies:

Before downloading and setting up DSI Studio, you need to ensure that all the required dependencies are installed on your system.

```
sudo apt-get update
```

Then please run following:

```
sudo apt update && sudo apt upgrade -y && \
sudo apt install -y \
  unzip \
  curl \
  cmake \
  ninja-build \
  git \
  zlib1g-dev \
  libglu1-mesa-dev \
  qt6-base-dev \
  libqt6charts6-dev \
  libqt6opengl6-dev \
  qt6-image-formats-plugins
```


### Step 3: Download and Extract DSI Studio:

Choose a directory where you want to store DSI Studio. This could be your home directory or another directory where you keep your applications.

```
mkdir dsistudio
```

**Download the DSI Studio zip file:**

Ensure you have the DSI Studio zip file (dsi_studio_ubuntu2204.zip) in your chosen directory `dsistudio`.

**Unzip the DSI Studio package:**

```
unzip dsi_studio_ubuntu2204.zip
```

### Step 4: Move to the DSI Studio Directory and Run:

Navigate to the extracted DSI Studio directory:

```
cd dsi-studio/
```

Run the DSI Studio:

```
./dsi_studio
```

If you have an issue with permissions, please run following command to give the necessary permissions:

```
chmod +x dsi_studio
```

After setting the executable permissions, you can run the command again:

```
./dsi_studio
```


If following screen appeared you have successfully installed DSI Studio. 

![alt text](image.png)

If you encounter the error while loading shared libraries: libQt6Charts.so.6: cannot open shared object file: No such file or directory, ensure all dependencies from Step 2 are installed.

### Step 5: Make DSI Studio Globally Accessible:

To run DSI Studio from any directory, add the DSI Studio directory to your PATH environment variable.

Depending on the shell you are using, open the appropriate configuration file:

- For `bash`:

```
nano ~/.bashrc
```

- For `zsh`:

```
nano ~/.zshrc
```

Add the following line to the PATH in the end of the file:

```
export PATH=$PATH:/path/to/your/directory/dsi-studio
```

Replace `/path/to/your/directory` with the actual path where you extracted DSI Studio.

Save and close the file:
- To save the file in Nano, press `Ctrl + O`, then Enter.
- To exit Nano, press `Ctrl + X`

Apply the changes in the terminal:


- For `bash`:

```
source ~/.bashrc
```

- For `zsh`:

```
source ~/.zshrc
```

### Step 6: Verify the Changes:

Open a new terminal window or tab and type:

```
dsi_studio
```

DSI Studio should now run from any location if not change the path again. 



