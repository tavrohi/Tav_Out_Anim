#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    zdd130030

:synopsis:
    This module runs the necessary commands to allow a GUI to be created in Maya. It also
    checks to make sure a viewport is selected

:description:
    The module allows a gui interface to be created in Maya

:applications:
    Autodesk Maya

:see_also:
    N/A

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in

# Third party
import maya.cmds as cmds
# Internal

# External
try:
    from PyQt4 import QtCore, QtWidgets
except ImportError:
    from PySide2 import QtCore, QtWidgets

from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#
"""
This function allows the GUI to be created
"""
def get_maya_window():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow    = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)
    return mayaMainWindow
"""
This function returns the type of viewport selected to later be checked if valid
"""
def get_model_panel():
    selected_panel = cmds.getPanel( withFocus=True )
    panel_check = '%s' % cmds.getPanel(typeOf=selected_panel)
    return panel_check

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#



