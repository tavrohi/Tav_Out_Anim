import maya
import maya.cmds as cmds
import pymel.core as pm
from pymel.all import *
import os
import inspect
import __main__

ENTRYFOLDER = "Tav_Anim_Out"
MENUNAME = "Tav_Tools"

try:
    os.listdir(ENTRYFOLDER)
except WindowsError:
    src_file_path = inspect.getfile(lambda: None).replace("\\","/").replace("utilities.py","")
    ENTRYFOLDER = os.path.join(src_file_path, ENTRYFOLDER)

def scriptls(foldername):
    dirc = os.listdir(foldername)
    scripts = []
    for itm in dirc:
        extention = os.path.splitext(itm)
        if extention[1] == ".mel" or extention[1] == ".py" or not extention[0] == "__init__":
            scripts.append(itm)
            
    return scripts

def runcmds(path):
    extention = os.path.splitext(path)
    if(extention[1] == ".mel"):
        mel.eval("source \""+path+"\";")
    else:
        execfile(path)

def updateinimenu():
    maya.utils.executeDeferred(inimenu, standalone=True)

def inimenu(standalone=False):
    if(cmds.menu("menuaddvert", exists=1)):
        cmds.deleteUI("menuaddvert")

    gMainWindow = pm.melGlobals['gMainWindow']
    print gMainWindow
    mainfolder = ENTRYFOLDER
    directory_contents = os.listdir(mainfolder)
    menuitemsfol = []
    for item in directory_contents:
        if os.path.isdir(os.path.join(mainfolder, item)):
            if len(scriptls(os.path.join(mainfolder, item))) != 0:
                menuitemsfol.append(item)

    cmds.menu("menuaddvert", label=MENUNAME, tearOff=True, parent=gMainWindow)
    
    for itms in menuitemsfol:
        cmds.menuItem(("pnt"+itms), label=itms, subMenu=1, tearOff=True, parent="menuaddvert")
        getall = scriptls(os.path.join(mainfolder, itms))
        for itr in getall:
            cmd_r = os.path.join(mainfolder, itms, itr).replace("\\","/")
            if os.path.isdir(cmd_r):
                name = itr.split(".")[-1]
                if len(scriptls(cmd_r)) != 0:
                    menuitmname = (("pntsub"+itr).replace(" ", "_").replace(".","_"))
                    cmds.menuItem(menuitmname, label=name, subMenu=1, tearOff=True, parent=("pnt"+itms))
                    getsuball = scriptls(cmd_r)
                    for itrsub in getsuball:
                        cmd_sub_r = os.path.join(cmd_r, itrsub).replace("\\","/")
                        namesub = os.path.splitext(itrsub)
                        namesub = namesub[0].split(".")[-1]
                        cmds.menuItem(label=namesub, subMenu=0, tearOff=True, parent=menuitmname, c=Callback(runcmds, cmd_sub_r))
            else:
                name = os.path.splitext(itr)
                name = name[0].split(".")[-1]
                cmds.menuItem(label=name, subMenu=0, tearOff=True, parent=("pnt"+itms), c=Callback(runcmds, cmd_r))
    cmds.menuItem(divider=1, parent="menuaddvert")
    cmds.menuItem(label="Update", subMenu=0, parent="menuaddvert", c=Callback(updateinimenu))