import maya.cmds as cmds
import tools.showxml as xm
import os
import maya.mel as mel
import pymel.core as pm
import re 

def playbblastmain(status):
    pfcus = cmds.getPanel(withFocus=1)
    try:
        cfcus = cmds.modelPanel(pfcus, q=1, camera=1)
    except:
        cmds.confirmDialog( title='Panel not Right',  icon="critical", message="Kindly select correct Viewport Panel then click on Playblast", button=['Okay'], defaultButton='Okay', cancelButton='Okay')
    cfcus = cmds.modelPanel(pfcus, q=1, camera=1)
    if re.search("Shape", cfcus):
        cshp = cfcus
    else :
        cshp = cmds.listRelatives(cfcus, s=1)[0]
    ogmskcolor = cmds.getAttr(cfcus+".displayGateMaskColor")
    ogmskopo = cmds.getAttr(cshp+".displayGateMaskOpacity")
    oovscn = cmds.getAttr(cshp+".overscan")
    cmds.setAttr(cshp+".displayGateMaskOpacity", 1)
    cmds.setAttr(cfcus+".displayResolution", 1)
    cmds.setAttr(cfcus+".displayGateMask", 1)
    cmds.setAttr(cshp+".overscan", 1.2)
    if(status == 1):
        cmds.setAttr(cfcus+".displayGateMaskColor", 0.023296, 0.182, 0.023296, type='double3')
    else:
        cmds.setAttr(cfcus+".displayGateMaskColor", 0.157, 0.0, 0.0, type='double3')
        
    rem()
    check()
    dopb()
    rem()
    cmds.setAttr(cshp+".overscan", oovscn)
    cmds.setAttr(cfcus+".displayGateMaskColor", ogmskcolor[0][0], ogmskcolor[0][1], ogmskcolor[0][2], type='double3')
    cmds.setAttr(cshp+".displayGateMaskOpacity", ogmskopo)
    cmds.setAttr(cfcus+".displayResolution", 0)
    cmds.setAttr(cfcus+".displayGateMask", 0)
    
def dopb():
    file_name = pm.sceneName()

    current_pane = cmds.getPanel(withFocus=True)
    cmds.modelEditor(current_pane, edit=True, alo=0)
    cmds.modelEditor(current_pane, edit=True, ns=0, pm=1, pl=1, da='smoothShaded', dtx=True, strokes=True, imagePlane=True, pluginObjects=('gpuCacheDisplayFilter', 1))
    pat = file_name.replace('.ma', '.mov').replace('.mb', '.mov')
    a_play_back_slider_python = mel.eval('$tmpVar=$gPlayBackSlider')
    sound_node = cmds.timeControl(a_play_back_slider_python, q=True, s=True)
    min = int(cmds.playbackOptions(q=1, min=1))
    max = int(cmds.playbackOptions(q=1, max=1))
    try:
        cmds.playblast(format='qt', filename=pat, forceOverwrite=True, clearCache=True, viewer=True,
                        showOrnaments=True, percent=100, compression='MPEG-4 Video', sound=sound_node, useTraxSounds=True, offScreen=True,
                        widthHeight=[1920, 1080], st=min, et=max)
    except RuntimeError:
        cmds.confirmDialog( title='QT unavailable',  icon="critical", message="QT not found. Kindly install QuickTime and restart Maya", button=['Okay'], defaultButton='Okay', cancelButton='Okay')

    cmds.modelEditor(current_pane, edit=True, ns=0, pm=1, nc=0, pl=1, ca=1)
    
def unme(item=None):
    unm = ""
    try:
        unm = os.environ["USER"]
    except:
        pass
    return unm

def pnme(item=None):
    nme = "Unknown"
    try:
        nme = xm.findname()['name']
    except:
        pass
    return (nme)

def cnme(item=None):
    return ("Tavrohi")

def cfl(item=None):
    pfcus = cmds.getPanel(withFocus=1)
    cfcus = cmds.modelPanel(pfcus, q=1, camera=1)
    focal = cmds.getAttr(cfcus+".focalLength")
    return (str(focal))

