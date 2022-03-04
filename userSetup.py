import maya
import sys
import inspect
import os
src_file_path = inspect.getfile(lambda: None).replace("\\","/").replace("userSetup.py","")
#py_subfiles = os.path.join(src_file_path, "tools", "Py_installs").replace("\\","/")
#sys.path.append(py_subfiles)

import utilities
from tools import anim_ui
#import tools.mod_ui
#import tools.rig_ui
#import tools.tex_ui
maya.utils.executeDeferred(utilities.inimenu, standalone=True)