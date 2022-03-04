#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    zdd130030

:synopsis:
    This module writes export and reads import alembic caches for maya animations.

:description:
    The module allows the user to save out alembic caches to a file destination from Maya.
    The object name and file destination may be given. The module also allows for the
    importing of alembic caches into Maya. The file path  must be given to import a cache.

:applications:
    Autodesk Maya

:see_also:
    N/A

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in
import tempfile
import os
# Third party
import maya.cmds as cmds
import maya.mel as mel
# Internal

# External

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#



class ImportCache(object):
    """
     This class imports alembic cache into Maya from a specified file location.

     Required arguments:
         read_file_path(str): The file destination fo the cache to be imported.
     """
    def __init__(self,read_file_path = None):
        self.read_file_path = read_file_path
    #runs the import function to bring cache in
    def import_cache(self):
        """
        Runs all the necessary commands and methods to import alembic cache to Maya.
        """
        #figures out file to import
        mel.eval('AbcImport -d -mode import "%s"' % self.read_file_path)



class ExportCache(object):
    """
     This class exports alembic cache from Maya to a specified file location.

     Required arguments:
         obj_name(str): The name of the object being cached.
     Optional arguments:
         file_path(str): The destination the cache will be saved to.
     """
    def __init__(self, min_num = None, max_num = None, obj_name = None, file_path = None):
        self.obj_name = obj_name
        self.file_path = file_path
        #frame range values
        self.min_num = min_num
        self.max_num = max_num
        #Decides what route to take based on if file_path is None
        """
        :param file_temp: Names the file that is being saved
        :type: string
        """
    def process_args(self):
        """
        Runs all the necessary commands and methods to export alembic cache from Maya.
        :param min_num: The first frame of the Time Slider
        :type: long

        :param max_num: The last frame of the Time Slider
        :type: long
        """
        # were frame ranges given
        if not self.min_num:
            self.min_num = long(cmds.playbackOptions(query=True, minTime=True))
        if not self.max_num:
            self.max_num = long(cmds.playbackOptions(query=True, maxTime=True))
        #was a file path given
        if not self.file_path:
            path = cmds.file(q=True,sn=True)
            directory = os.path.dirname(path)
            self.file_path = "%s/%s.abc" % (directory, self.obj_name)

    #runs the export function to save out a cache
    def export_cache(self):
        """
        Runs all the necessary commands and methods to export alembic cache from Maya.

        """
        #figures out  where to save .abc file
        mel.eval('AbcExport -j "-frameRange %s %s -uvWrite -worldSpace -writeVisibility -writeFaceSets -writeUVSets -root %s -root |%s -file %s"' %(self.min_num, self.max_num, self.obj_name, self.obj_name, self.file_path))