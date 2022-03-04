DESCRIPTION

This module writes export and reads import alembic caches for maya animations.

The module allows the user to save out alembic caches to a file destination from Autodesk Maya.
The object name and file destination may be given. 

The module also allows for the importing of alembic caches into Maya. The file path  must be given to import a cache.


SETUP

1.Set up the python path to find the code directory.
	In the Windows search bar, type "var" and select "edit environment variables for your accouunt"
	Under "User Variables"select "New"
	Set the "Variable Name" to PYTHONPATH
	Set the "Variable Value" to the directory destination (ex. C:\Users\Name\Desktop)
	Click OK, then OK again to close the window.

2.Load Autodesk Maya

3.Open the script editor in the bottom right corner

4. Hit the "+" to open a new PYTHON tab

5. Copy and Paste the following code as shown

from td_maya_tools.guis.cacher_gui import CacherGUI
cacher_gui = CacherGUI()
cacher_gui.init_gui() 

5. In the script editor, select Command > Execute
	