def framn(item=None):
    start = cmds.playbackOptions(q=1, min=1)
    curr = cmds.currentTime(q=1)
    end = cmds.playbackOptions(q=1, max=1)
    fps_str = cmds.currentUnit(q=1, time=1)
    fps_int = mel.eval("currentTimeUnitToFPS")
    disp_str = "[ " + str(start) + " / " + str(curr) + " / " + str(end) + " ] " + str(fps_str).upper() + " (" + str(fps_int) + ")"
    return disp_str

def filenme(item=None):
    showname_f = pm.sceneName()
    buffer = showname_f.split("/")
    buffer1 = buffer[-1].split(".")
    fnme = buffer1[0]
    return fnme

def cntref(item=None):
    refs = cmds.file(q=1, r=1)
    total_refs = len(refs)
    onrefs = []
    for each in refs:
        if cmds.referenceQuery(each, il=1):
            onrefs.append(each)
    total_onrefs = len(onrefs)
    disp_str = str(total_onrefs) + " / " + str(total_refs)
    return disp_str

def datetime(item=None):
    date = cmds.date()
    return date

def usernamepbdisp():
    cmds.headsUpDisplay("HUD_usernamepbdisp", section=6, block=2, blockSize = "small", dfs = "large", ao=2, l="User Name", command=unme)

def projectnamedisp():
    cmds.headsUpDisplay("HUD_projectnamedisp", section=1, block=3, blockSize="small", dfs="large", lfs="large",  ao=1, l="Project Name", command=pnme)
    
def cnamedisp():
    cmds.headsUpDisplay("HUD_cnamedisp", section=2, block=4, blockSize="small", dfs="large",  lfs="large", ao=1, l="", command=cnme)

def camfldisp():
    cmds.headsUpDisplay("HUD_camfldisp", section=8, block=3, ba="left", blockSize="small", dfs="large", lfs="large", ao=1, l="Focal length", command=cfl, atr=1)
    
def framndisp():
    cmds.headsUpDisplay("HUD_framndisp", section=8, block=2, blockSize="small", dfs="large",  lfs="large", ao=2, l="Frame", command=framn, atr=1)

def filenmedisp():
    cmds.headsUpDisplay("HUD_filenmedisp", section=3, block=2, blockSize="small", dfs="large",  lfs="large", ao=1, l="File Name", command=filenme)

def cntrefdisp():
    cmds.headsUpDisplay("HUD_cntrefdisp", section=6, block=3, blockSize="small", dfs="large", lfs="large", ao=2, l="Refs", command=cntref)

def datedisp():
    cmds.headsUpDisplay("HUD_datedisp", section=3, block=3, blockSize="small", dfs="large", lfs="large", ao=2, l="Date and Time", command=datetime, atr=1)

def check():
    try:
        usernamepbdisp()
    except:
        pass
    try:
        projectnamedisp()
    except:
        pass
    try:
        cnamedisp()
    except:
        pass
    try:
        camfldisp()
    except:
        pass
    try:
        framndisp()
    except:
        pass
    try:
        camnamedisp()
    except:
        pass
    try:
        filenmedisp()
    except:
        pass
    try:
        cntrefdisp()
    except:
        pass
    try:
        datedisp()
    except:
        pass
    
def rem():
    cmds.headsUpDisplay( "HUD_usernamepbdisp", rem=True )
    cmds.headsUpDisplay( "HUD_projectnamedisp", rem=True )
    cmds.headsUpDisplay( "HUD_cnamedisp", rem=True )
    cmds.headsUpDisplay( "HUD_camfldisp", rem=True )
    cmds.headsUpDisplay( "HUD_framndisp", rem=True )
    cmds.headsUpDisplay( "HUD_filenmedisp", rem=True )
    cmds.headsUpDisplay( "HUD_cntrefdisp", rem=True )
    cmds.headsUpDisplay( "HUD_datedisp", rem=True )