import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
#from tools.lit_ui_scripts.lit_save_ui import HEIGHT
import tools.showxml as xm
import os
import sans as ss
import playblast as pb
from datetime import datetime
import shutil
reload(ss)

WIDTH = 550
HEIGHT = 410

def mkdirp( path ):
    #try:
    #    cmds.deleteUI('mkfol')
    #except:
    #    pass
        
    try:
        os.makedirs( path )
    except OSError:
        if not os.path.isdir( path ):
            raise

def wincheckui():
    try:
        cmds.windowPref('achkwin', r=1)
    except:
        pass
        
    try:
        cmds.deleteUI('achkwin')
    except:
        pass
        
        
        
    window = cmds.window('achkwin', title="Anim Checker and PB", widthHeight=(WIDTH, HEIGHT) )
    cmds.columnLayout( adjustableColumn=True )
    cmds.text(label="")
    
    cmds.rowLayout(nc = 4)
    cmds.text(label="  Project: ")
    cmds.optionMenu("prj", label='', w=80, changeCommand=setprjnme)
    cmds.text(label="   ")
    cmds.text("prjnme", l="")
    
    cmds.setParent( '..' )
    
    cmds.rowLayout(nc = 7)
    cmds.text(label="  Episode: ")
    cmds.textField("epi", aie=1, ec=changeep)
    cmds.text(label="  Sequence: ")
    cmds.textField("seq", aie=1, ec=changeseq)
    cmds.text(label="  Shot: ")
    cmds.textField("sht", aie=1, ec=changesh)
    cmds.optionMenu("task", label='  ', w=80, changeCommand=changetask)
    cmds.menuItem(label="staging", p="task")
    cmds.menuItem(label="anim", p="task")
    cmds.setParent( '..' )
    
    cmds.rowLayout(nc=2)
    cmds.text(label="  File Name: ")
    cmds.text("flnme", l="")
    cmds.setParent( '..' )
    
    
    cmds.text(label="")
    cmds.text(label="==========")
    cmds.text(label="||     Checks     ||")
    cmds.text(label="==========")
    cmds.text(label="")
    
    cmds.rowLayout(nc = 6)
    cmds.text(l="   ")
    cmds.iconTextButton("chkcam", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chkcam)
    cmds.text(l=" Unwanted Camera")
    #cmds.setParent( '..' )
    #cmds.rowLayout(nc = 3)
    cmds.text(l="                                                  ")
    cmds.iconTextButton("chkimm", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chkimm)
    cmds.text(l=" Imported Mesh")
    cmds.setParent( '..' )
    cmds.rowLayout(nc = 6)
    cmds.text(l="   ")
    cmds.iconTextButton("chknms", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chknms)
    cmds.text(l=" Name Space Exists")
    #cmds.setParent( '..' )
    #cmds.rowLayout(nc = 3)
    cmds.text(l="                                                   ")
    cmds.iconTextButton("chkrap", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chkrap)
    cmds.text(l=" Referenced Asset Path")
    cmds.setParent( '..' )
    cmds.rowLayout(nc = 6)
    cmds.text(l="   ")
    cmds.iconTextButton("chklit", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chklit)
    cmds.text(l=" Imported Lights")
    #cmds.setParent( '..' )
    #cmds.rowLayout(nc = 3)
    cmds.text(l="                                                       ")
    cmds.iconTextButton("chkfps", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chkfps)
    cmds.text(l=" Time Unit / FPS")
    cmds.setParent( '..' )
    cmds.rowLayout(nc = 6)
    cmds.text(l="   ")
    cmds.iconTextButton("chkmav", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chkmav)
    cmds.text(l=" Maya Version")
    #cmds.setParent( '..' )
    #cmds.rowLayout(nc = 3)
    cmds.text(l="                                                           ")
    cmds.iconTextButton("chkdsl", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chkdsl)
    cmds.text(l=" Display Layer")
    cmds.setParent( '..' )
    cmds.rowLayout(nc = 6)
    cmds.text(l="   ")
    cmds.iconTextButton("chkrdl", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chkrdl)
    cmds.text(l=" Render Layer")
    #cmds.setParent( '..' )
    #cmds.rowLayout(nc = 3)
    cmds.text(l="                                                            ")
    cmds.iconTextButton("chkanl", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chkanl)
    cmds.text(l=" Animation Layer")
    cmds.setParent( '..' )
    cmds.rowLayout(nc = 6)
    cmds.text(l="   ")
    cmds.iconTextButton("chkpcm", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chkpcm)
    cmds.text(l=" Correct Camera")
    #cmds.setParent( '..' )
    #cmds.rowLayout(nc = 3)
    cmds.text(l="                                                        ")
    cmds.iconTextButton("chkmfr", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chkmfr)
    cmds.text(l=" 101 Frame Range")
    cmds.setParent( '..' )
    #cmds.rowLayout(nc = 6)
    #cmds.text(l="   ")
    #cmds.iconTextButton("chkaex", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chkaex)
    #cmds.text(l=" Audio Exists")
    #cmds.text(l="                                                             ")
    #cmds.iconTextButton("chkmfr", style='iconOnly', image=retimg("grey.png"), w=20, h=20, c=chkmfr)
    #cmds.text(l=" 101 Frame Range")
    #cmds.setParent( '..' )
    
    
    
    cmds.text(label="")
    cmds.text("Status", l="not_saved", vis=0)
    cmds.rowLayout(nc = 4)
    cmds.text("     ")
    cmds.checkBox("svl", l="Save in Local", v=1, cc=updatesl)
    cmds.text(" "*105)
    cmds.checkBox("fce", l="FBX Cam Exp", v=1)
    cmds.setParent( '..' )
    cmds.rowLayout(nc=3)
    cmds.text(label="  File Path: ")
    cmds.textField("flpth", tx="", ed=0, w=450)
    cmds.iconTextButton("outfoldicn", style='iconOnly', image=retimg("folder.png"), w=20, h=20, c=openoutfolder)
    cmds.setParent( '..' )
    cmds.text(label="")
    cmds.rowLayout(nc = 3)
    cmds.button(label="Check file", w=180, c=chkall)
    cmds.button(label="Save file", w=180, c=savethefile)
    cmds.button(label="Playblast", w=180, c=dopbchk)
    cmds.setParent( '..' )
    
    cmds.text(l="")
    cmds.frameLayout("errlogsframe", l="Errors", cll = True, cl= True, pcc=collapefl, pec=expandfl)
    cmds.textScrollList("errlogs", numberOfRows=10, allowMultiSelection=True, sc=selectitems)
    cmds.setParent( '..' )

    cmds.setParent( '..' )
    cmds.showWindow( window )
    getprj()
    
