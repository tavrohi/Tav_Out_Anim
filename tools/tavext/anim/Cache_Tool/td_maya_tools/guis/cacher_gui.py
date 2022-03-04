#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    zdd130030

:synopsis:
    This module writes export and reads import alembic caches for maya animations from a GUI

:description:
    The module allows the user to save out alembic caches to a file destination from Maya. The object name and file
    destination may be given. The module also allows for the importing of alembic caches into Maya. The file path  must
    be given to import a cache. All of these functions are done through user input on a GUI.

:applications:
    Autodesk Maya

:see_also:
    N/A

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in
import tempfile
# Third party
import maya.cmds as cmds
import maya.mel as mel
import os
# Internal

# External
import tools.tavext.anim.Cache_Tool.td_maya_tools.cacher as cacher
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
#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

# set up GUI interface
class CacherGUI(QtWidgets.QDialog):
    """
     This class is the GUI for the maya_tools.cacher.py file
    """
    def __init__(self):
        QtWidgets.QDialog.__init__(self, parent=get_maya_window())
        self.le_frame_start = None
        self.le_frame_end = None
        self.file_name = None
        self.le_file_name = None
        self.text_write_directory = None
        self.dir_name = None

    # build gui layout
    def init_gui(self):
        """
        Sets up all objects present in the GUI
        """
        # create main layout box
        main_hb = QtWidgets.QHBoxLayout(self)

        # set up buttons
        btn_write_directory = QtWidgets.QPushButton('Directory', self)
        btn_read_directory = QtWidgets.QPushButton('Directory')
        btn_read_file = QtWidgets.QPushButton('File', self)
        btn_write_cache = QtWidgets.QPushButton('Write Cache', self)
        btn_cancel = QtWidgets.QPushButton('Cancel', self)

        # set up line edits

        self.le_frame_start = QtWidgets.QLineEdit()
        self.le_frame_end = QtWidgets.QLineEdit()
        self.le_file_name = QtWidgets.QLineEdit()

        # set up text
        text_write_title = QtWidgets.QLabel('Write Cache')
        text_read_title = QtWidgets.QLabel('Read Cache')
        text_frange = QtWidgets.QLabel('Frame Range')
        text_frange_to = QtWidgets.QLabel('to')
        text_read_or = QtWidgets.QLabel('or')
        text_fileName = QtWidgets.QLabel('ABC File Name*')
        text_blank = QtWidgets.QLabel('')
        self.text_write_directory = QtWidgets.QLabel('')

        # button logic
        btn_write_cache.clicked.connect(self.validate_export)
        btn_write_directory.clicked.connect(self.select_dir)
        btn_read_directory.clicked.connect(self.select_dir_read)
        btn_read_file.clicked.connect(self.select_file_read)
        btn_cancel.clicked.connect(self.close)

        # set up gui layout
        # write title
        row_write_title = QtWidgets.QHBoxLayout()
        row_write_title.addWidget(text_write_title)

        # read title
        row_read_title = QtWidgets.QHBoxLayout()
        row_read_title.addWidget(text_read_title)

        # frame range
        row_frange = QtWidgets.QHBoxLayout()
        row_frange.addWidget(text_frange)
        row_frange.addWidget(self.le_frame_start)
        row_frange.addWidget(text_frange_to)
        row_frange.addWidget(self.le_frame_end)
        
        #File Name
        row_file_name = QtWidgets.QHBoxLayout()
        row_file_name.addWidget(text_fileName)
        row_file_name.addWidget(self.le_file_name)
        
        # write directory
        row_write_directory = QtWidgets.QHBoxLayout()
        row_write_directory.addWidget(btn_write_directory)
        row_write_directory.addWidget(self.text_write_directory)

        # read directory
        row_read_directory = QtWidgets.QHBoxLayout()
        row_read_directory.addWidget(btn_read_directory)

        # read file
        row_read_file = QtWidgets.QHBoxLayout()
        row_read_file.addWidget(btn_read_file)

        # write accept
        row_waccept = QtWidgets.QHBoxLayout()
        row_waccept.addWidget(btn_write_cache)

        # read or line
        row_or = QtWidgets.QHBoxLayout()
        row_or.addWidget(text_blank)
        row_or.addWidget(text_read_or)
        row_or.addWidget(text_blank)

        # write column
        column_write = QtWidgets.QVBoxLayout()
        column_write.addLayout(row_write_title)
        column_write.addLayout(row_frange)
        column_write.addLayout(row_file_name)
        column_write.addLayout(row_write_directory)
        column_write.addLayout(row_waccept)
        column_write.addWidget(text_blank)
        
        # read column
        column_read = QtWidgets.QVBoxLayout()
        column_read.addLayout(row_read_title)
        column_read.addLayout(row_read_directory)
        column_read.addLayout(row_or)
        column_read.addLayout(row_read_file)
        column_read.addWidget(btn_cancel)

        # place boxes onto main
        main_hb.addLayout(column_write)
        main_hb.addLayout(column_read)

        # create area and window title
        column_write.addStretch(1)
        column_read.addStretch(1)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Maya Cacher')
        self.show()
        
    # check if frame range was input
    def get_frange(self):
        """
        Runs commands to retrieve frame values
        """
        self.ex_min = self.le_frame_start.text()
        self.ex_max = self.le_frame_end.text()
        """
        #if no start input
        if not self.le_frame_start.text():
            ex_min= long(cmds.playbackOptions(minTime=True, query=True))

        #if no end input
        if not self.le_frame_end.text():
            ex_max = long(cmds.playbackOptions(maxTime=True, query=True))
        """
        # selects the directory to write

    def select_dir(self):
        """
        Runs commands and methods to select export directory
        """
        # opens the file dialog
        write_directory_name = cmds.fileDialog2(dialogStyle=2, caption='Load Directory',
        fileMode=2, okCaption='Select')
        self.dir_name = ''.join(str(letter) for letter in write_directory_name)
        # sets a value to be set into the line edit
        self.file_location = self.dir_name
        self.update_export()

    # selects the directory to read
    def select_dir_read(self):
        """
        Runs commands and methods to select import directory
        """
        # opens the file dialog
        read_directory_name = cmds.fileDialog2(dialogStyle=2, caption='Load Directory',
        fileMode=3, okCaption='Select')
        read_dir_name = ''.join(str(letter) for letter in read_directory_name)

        # runs the loading cache for each file in directory
        file_list = cmds.getFileList(folder=read_dir_name, filespec='*.abc')
        for name in file_list:
            file_name = ''.join(str(letter) for letter in name)
            # sets a value for cacher
            self.read_file = read_dir_name + '/' + file_name

            # runs the import operation
            self.read_cache()
        self.display_import_result()
        # selects the file to read

    def select_file_read(self):
        """
        Runs commands and methods to open a dialog to import a file
        """
        # opens the file dialog
        read_file_name = cmds.fileDialog(directoryMask='*.abc')
        # sets a value for cacher
        self.read_file = read_file_name

        # runs the loading cache
        self.read_cache()
        
    def file_Nam(self):
        """ 
        Reads file Name and save it as this file Name
        """
        self.name = self.le_file_name.text()
        

    # vailidates export
    def validate_export(self):
        """
        Runs commands to make sure something is selected before caching
        """
        valid = cmds.ls(selection=True)
        if not valid:
            self.display_warning()
        else:
            self.write_cache()

    # displays warning box
    def display_warning(self):
        """
         Runs commands to display if nothing is selected
        """
        reply = QtWidgets.QMessageBox.warning(self, 'Error', "No Object Selected")

        # updates text representing write directory

    def update_export(self):
        self.text_write_directory.setText(self.file_location)

    # export result
    def display_export_result(self):
        """
        Runs all the necessary commands and methods to display export results
        """
        reply = QtWidgets.QMessageBox.information(self, 'Export Result',
        "Files saved to Directory: %s" % self.file_location)

    # import result
    def display_import_result(self):
        """
        Runs all the necessary commands and methods to display import results
        """
        reply = QtWidgets.QMessageBox.information(self, 'Import Result',
        "Imported Cache successfully")

    # writes cache useing cacher.py
    def write_cache(self):
        """
         Runs all the necessary commands and methods to export alembic cache from Maya.
        """
        self.get_frange()
        self.file_Nam()
        selected_obj = cmds.ls(selection=True)
        
        # converts list to strings and checks if there is a directory
        for geo in selected_obj:
            name = ' -root '.join(str(geo) for geo in selected_obj)
            if self.dir_name:
                w_file_name = self.dir_name + '/' + self.name + '.abc'
            else:
                path = cmds.file(q=True,sn=True)
                directory = os.path.dirname(path)
                w_file_name = directory + '/' + self.name + '.abc'
        ex_cacher = cacher.ExportCache(self.ex_min, self.ex_max, name, w_file_name)
        ex_cacher.process_args()
        ex_cacher.export_cache()
        self.display_export_result()

    # reads cache using cacher.py
    def read_cache(self):
        """
        Runs all the necessary commands and methods to import alembic cache to Maya.
        """
        imp_cacher = cacher.ImportCache(self.read_file)
        imp_cacher.import_cache()
        self.display_import_result()

