import maya.cmds as cmds
import pymel.core as pm
import tools.anim_ui_scripts.file_checker as fc

WINDOW_SIDE_TITLE = "Animation Tools"
WINDOW_DISPLAY_TEXT = "TAV Tools Animation Toolkit"

def windowanimlayout():
    cmds.scrollLayout(w=240)
    cmds.columnLayout(w=220, co=("left",10))
    cmds.text(l="",h=10)
    cmds.text(label=WINDOW_DISPLAY_TEXT, align='center', font='boldLabelFont')
    cmds.text(l="",h=10)
    
    cmds.button(label = "Anim/Layout Check and Playblast", width=200, bgc=(0.1,0.1,0.1), c=("anim_ui.apbui()"))
    #cmds.button(label = "FK IK Switch", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"tools/anim_ui_scripts/FkIK_Switch.mel\"; db_IKFkWindow;')")
    #cmds.button(label = "Auto Tangent", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"tools/anim_ui_scripts/Auto_Tangent.mel\"; autoTangent;')")
    cmds.button(label = "Crack Selections", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"tools/anim_ui_scripts/CrackSelections.mel\"; craSelections;')")
    cmds.button(label = "Auto Save", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"tools/anim_ui_scripts/AutoSave.mel\"; autosaveoon;')")
    cmds.button(label = "FINALIZE", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"tools/anim_ui_scripts/Finalize.mel\"; finalizze;')")
    cmds.button(label = "Remove Unload References", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"tools/anim_ui_scripts/xtras.mel\"; remove_unload_references;')")
    cmds.button(label = "Remove Namespace", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"tools/anim_ui_scripts/Finalize.mel\"; sbRemoveNSproc;')")
    cmds.button(label = "Remove Extra Camera", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"tools/anim_ui_scripts/xtras.mel\"; remove_extra_cam;')")
    cmds.button(label = "pk Ghost", width=200, bgc=(0.1,0.1,0.1), c="import tools.pk_ghosts\nreload(tools.pk_ghosts)")
    cmds.button(label = "CLOSE EDITORS / BOUNDING BOX", width=200, bgc=(0.22, 1.0, 0.09), c="maya.mel.eval('source \"tools/anim_ui_scripts/xtras.mel\"; Clean_Editors;')")
    

def windowanimui():
    try:
        pm.deleteUI('animwin')
        pm.workspaceControlState('animwin', remove=True)
    except:
        pass
    
    cmds.workspaceControl('animwin', tabToControl=('AttributeEditor', -1), li=1, r=1, mw=250 , label=WINDOW_SIDE_TITLE, uiScript=("anim_ui.windowanimlayout()"))

def apbui(item=None):
    reload(fc)
    abc = fc.animFCmod()
    abc.wincheckui()

if __name__ == "__main__":
    windowanimui()