# Install DSI studio
## Download and install

[DSI Studio Download Link](https://dsi-studio.labsolver.org/download.html)
## Add PATH
* Add the directory containing `dsi_studio.exe` to your system's PATH environment variable.
* To run DSI Studio from anywhere in Windows by just typing `dsi_studio`, you'll need to do this. The PATH variable helps Windows locate executables from the command line without needing to specify the full path.
### Detailed instruction for adding PATH
#### Open System Properties:

- Right-click on the Start menu and choose System.
- Click on Advanced system settings on the left sidebar to open the System Properties window.
- Go to the Advanced tab and click on Environment Variables.

#### Edit the PATH Environment Variable:

- In the Environment Variables window, search for the Path variable under the "System variables" section (for all users) or the "User variables for [your username]" section (for the current user only). Select it and then click on Edit.
- In the Edit Environment Variable window, click on New and paste the path to the directory where dsi_studio.exe is located. Based on your provided path, this would be:

#### Path example to the dsi studio:

```
C:\Users\Downloads\dsi_studio\dsi_studio_win\dsi_studio.exe
```

- Click OK to close the editor, then OK again to close the Environment Variables window, and once more on the System Properties window to apply the changes.

#### Restart Windows Terminal or Command Prompt:

For the changes to take effect, close and reopen any open Command Prompt or PowerShell windows. Now you should be able to launch DSI Studio by simply typing `dsi_studio` (assuming dsi_studio.exe is the executable's name) from any directory.

# Clone the Repository:

Open your terminal or command prompt and navigate to the directory where you want to clone the project, then run:


For **SHH** connection:

```
git clone git@github.com:ut-klab-ygroup/dsi-studio-scripts.git
```

For **HTTPS** connection:

```
git clone https://github.com/ut-klab-ygroup/dsi-studio-scripts.git
```

After cloning the repository, navigate into the project directory in order to create Virtual Environment:

```
cd dsi-studio-scripts
```

# Creating a Virtual Environment

**Create a Virtual Environment:**

Open your terminal or command prompt and navigate to your project directory, then run:

```
python -m venv myenv
```

**Activate the Virtual Environment:**

To activate the virtual environment, run the following command:

```
.\myenv\Scripts\activate
```

**Install Required Packages:**

While the virtual environment is activated, install the necessary packages by running:

```
pip install python-dotenv colorama pandas numpy
```

This installs the python-dotenv, colorama, pandas, and numpy packages that is used durring the pipline. 

# Using Environment Variables

### Create a `.env` File

Create a `.env` file in your project directory and add your environment variables. For example:

```
RAWDATA = path\to\the\folder\with\raw_data
ANALYSIS_DATA = path\to\the\folder\with\analysis
```

So now you are ready to process analysis. Please refer to the Main Components section [here](../README.md) for further instruction.