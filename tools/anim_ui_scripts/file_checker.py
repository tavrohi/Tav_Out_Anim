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
import re
reload(ss)

WIDTH = 550
HEIGHT = 410

class animFCmod():

    def __init__(self):
        self.all_c = xm.findallcode()
        self.show = ""
        self.episode = ""
        self.sequence = ""
        self.shot = ""
        self.task = ""

    def mkdirp(self, path ):
        #try:
        #    cmds.deleteUI('mkfol')
        #except:
        #    pass
            
        try:
            os.makedirs( path )
        except OSError:
            if not os.path.isdir( path ):
                raise

    def wincheckui(self):
        try:
            cmds.windowPref('achkwin', r=1)
        except:
            pass
            
        try:
            cmds.deleteUI('achkwin')
        except:
            pass
            
        window = cmds.window('achkwin', title="Anim Checker and PB 2", widthHeight=(WIDTH, HEIGHT) )
        cmds.columnLayout( adjustableColumn=True )
        cmds.text(label="")
        
        cmds.rowLayout(nc = 4)
        cmds.text(label="  Project: ")
        cmds.optionMenu("prj", label='', w=80, changeCommand=self.changeshow)
        cmds.text(label="   ")
        cmds.text("prjnme", l="")
        
        cmds.setParent( '..' )
        
        cmds.rowLayout(nc = 7)
        cmds.text(label="  Episode: ")
        cmds.textField("epi", cc=self.changeepisode)
        cmds.text(label="  Sequence: ")
        cmds.textField("seq", cc=self.changesequence)
        cmds.text(label="  Shot: ")
        cmds.textField("sht", cc=self.changeshot)
        cmds.optionMenu("task", label='  ', w=80, changeCommand=self.changetask)
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
        cmds.iconTextButton("chkcam", style='iconOnly', image=self.retimg("grey.png"), w=20, h=20, c=self.chkcam)
        cmds.text(l=" Unwanted Camera")
        #cmds.setParent( '..' )
        #cmds.rowLayout(nc = 3)
        cmds.text(l="                                                  ")
        cmds.iconTextButton("chkimm", style='iconOnly', image=self.retimg("grey.png"), w=20, h=20, c=self.chkimm)
        cmds.text(l=" Imported Mesh")
        cmds.setParent( '..' )
        cmds.rowLayout(nc = 6)
        cmds.text(l="   ")
        cmds.iconTextButton("chknms", style='iconOnly', image=self.retimg("grey.png"), w=20, h=20, c=self.chknms)
        cmds.text(l=" Name Space Exists")
        #cmds.setParent( '..' )
        #cmds.rowLayout(nc = 3)
        cmds.text(l="                                                   ")
        cmds.iconTextButton("chkrap", style='iconOnly', image=self.retimg("grey.png"), w=20, h=20, c=self.chkrap)
        cmds.text(l=" Referenced Asset Path")
        cmds.setParent( '..' )
        cmds.rowLayout(nc = 6)
        cmds.text(l="   ")
        cmds.iconTextButton("chklit", style='iconOnly', image=self.retimg("grey.png"), w=20, h=20, c=self.chklit)
        cmds.text(l=" Imported Lights")
        #cmds.setParent( '..' )
        #cmds.rowLayout(nc = 3)
        cmds.text(l="                                                       ")
        cmds.iconTextButton("chkfps", style='iconOnly', image=self.retimg("grey.png"), w=20, h=20, c=self.chkfps)
        cmds.text(l=" Time Unit / FPS")
        cmds.setParent( '..' )
        cmds.rowLayout(nc = 6)
        cmds.text(l="   ")
        cmds.iconTextButton("chkmav", style='iconOnly', image=self.retimg("grey.png"), w=20, h=20, c=self.chkmav)
        cmds.text(l=" Maya Version")
        #cmds.setParent( '..' )
        #cmds.rowLayout(nc = 3)
        cmds.text(l="                                                           ")
        cmds.iconTextButton("chkdsl", style='iconOnly', image=self.retimg("grey.png"), w=20, h=20, c=self.chkdsl)
        cmds.text(l=" Display Layer")
        cmds.setParent( '..' )
        cmds.rowLayout(nc = 6)
        cmds.text(l="   ")
        cmds.iconTextButton("chkrdl", style='iconOnly', image=self.retimg("grey.png"), w=20, h=20, c=self.chkrdl)
        cmds.text(l=" Render Layer")
        #cmds.setParent( '..' )
        #cmds.rowLayout(nc = 3)
        cmds.text(l="                                                            ")
        cmds.iconTextButton("chkanl", style='iconOnly', image=self.retimg("grey.png"), w=20, h=20, c=self.chkanl)
        cmds.text(l=" Animation Layer")
        cmds.setParent( '..' )
        cmds.rowLayout(nc = 6)
        cmds.text(l="   ")
        cmds.iconTextButton("chkpcm", style='iconOnly', image=self.retimg("grey.png"), w=20, h=20, c=self.chkpcm)
        cmds.text(l=" Correct Camera")
        #cmds.setParent( '..' )
        #cmds.rowLayout(nc = 3)
        cmds.text(l="                                                        ")
        cmds.iconTextButton("chkmfr", style='iconOnly', image=self.retimg("grey.png"), w=20, h=20, c=self.chkmfr)
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
        cmds.checkBox("svl", l="Save in Local", v=1, cc=self.updatesl)
        cmds.text(" "*105)
        cmds.checkBox("fce", l="FBX Cam Exp", v=1)
        cmds.setParent( '..' )
        cmds.rowLayout(nc=3)
        cmds.text(label="  File Path: ")
        cmds.textField("flpth", tx="", ed=0, w=450)
        cmds.iconTextButton("outfoldicn", style='iconOnly', image=self.retimg("folder.png"), w=20, h=20, c=self.openoutfolder)
        cmds.setParent( '..' )
        cmds.text(label="")
        cmds.rowLayout(nc = 3)
        cmds.button(label="Check file", w=180, c=self.chkall)
        cmds.button(label="Save file", w=180, c=self.savethefile)
        cmds.button(label="Playblast", w=180, c=self.dopbchk)
        cmds.setParent( '..' )
        
        cmds.text(l="")
        cmds.frameLayout("errlogsframe", l="Errors", cll = True, cl= True, pcc=self.collapefl, pec=self.expandfl)
        cmds.textScrollList("errlogs", numberOfRows=10, allowMultiSelection=True, sc=self.selectitems)
        cmds.setParent( '..' )

        cmds.setParent( '..' )
        cmds.showWindow( window )
        self.getprj()
        
    def chkall(self, item=None):
        self.changeepisode()
        cmds.textScrollList("errlogs", e=1, ra=1)
        self.chkcam()
        self.chkimm()
        self.chknms()
        self.chkrap()
        self.chklit()
        self.chkfps()
        self.chkmav()
        self.chkdsl()
        self.chkrdl()
        self.chkanl()
        #chkaex()
        self.chkmfr()
        self.chkpcm()
        self.checkcollapse()

    def changed(self, item=None):
        all_chks = ["chkcam", "chkimm", "chknms", "chkrap", "chklit", "chkfps", "chkmav", "chkdsl", "chkrdl", "chkanl", "chkmfr", "chkpcm"]
        for each in all_chks:
            cmds.iconTextButton(each, e=1, image=self.retimg("grey.png"))

    def chkcam(self, item=None):
        if not ss.check_unwanted_camera():
            cmds.iconTextButton("chkcam", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chkcam", e=1, image=self.retimg("red.png"))
            
    def chkimm(self, item=None):
        if not ss.check_imported_mesh_objects():
            cmds.iconTextButton("chkimm", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chkimm", e=1, image=self.retimg("red.png"))
            
    def chknms(self, item=None):
        if not ss.check_name_spaces():
            cmds.iconTextButton("chknms", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chknms", e=1, image=self.retimg("red.png"))
            
    def chkrap(self, item=None):
        code = cmds.optionMenu("prj", q=1, v=1)
        ep = cmds.textField("epi", q=1, tx=1)
        if not ss.check_reference_asset_path(code, ep):
            cmds.iconTextButton("chkrap", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chkrap", e=1, image=self.retimg("red.png"))
            
    def chklit(self, item=None):
        if not ss.check_lights():
            cmds.iconTextButton("chklit", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chklit", e=1, image=self.retimg("red.png"))
            
    def chkfps(self, item=None):
        code = cmds.optionMenu("prj", q=1, v=1)
        if not ss.check_time_unit(code):
            cmds.iconTextButton("chkfps", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chkfps", e=1, image=self.retimg("red.png"))
            
    def chkmav(self, item=None):
        code = cmds.optionMenu("prj", q=1, v=1)
        if not ss.check_maya_cut_id(code):
            cmds.iconTextButton("chkmav", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chkmav", e=1, image=self.retimg("red.png"))
            
    def chkdsl(self, item=None):
        if not ss.check_display_layer():
            cmds.iconTextButton("chkdsl", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chkdsl", e=1, image=self.retimg("red.png"))
            
    def chkrdl(self, item=None):
        if not ss.check_render_layer():
            cmds.iconTextButton("chkrdl", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chkrdl", e=1, image=self.retimg("red.png"))
            
    def chkanl(self, item=None):
        if not ss.check_anim_layer():
            cmds.iconTextButton("chkanl", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chkanl", e=1, image=self.retimg("red.png"))

    def chkaex(self, item=None):
        if not ss.check_audio():
            cmds.iconTextButton("chkaex", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chkaex", e=1, image=self.retimg("red.png"))
            
    def chkmfr(self, item=None):
        if not ss.check_101_frame_range():
            cmds.iconTextButton("chkmfr", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chkmfr", e=1, image=self.retimg("red.png"))
            
    def chkpcm(self, item=None):
        if not ss.check_proper_camera():
            cmds.iconTextButton("chkpcm", e=1, image=self.retimg("green.png"))
        else:
            cmds.iconTextButton("chkpcm", e=1, image=self.retimg("red.png"))
            
    def retimg(self, imga):
        diri = os.path.dirname(__file__)
        diri = os.path.join(diri, "icons", imga).replace("\\","/")
        #diri = "\"" + diri + "\"" 
        return diri
        
    def openoutfolder(self, item=None):
        dir_o = cmds.textField("flpth", q=1, tx=1)
        if(not os.path.exists(dir_o)):
            self.mkdirp(dir_o)
        cmds.launch(directory=dir_o)
        
    def getprj(self, item=None):

        for ech in self.all_c:
            cmds.menuItem(label=ech, p="prj")
        
        self.setinitial()

    def setinitial(self):
        showname_f = pm.sceneName()
        buffer = showname_f.split("/")
        filename = buffer[-1]
        print(filename)
        show_code = filename[:3]

        if show_code.upper() in self.all_c:
            self.show = show_code

        if "ep" in filename.lower():
            try:
                x = filename.lower().split("ep")[-1]
                e = str(int(re.findall(r'\d+', x)[0])).zfill(3)
                self.episode = "ep" + e
            except:
                pass

        if "sq" in filename.lower():
            try:
                x = filename.lower().split("sq")[-1]
                e = str(int(re.findall(r'\d+', x)[0])).zfill(2)
                self.sequence = "sq" + e
            except:
                pass

        if "sh" in filename.lower():
            try:
                x = filename.lower().split("sh")[-1]
                e = str(int(re.findall(r'\d+', x)[0])).zfill(3)
                self.shot = "sh" + e
            except:
                pass

        if "anim" in filename.lower():
            self.task = "anim"
        else:
            self.task = "staging"

        if self.show == "":
            self.show = self.all_c[0]
        if self.episode == "":
            self.episode = "ep000"
        if self.sequence == "":
            self.sequence = "sq01"
        if self.shot == "":
            self.shot = "sh001"

        print(self.show)
        print(self.episode)
        print(self.sequence)
        print(self.shot)
        print(self.task)
        self.setshow()
    
    def setshow(self):
        i = 1
        itms = cmds.menu("prj", q=True, ia=True)
        for each in itms:
            val = cmds.menuItem(each, q=1, l=1)
            if self.show.lower() == val.lower():
                cmds.optionMenu("prj", e=1, sl=i)
            i = i + 1
        self.setepisode()

    def setepisode(self):
        filepath = xm.findfolderpath(self.show.lower())
        epfol = os.path.join(filepath, "03_episode", self.episode).replace("\\","/")
        if os.path.exists(epfol):
            cmds.textField("epi", e=1, tx=self.episode)
        else:
            cmds.confirmDialog( title='Episode folder not found',  icon="critical", message=(self.episode+' can\'t be found. Ask production to build it.'), button=['Okay'], defaultButton='Okay', cancelButton='Okay')
            epfols = epfol.replace(("/" + self.episode), "")
            eps = os.listdir(epfols)
            for ep in eps:
                if (ep.startswith("ep")) and ("_" not in str(ep)):
                    self.episode = ep
                    self.setepisode()
                    break

        self.setsequence()

    def setsequence(self):
        filepath = xm.findfolderpath(self.show.lower())
        epfol = os.path.join(filepath, "03_episode", self.episode, ).replace("\\","/")
        if(self.task == "staging"):
            task = "02_staging"
        else:
            task = "03_animation"

        sveinl = cmds.checkBox("svl", q=1, v=1)
        if(sveinl == 1):
            cmds.textField("seq", e=1, tx=self.sequence)
        else:
            task  = cmds.optionMenu("task", q=1, v=1)
            if(self.task == "staging"):
                task = "02_staging"
            else:
                task = "03_animation"
            sqfol = os.path.join(epfol, task, self.sequence).replace("\\","/")
            if os.path.exists(sqfol):
                cmds.textField("seq", e=1, tx=self.sequence)
            else:
                cmds.confirmDialog( title='Sequence folder not found',  icon="critical", message=(self.sequence+' can\'t be found. Ask production to build it.'), button=['Okay'], defaultButton='Okay', cancelButton='Okay')
                epfols = sqfol.replace(("/" + self.sequence), "")
                eps = os.listdir(epfols)
                for ep in eps:
                    if (ep.startswith("sq")) and ("_" not in str(ep)):
                        self.sequence = ep
                        self.setsequence()
                        break

        self.setshot()

    def setshot(self):
        cmds.textField("sht", e=1, tx=self.shot)
        self.settask()

    def settask(self):
        i = 1
        itms = cmds.menu("task", q=True, ia=True)
        for each in itms:
            val = cmds.menuItem(each, q=1, l=1)
            if self.task == val.lower():
                cmds.optionMenu("task", e=1, sl=i)
            i = i + 1
        self.setname()

    def setname(self):
        self.filename = "{}_{}_{}_{}_{}.ma".format(self.show, self.episode, self.sequence, self.shot, self.task)
        cmds.text("flnme", e=1, l=self.filename)
        self.setfolderpath()

    def changeshow(self, item=None):
        self.show = cmds.optionMenu("prj", q=1, v=1).lower()
        self.setshow()

    def changeepisode(self, item=None):
        epi = cmds.textField("epi", q=1, tx=1)
        if (epi == ""):
            epi = "ep000"
        e = str(int(re.findall(r'\d+', epi)[0])).zfill(3)
        self.episode = "ep" + e
        self.setepisode()

    def changesequence(self, item=None):
        sq = cmds.textField("seq", q=1, tx=1)
        if(sq == ""):
            sq = "sq01"
        e = str(int(re.findall(r'\d+', sq)[0])).zfill(2)
        self.sequence = "sq" + e
        self.setsequence()

    def changeshot(self, item=None):
        sh = cmds.textField("sht", q=1, tx=1).replace("sh", "")
        shf = ""
        if sh == "":
            sh = "001"
        if re.search("\+", sh):
            shname = sh.split("+")
            for sha in shname:
                shn = str(int(re.findall(r'\d+', sha)[0])).zfill(3)
                try:
                    sht = re.findall(r"[a-zA-Z]+", sha)[0]
                    shn = str(shn+sht)
                except: pass
                if shf:
                    shf = (shf + "+"+ shn)
                else:
                    shf = str(shn)
        else:
            shf = str(int(re.findall(r'\d+', sh)[0])).zfill(3)
            try:
                sht = re.findall(r"[a-zA-Z]+", sh)[0]
                shf = str(shf+sht)
            except: pass

        print(shf)
        self.shot = "sh" + shf
        self.setshot()

    def changetask(self, item=None):
        task = cmds.optionMenu("task", q=1, v=1)
        if(task == "staging"):
            self.task = "stg"
        else:
            self.task = "anim"
        self.settask()

    def updatesl(self, item=None):
        self.changeepisode()

    def setfolderpath(self, item=None):
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
        self.changed()
        
    def savethefile(self, item=None):
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
                self.mkdirp(file_path)
                
            file_fullname = os.path.join(file_path, file_name).replace("\\","/")
            chk_fe = os.path.isfile(file_fullname)
            
            if(chk_fe == False):
                cmds.file(rn=file_fullname)
                cmds.file(f=True, save=True, options="v=0;", type="mayaAscii")
            else:
                back_fol = os.path.join(file_path, "bak").replace("\\","/")
                if(not os.path.exists(back_fol)):
                    self.mkdirp(back_fol)
                time_stamp = datetime.today().strftime('%y%m%d%H%M%S')
                unm = os.environ["USER"]
                back_file_name = file_name.replace(".ma",("_" + time_stamp + "_" + unm + ".ma"))
                back_file_path = os.path.join(back_fol, back_file_name).replace("\\","/")
                shutil.copy(file_fullname, back_file_path)
                cmds.file(rn=file_fullname)
                cmds.file(f=True, save=True, options="v=0;", type="mayaAscii")
            
            cmds.text("Status", e=1, l="saved")

    def camlock(self, item=None):
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

    def dopbchk(self, item=None):
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
                self.camlock()
                reload(pb)
                fce = cmds.checkBox("fce", q=1, v=1)
                if(fce == 1):
                    self.exportfbxcam()
                if (okay):
                    pb.playbblastmain(1)
                else:
                    pb.playbblastmain(0)

    def exportfbxcam(self, item=None):
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
                self.mkdirp(file_path)
                
            file_fullname = os.path.join(file_path, file_name).replace("\\","/")
            chk_fe = os.path.isfile(file_fullname)
            
            if(chk_fe == False):
                cmds.select(abc)
                cmds.file(file_fullname, force=True, options="v=0;", typ="FBX export", pr=False, es=True)
            else:
                back_fol = os.path.join(file_path, "bak").replace("\\","/")
                if(not os.path.exists(back_fol)):
                    self.mkdirp(back_fol)
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

    def checkcollapse(self, item=None):
        items = cmds.textScrollList("errlogs", q=1, ni=1)
        if items != 0:
            cmds.frameLayout("errlogsframe", e=1, cl=0)
            self.expandfl()
        else:
            cmds.frameLayout("errlogsframe", e=1, cl=1)
            self.collapefl()

    def selectitems(self, item=None):
        selected = cmds.textScrollList("errlogs", q=1, sut=1)
        tosel = []
        for ech in selected:
            if ech != '':
                tosel.append(ech)

        cmds.select(tosel)

    def collapefl(self, item=None):
        cmds.window('achkwin', e=1, widthHeight=(WIDTH, HEIGHT))

    def expandfl(self, item=None):
        cmds.window('achkwin', e=1, widthHeight=(WIDTH, HEIGHT+80))
