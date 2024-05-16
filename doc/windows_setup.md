# For Windows 10 and Windows 11:

To run DSI Studio from anywhere in Windows by just typing `dsi_studio`, you'll need to add the directory containing `dsi_studio.exe` to your system's PATH environment variable. The PATH variable helps Windows locate executables from the command line without needing to specify the full path.

## Open System Properties:

- Right-click on the Start menu and choose System.
- Click on Advanced system settings on the left sidebar to open the System Properties window.
- Go to the Advanced tab and click on Environment Variables.

## Edit the PATH Environment Variable:

- In the Environment Variables window, search for the Path variable under the "System variables" section (for all users) or the "User variables for [your username]" section (for the current user only). Select it and then click on Edit.
- In the Edit Environment Variable window, click on New and paste the path to the directory where dsi_studio.exe is located. Based on your provided path, this would be:

#### Path example to the dsi studio:

```
C:\Users\Downloads\dsi_studio\dsi_studio_win\dsi_studio.exe
```

- Click OK to close the editor, then OK again to close the Environment Variables window, and once more on the System Properties window to apply the changes.

## Restart Windows Terminal or Command Prompt:

For the changes to take effect, close and reopen any open Command Prompt or PowerShell windows. Now you should be able to launch DSI Studio by simply typing `dsi_studio` (assuming dsi_studio.exe is the executable's name) from any directory.