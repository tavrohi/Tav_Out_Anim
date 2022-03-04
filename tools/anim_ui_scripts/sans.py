import re, os
import tools.showxml as xm
import maya.cmds as cmds
import pymel.core as pm

def check_unwanted_camera():
    no_of_camera = cmds.listCameras(p=True)
    unwanted_cam = []
    for default_camera in ['persp']:
        no_of_camera.remove(default_camera)
    for cam in no_of_camera:
        if not cmds.reference(cam, q=True, inr=True):
            unwanted_cam.append(cam)
    if len(unwanted_cam) > 1:
        cmds.textScrollList("errlogs", e=1, append="Unwanted Camera in scene:")
        for ech in unwanted_cam:
            cmds.textScrollList("errlogs", e=1, append=("\t"+ech), utg=ech)
        return unwanted_cam
    return False
    
def check_imported_mesh_objects():
    imported_mesh_obj = []
    all_transform_mesh = cmds.ls(type='mesh', l=True)
    for each in all_transform_mesh:
        if not cmds.referenceQuery(each, inr=True) and not re.search('persp|side|top|front', each, re.I):
            if each.startswith('|FX') or each.startswith('FX'):
                continue
            if each not in imported_mesh_obj:
                imported_mesh_obj.append(each)
    if imported_mesh_obj:
        cmds.textScrollList("errlogs", e=1, append="Imported Mesh in scene:")
        for ech in imported_mesh_obj:
            cmds.textScrollList("errlogs", e=1, append=("\t"+ech), utg=ech)
        return imported_mesh_obj
    return False
    
def check_name_spaces():
    name_space_list = cmds.namespaceInfo(listOnlyNamespaces=True)
    name_space_list.remove('UI')
    name_space_list.remove('shared')
    for each_ref in cmds.file(q=True, r=True):
        file_name_space = cmds.file(each_ref, q=True, ns=True)
        if file_name_space in name_space_list:
            name_space_list.remove(file_name_space)
    if name_space_list:
        cmds.textScrollList("errlogs", e=1, append="Namespace:")
        for ech in name_space_list:
            cmds.textScrollList("errlogs", e=1, append=("\t"+ech))
        return name_space_list
    else:
        return False
    
def check_reference_asset_path(code, episode):
    folderpth = xm.findfolderpath(code)
    if(folderpth == ""):
        return True
    
    beginfol = os.path.join(folderpth, "02_library", "01_asset", "02_rig").replace("\\", "/")
    asseteppath = os.path.join(beginfol, "02_prp" , episode).replace("\\", "/")
    
    for each_ref in cmds.file(r=True, q=True):
        ### path checker from proper Drive
        if each_ref.startswith(beginfol):
            pass
        else:
            cmds.textScrollList("errlogs", e=1, append=("Wrong Reference Path: "+each_ref))
            return True
        
        ### path checker prop from proper episode
        if "02_prp" in each_ref and ("bb_p_vehicle" not in each_ref and "bag_vehicle" not in each_ref):
            if each_ref.startswith(asseteppath):
                pass
            else:
                cmds.textScrollList("errlogs", e=1, append=("Reference Path from difference episode: "+each_ref))
                return True
        
    return False
    
def check_lights():
    lights_list = cmds.ls(lights=True)
    unwanted_lights = []
    for each_light in lights_list:
        if not cmds.referenceQuery(each_light, inr=True):
            unwanted_lights.append(each_light)

    if unwanted_lights:
        cmds.textScrollList("errlogs", e=1, append="Unwanted Lights:")
        for ech in unwanted_lights:
            cmds.textScrollList("errlogs", e=1, append=("\t"+ech), utg=ech)
        return unwanted_lights
    else:
        return False
    
def check_time_unit(code):
    time_unit = cmds.currentUnit(t=True, q=True)
    reload(xm)
    fps = xm.findfps(code)
    if str(time_unit) == str(fps):
        return False

    cmds.textScrollList("errlogs", e=1, append=("Wrong FPS: Current " + str(time_unit) + " | Expected " + str(fps)))
    return True
    
def check_maya_cut_id(code):
    maya_cut_id = cmds.about(c=True, q=True)
    env_cut_id = xm.findmci(code)
    if maya_cut_id != env_cut_id:
        cmds.textScrollList("errlogs", e=1, append=("Wrong Maya Version: Current " + str(maya_cut_id) + " | Expected " + str(env_cut_id)))
        return True
    return False
    
def check_display_layer():
    unwanted_display_layer = []
    for display_layer in cmds.ls(type='displayLayer'):
        if cmds.referenceQuery(display_layer, inr=True):
            continue
        if 'defaultLayer' not in display_layer and 'hide' not in display_layer:
            if not cmds.getAttr("%s.visibility" % display_layer):
                unwanted_display_layer.append(display_layer)
    if unwanted_display_layer:
        cmds.textScrollList("errlogs", e=1, append="Display Layer are off:")
        for ech in unwanted_display_layer:
            cmds.textScrollList("errlogs", e=1, append=("\t"+ech))
        return unwanted_display_layer
    return False
    
def check_render_layer():
    unwanted_render_layer = []
    for each_render_layer in cmds.ls(type='renderLayer'):
        if re.search(r'defaultRenderLayer', each_render_layer, re.I):
            continue
        unwanted_render_layer.append(each_render_layer)

    if unwanted_render_layer:
        cmds.textScrollList("errlogs", e=1, append="Unwanted Render Layers:")
        for ech in unwanted_render_layer:
            cmds.textScrollList("errlogs", e=1, append=("\t"+ech))
        return unwanted_render_layer
    return False
    
def check_anim_layer():
    animlays = cmds.ls(type='animLayer')
    if len(animlays) > 1:
        cmds.textScrollList("errlogs", e=1, append="Unwanted Anim Layers:")
        for ech in animlays:
            if ech != "BaseAnimation":
                cmds.textScrollList("errlogs", e=1, append=("\t"+ech))
        return True
    return False
    
def check_audio():
    if len(cmds.ls(type='audio')) != 0:
        return False
    else:
        return True
    
def check_minus_frame_range():
    ast_value = cmds.playbackOptions(q=True, ast=True)
    min_value = cmds.playbackOptions(q=True, min=True)
    if min_value < 1 or ast_value < 1:
        return True
    return False
    
def check_101_frame_range():
    ast_value = cmds.playbackOptions(q=True, ast=True)
    min_value = cmds.playbackOptions(q=True, min=True)
    if min_value < 101:
        cmds.textScrollList("errlogs", e=1, append="Frame doesn't starts from 101")
        return True
    return False
    
def check_proper_camera():
    all_c = cmds.ls(type = "camera", l=1)
    e=1
    for each in all_c:
        x = each.split("|")
        if x[1] == "render_cam" and len(x) == 3:
            if x[2] != "render_camShape":
                cmds.rename(each, 'render_camShape')
            e=0

    if e:
        cmds.textScrollList("errlogs", e=1, append="render_cam unavailable")

    return e