def chkall(item=None):
    cmds.textScrollList("errlogs", e=1, ra=1)
    chkcam()
    chkimm()
    chknms()
    chkrap()
    chklit()
    chkfps()
    chkmav()
    chkdsl()
    chkrdl()
    chkanl()
    #chkaex()
    chkmfr()
    chkpcm()
    checkcollapse()

def changed(item=None):
    all_chks = ["chkcam", "chkimm", "chknms", "chkrap", "chklit", "chkfps", "chkmav", "chkdsl", "chkrdl", "chkanl", "chkmfr", "chkpcm"]
    for each in all_chks:
        cmds.iconTextButton(each, e=1, image=retimg("grey.png"))

def chkcam(item=None):
    if not ss.check_unwanted_camera():
        cmds.iconTextButton("chkcam", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chkcam", e=1, image=retimg("red.png"))
        
def chkimm(item=None):
    if not ss.check_imported_mesh_objects():
        cmds.iconTextButton("chkimm", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chkimm", e=1, image=retimg("red.png"))
        
def chknms(item=None):
    if not ss.check_name_spaces():
        cmds.iconTextButton("chknms", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chknms", e=1, image=retimg("red.png"))
        
def chkrap(item=None):
    code = cmds.optionMenu("prj", q=1, v=1)
    ep = cmds.textField("epi", q=1, tx=1)
    if not ss.check_reference_asset_path(code, ep):
        cmds.iconTextButton("chkrap", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chkrap", e=1, image=retimg("red.png"))
        
def chklit(item=None):
    if not ss.check_lights():
        cmds.iconTextButton("chklit", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chklit", e=1, image=retimg("red.png"))
        
def chkfps(item=None):
    code = cmds.optionMenu("prj", q=1, v=1)
    if not ss.check_time_unit(code):
        cmds.iconTextButton("chkfps", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chkfps", e=1, image=retimg("red.png"))
        
def chkmav(item=None):
    code = cmds.optionMenu("prj", q=1, v=1)
    if not ss.check_maya_cut_id(code):
        cmds.iconTextButton("chkmav", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chkmav", e=1, image=retimg("red.png"))
        
def chkdsl(item=None):
    if not ss.check_display_layer():
        cmds.iconTextButton("chkdsl", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chkdsl", e=1, image=retimg("red.png"))
        
def chkrdl(item=None):
    if not ss.check_render_layer():
        cmds.iconTextButton("chkrdl", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chkrdl", e=1, image=retimg("red.png"))
        
def chkanl(item=None):
    if not ss.check_anim_layer():
        cmds.iconTextButton("chkanl", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chkanl", e=1, image=retimg("red.png"))

def chkaex(item=None):
    if not ss.check_audio():
        cmds.iconTextButton("chkaex", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chkaex", e=1, image=retimg("red.png"))
        
def chkmfr(item=None):
    if not ss.check_101_frame_range():
        cmds.iconTextButton("chkmfr", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chkmfr", e=1, image=retimg("red.png"))
        
def chkpcm(item=None):
    if not ss.check_proper_camera():
        cmds.iconTextButton("chkpcm", e=1, image=retimg("green.png"))
    else:
        cmds.iconTextButton("chkpcm", e=1, image=retimg("red.png"))
        
def retimg(imga):
    diri = os.path.dirname(__file__)
    diri = os.path.join(diri, "icons", imga).replace("\\","/")
    #diri = "\"" + diri + "\"" 
    return diri
    
def openoutfolder(item=None):
    dir_o = cmds.textField("flpth", q=1, tx=1)
    if(not os.path.exists(dir_o)):
        mkdirp(dir_o)
    cmds.launch(directory=dir_o)
    
def getprj(item=None):
    reload(xm)
    all_c = xm.findallcode()
    for ech in all_c:
        cmds.menuItem(label=ech, p="prj")
    
    setfilename()
    updateproperfilename()
    setprjnme()

def updateproperfilename():
    code = cmds.optionMenu("prj", q=1, v=1).lower()
    epname = cmds.textField("epi", q=1, tx=1)
    sqname = cmds.textField("seq", q=1, tx=1)
    shname = cmds.textField("sht", q=1, tx=1)
    task = cmds.optionMenu("task", q=1, v=1)
    if(task == "staging"):
        task = "stg"
    else:
        task = "anim"
        
    filename = code + "_" + epname + "_" + sqname + "_" + shname + "_" + task + ".ma"
    cmds.text("flnme", e=1, l=filename)

def setfilename(item=None):
    showname_f = pm.sceneName()
    buffer = showname_f.split("/")
    filename = buffer[-1]
    cmds.text("flnme", e=1, l=filename)
    if(len(filename) > 1):
        setfromname()
    else:
        code = cmds.optionMenu("prj", q=1, v=1)
        filename = code.lower() + "_ep000_sq01_sh001_stg.ma"
        cmds.text("flnme", e=1, l=filename)
        cmds.textField("epi", e=1, tx="ep000")
        cmds.textField("seq", e=1, tx="sq01")
        cmds.textField("sht", e=1, tx="sh001")
        setfromname()

def setfromname(item=None):

    ### Initialize Code
    filename = cmds.text("flnme", q=1, l=1)
    code = filename.split("_")[0]
    itms = cmds.menu("prj", q=True, ia=True)
    i = 1
    got_prj = False
    for each in itms:
        val = cmds.menuItem(each, q=1, l=1)
        if code.lower() == val.lower():
            cmds.optionMenu("prj", e=1, sl=i)
            got_prj = True
        i = i + 1
    
    if not got_prj:
        code = cmds.optionMenu("prj", q=1, v=1 )
        filename = code.lower() + "_" + filename
        
    ### Initialize task
    taskq = filename.split(".")[0].split("_")
    for ech in taskq:
        if(ech == "anim"):
            cmds.optionMenu("task", e=1, sl=2)
            task = "anim"
            break
        elif(ech == "stg"):
            cmds.optionMenu("task", e=1, sl=1)
            task = "stg"
            break
        
    ### Initialize Episode
    epnameq = filename.split(".")[0].split("_")
    folderpth = xm.findfolderpath(code)
    epname = "ep000"
    for each in epnameq:
        if(each.startswith("ep")):
            epname = "ep" + each.replace("ep","").zfill(3)
            break
    
    
    epfol = os.path.join(folderpth, "03_episode", epname).replace("\\","/")
    if os.path.exists(epfol):
        cmds.textField("epi", e=1, tx=epname)
    else:
        cmds.confirmDialog( title='Episode folder not found',  icon="critical", message=(epname+' can\'t be found. Ask production to build it.'), button=['Okay'], defaultButton='Okay', cancelButton='Okay')
        epfols = epfol.replace(("/" + epname), "")
        eps = os.listdir(epfols)
        for ep in eps:
            if (ep.startswith("ep")) and ("_" not in str(ep)):
                cmds.textField("epi", e=1, tx=ep)
                break
                
    ### Initialize Sequence
    sqnameq = filename.split(".")[0].split("_")
    sqname = "sq01"
    for each in sqnameq:
        if(each.startswith("sq")):
            sqname = "sq" + each.replace("sq","").zfill(2)
            break
    
    
    sveinl = cmds.checkBox("svl", q=1, v=1)
    if(sveinl == 1):
        cmds.textField("seq", e=1, tx=sqname)
    else:
        task  = cmds.optionMenu("task", q=1, v=1)
        if(task == "staging"):
            task = "02_staging"
        else:
            task = "03_animation"
        sqfol = os.path.join(epfol, task, sqname).replace("\\","/")
        if os.path.exists(sqfol):
            cmds.textField("seq", e=1, tx=sqname)
        else:
            cmds.confirmDialog( title='Sequence folder not found',  icon="critical", message=(sqname+' can\'t be found. Ask production to build it.'), button=['Okay'], defaultButton='Okay', cancelButton='Okay')
            epfols = sqfol.replace(("/" + sqname), "")
            eps = os.listdir(epfols)
            for ep in eps:
                if (ep.startswith("sq")) and ("_" not in str(ep)):
                    cmds.textField("seq", e=1, tx=ep)
                    break
                    
    ### Initialize Shot
    shnameq = filename.split(".")[0].split("_")
    shname = "sh001"
    for each in shnameq:
        if(each.startswith("sh")):
            shname = "sh" + each.replace("sh","").zfill(3)
            break
    
    cmds.textField("sht", e=1, tx=shname)
        
    setfolderpath()

def changeseq(item=None):
    filename = cmds.text("flnme", q=1, l=1)
    sq_name_old = filename.split(".")[0].split("_")[2]
    sq_name_new = cmds.textField("seq", q=1, tx=1)
    filename = filename.replace(sq_name_old, sq_name_new)
    cmds.text("flnme", e=1, l=filename)
    
    sqname = filename.split(".")[0].split("_")[2]
    sveinl = cmds.checkBox("svl", q=1, v=1)
    if(sveinl == 1):
        cmds.textField("seq", e=1, tx=sqname)
    else:
        print("Check box off")
        task  = cmds.optionMenu("task", q=1, v=1)
        if(task == "staging"):
            task = "02_staging"
        else:
            task = "03_animation"
        code = filename.split("_")[0]
        epname = filename.split(".")[0].split("_")[1]
        folderpth = xm.findfolderpath(code)
        epfol = os.path.join(folderpth, "03_episode", epname).replace("\\","/")
        sqfol = os.path.join(epfol, task, sqname).replace("\\","/")
        if os.path.exists(sqfol):
            cmds.textField("seq", e=1, tx=sqname)
        else:
            cmds.confirmDialog( title='Sequence folder not found',  icon="critical", message=(sqname+' can\'t be found. Ask production to build it.'), button=['Okay'], defaultButton='Okay', cancelButton='Okay')
            epfols = sqfol.replace(("/" + sqname), "")
            eps = os.listdir(epfols)
            for ep in eps:
                if (ep.startswith("sq")) and ("_" not in str(ep)):
                    cmds.textField("seq", e=1, tx=ep)
                    break
    changesh()

def changesh(item=None):
    filename = cmds.text("flnme", q=1, l=1)
    sh_name_old = filename.split(".")[0].split("_")[3]
    sh_name_new = cmds.textField("sht", q=1, tx=1)
    filename = filename.replace(sh_name_old, sh_name_new)
    cmds.text("flnme", e=1, l=filename)
    
    changetask()

def changetask(item=None):
    filename = cmds.text("flnme", q=1, l=1)
    tsk_name_old = filename.split(".")[0].split("_")[4]
    tsk_name_new = cmds.optionMenu("task", q=1, v=1)
    if(tsk_name_new == "staging"):
        tsk_name_new = "stg"
    else:
        tsk_name_new = "anim"
    filename = filename.replace(tsk_name_old, tsk_name_new)
    cmds.text("flnme", e=1, l=filename)
    
    setfolderpath()

def changeep(item=None):
    filename = cmds.text("flnme", q=1, l=1)
    ep_name_old = filename.split(".")[0].split("_")[1]
    ep_name_new = cmds.textField("epi", q=1, tx=1)
    filename = filename.replace(ep_name_old, ep_name_new)
    cmds.text("flnme", e=1, l=filename)

    #filename = cmds.text("flnme", q=1, l=1)
    code = filename.split("_")[0]
    epname = filename.split(".")[0].split("_")[1]
    folderpth = xm.findfolderpath(code)
    epfol = os.path.join(folderpth, "03_episode", epname).replace("\\","/")
    if os.path.exists(epfol):
        cmds.textField("epi", e=1, tx=epname)
    else:
        cmds.confirmDialog( title='Episode folder not found',  icon="critical", message=(epname+' can\'t be found. Ask production to build it.'), button=['Okay'], defaultButton='Okay', cancelButton='Okay')
        epfols = epfol.replace(("/" + epname), "")
        eps = os.listdir(epfols)
        for ep in eps:
            if (ep.startswith("ep")) and ("_" not in str(ep)):
                cmds.textField("epi", e=1, tx=ep)
                break
                
    changeseq()

def updatesl(item=None):
    changeep()
    setfolderpath()

def changecode(item=None):
    cde = cmds.optionMenu("prj", q=1, v=1)
    filename = cmds.text("flnme", q=1, l=1)
    old_cde = filename.split(".")[0].split("_")[0]
    chkep = old_cde.startswith("ep")
    chksq = old_cde.startswith("sq")
    chksh = old_cde.startswith("sh")
    if chkep == False and chksq == False and chksh == False:
        filename = filename.replace(old_cde, cde.lower())
    else:
        filename = cde.lower() + "_" + filename
    cmds.text("flnme", e=1, l=filename)
    #setfilename()
    changeep()

def setprjnme(item=None):
    cde = cmds.optionMenu("prj", q=1, v=1)
    fulnme = xm.findname(cde)["name"]
    cmds.text("prjnme", e=1, l=fulnme)
    changecode()
    
def setfolderpath(item=None):
    sveinl = cmds.checkBox("svl", q=1, v=1)
    if(sveinl == 1):
        code = cmds.optionMenu("prj", q=1, v=1)
        nme = xm.findname(code)['name']
        ep_name  = cmds.textField("epi", q=1, tx=1)
        ###task-add
        task  = cmds.optionMenu("task", q=1, v=1)
        if(task == "staging"):
            task = "02_staging"
        else:
            task = "03_animation"
        sq_name  = cmds.textField("seq", q=1, tx=1)
        sh_name  = cmds.textField("sht", q=1, tx=1)
        folderpth = os.path.join("D:/", nme , ep_name, task, sq_name, sh_name).replace("\\","/")
    else:
        code = cmds.optionMenu("prj", q=1, v=1)
        folderpth = xm.findfolderpath(code)
        ep_name  = cmds.textField("epi", q=1, tx=1)
        ###task-add
        task  = cmds.optionMenu("task", q=1, v=1)
        if(task == "staging"):
            task = "02_staging"
        else:
            task = "03_animation"
        sq_name  = cmds.textField("seq", q=1, tx=1)
        sh_name  = cmds.textField("sht", q=1, tx=1)
        folderpth = os.path.join(folderpth, "03_episode", ep_name, task, sq_name, sh_name).replace("\\","/")
    cmds.textField("flpth", e=1, tx=folderpth)
    changed()
    
def savethefile(item=None):
    all_chks = ["chkcam", "chkimm", "chknms", "chkrap", "chklit", "chkfps", "chkmav", "chkdsl", "chkrdl", "chkanl", "chkmfr", "chkpcm"]
    unchecked = 0
    for each in all_chks:
        imagepth = cmds.iconTextButton(each, q=1, image=1)
        img = imagepth.split("/")[-1].split(".")[0]
        if img == "grey":
            unchecked = 1
            cmds.confirmDialog( title='File not checked',  icon="critical", message="Kindly check all the checks before saving", button=['Okay'], defaultButton='Okay', cancelButton='Okay')
            break

    if unchecked == 0:
        file_name = cmds.text("flnme", q=1, l=1)
        file_path = cmds.textField("flpth", q=1, tx=1)
        if(not os.path.exists(file_path)):
            mkdirp(file_path)
            
        file_fullname = os.path.join(file_path, file_name).replace("\\","/")
        chk_fe = os.path.isfile(file_fullname)
        
        if(chk_fe == False):
            cmds.file(rn=file_fullname)
            cmds.file(f=True, save=True, options="v=0;", type="mayaAscii")
        else:
            back_fol = os.path.join(file_path, "bak").replace("\\","/")
            if(not os.path.exists(back_fol)):
                mkdirp(back_fol)
            time_stamp = datetime.today().strftime('%y%m%d%H%M%S')
            unm = os.environ["USER"]
            back_file_name = file_name.replace(".ma",("_" + time_stamp + "_" + unm + ".ma"))
            back_file_path = os.path.join(back_fol, back_file_name).replace("\\","/")
            shutil.copy(file_fullname, back_file_path)
            cmds.file(rn=file_fullname)
            cmds.file(f=True, save=True, options="v=0;", type="mayaAscii")
        
        cmds.text("Status", e=1, l="saved")

def camlock(item=None):
    attributes = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".v"]
    all_c = cmds.ls(type = "camera", l=1)
    e=1
    for each in all_c:
        if each.startswith("|render_cam|"):
            ep = cmds.listRelatives(each, p=1)
            for i in attributes:
                try:
                    cmds.setAttr( (ep[0]+i), lock=True)
                except:
                    pass

def dopbchk(item=None):
    fileCheckState = 1
    if cmds.text("Status", q=1, l=1) == "saved":
        fileCheckState = 0
        
    if fileCheckState:
        cmds.confirmDialog( title='File Unsaved',  icon="critical", message="File not saved.\nThere are unsaved changes,\nkindly save the file and then Playblast", button=['Okay'], defaultButton='Okay', cancelButton='Okay')
    else:
        all_chks = ["chkcam", "chkimm", "chknms", "chkrap", "chklit", "chkfps", "chkmav", "chkdsl", "chkrdl", "chkanl", "chkmfr", "chkpcm"]
        unchecked = 0
        okay = 1
        for each in all_chks:
            imagepth = cmds.iconTextButton(each, q=1, image=1)
            img = imagepth.split("/")[-1].split(".")[0]
            if img == "grey":
                unchecked = 1
                cmds.confirmDialog( title='File not checked',  icon="critical", message="Kindly check all the checks before playblasting", button=['Okay'], defaultButton='Okay', cancelButton='Okay')
                break
            if img == "red":
                okay = 0
        
        if unchecked == 0:
            camlock()
            reload(pb)
            fce = cmds.checkBox("fce", q=1, v=1)
            if(fce == 1):
                exportfbxcam()
            if (okay):
                pb.playbblastmain(1)
            else:
                pb.playbblastmain(0)

def exportfbxcam(item=None):
    imagepth = cmds.iconTextButton("chkpcm", q=1, image=1)
    img = imagepth.split("/")[-1].split(".")[0]
    if img == "green":
        print("FBX")
        mel.eval('source "tools/anim_ui_scripts/cam_bke"')
        abc = mel.eval('RenderCamBake("render_cam")')
        print(abc)

        ##Load fbx plugin
        if(not cmds.pluginInfo("fbxmaya", query=1, name=1, loaded=1)):
            cmds.loadPlugin("fbxmaya")

        ##Update the fbx settings
        pm.mel.eval('FBXExportFileVersion "FBX2010"')
        pm.mel.eval('FBXResetExport')
        pm.mel.eval('FBXExportInputConnections -v 0')
        pm.mel.eval('FBXExportBakeComplexAnimation -v 1')
        pm.mel.eval('FBXExportInAscii -v true')

        ##FBX Export ---> Cam
        file_name = (cmds.text("flnme", q=1, l=1).replace(".ma","_renCam.fbx"))
        file_path = cmds.textField("flpth", q=1, tx=1)
        if(not os.path.exists(file_path)):
            mkdirp(file_path)
            
        file_fullname = os.path.join(file_path, file_name).replace("\\","/")
        chk_fe = os.path.isfile(file_fullname)
        
        if(chk_fe == False):
            cmds.select(abc)
            cmds.file(file_fullname, force=True, options="v=0;", typ="FBX export", pr=False, es=True)
        else:
            back_fol = os.path.join(file_path, "bak").replace("\\","/")
            if(not os.path.exists(back_fol)):
                mkdirp(back_fol)
            time_stamp = datetime.today().strftime('%y%m%d%H%M%S')
            unm = os.environ["USER"]
            back_file_name = file_name.replace(".fbx",("_" + time_stamp + "_" + unm + ".fbx"))
            back_file_path = os.path.join(back_fol, back_file_name).replace("\\","/")
            shutil.copy(file_fullname, back_file_path)
            cmds.select(abc)
            cmds.file(file_fullname, force=True, options="v=0;", typ="FBX export", pr=False, es=True)

        cmds.select(cl=True)
        cmds.delete(abc)
    else:
        cmds.confirmDialog( title='Error FBX Cam',  icon="critical", message="Kindly resolve 'Correct Camera' issue", button=['Okay'], defaultButton='Okay', cancelButton='Okay')

def checkcollapse(item=None):
    items = cmds.textScrollList("errlogs", q=1, ni=1)
    if items != 0:
        cmds.frameLayout("errlogsframe", e=1, cl=0)
        expandfl()
    else:
        cmds.frameLayout("errlogsframe", e=1, cl=1)
        collapefl()

def selectitems(item=None):
    selected = cmds.textScrollList("errlogs", q=1, sut=1)
    tosel = []
    for ech in selected:
        if ech != '':
            tosel.append(ech)

    cmds.select(tosel)

def collapefl(item=None):
    cmds.window('achkwin', e=1, widthHeight=(WIDTH, HEIGHT))

def expandfl(item=None):
    cmds.window('achkwin', e=1, widthHeight=(WIDTH, HEIGHT+80))
