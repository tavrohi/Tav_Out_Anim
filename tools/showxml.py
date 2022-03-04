import xml.etree.ElementTree as ET
import pymel.core as pm
import os

curr_path = os.path.dirname(__file__)
actual_path = os.path.join(curr_path,"show_setup","show.xml")
tree = ET.parse(actual_path)
root = tree.getroot()

def showcode():
    showname_f = pm.sceneName()
    buffer = showname_f.split("/")
    buffer1 = buffer[-1].split("_")
    showcode = buffer1[0]
    return showcode

def findpath():
    sc = showcode()
    dir_path = ""
    for show in root.findall('show'):
        code = show.find('code').text
        path = show.find('dir').text
        if code.lower() == sc.lower():
            dir_path = path
    return dir_path
    
def findxlpath():
    sc = showcode()
    dir_path = ""
    for show in root.findall('show'):
        code = show.find('code').text
        path = show.find('xlpath').text
        if code.lower() == sc.lower():
            dir_path = path
    return dir_path
    
def findname(sc = None):
    if sc == None:
        sc = showcode()
    dir_path = ""
    for show in root.findall('show'):
        code = show.find('code').text
        path = show.attrib
        if code.lower() == sc.lower():
            dir_path = path
    return dir_path
    
def findallcode():
    all_codes = []
    for show in root.findall('show'):
        code = show.find('code').text
        all_codes.append(code)
        
    return all_codes
    
def findmci(sc = None):
    if sc == None:
        sc = showcode()
    dir_path = ""
    for show in root.findall('show'):
        code = show.find('code').text
        path = show.find('cutid').text
        if code.lower() == sc.lower():
            dir_path = path
    return dir_path
    
def findfolderpath(sc=None):
    if sc == None:
        sc = showcode()
    dir_path = ""
    for show in root.findall('show'):
        code = show.find('code').text
        path = show.find('dir').text
        if code.lower() == sc.lower():
            dir_path = path
    return dir_path
    
def findfps(sc=None):
    if sc == None:
        sc = showcode()
    dir_path = ""
    for show in root.findall('show'):
        code = show.find('code').text
        path = show.find('fps').text
        if code.lower() == sc.lower():
            dir_path = path
    return dir_path

def findres(sc=None):
    if sc == None:
        sc = showcode()
    res = []
    for show in root.findall('show'):
        code = show.find('code').text
        resh = show.find('resheight').text
        resw = show.find('reswidth').text
        if code.lower() == sc.lower():
            res = [resh, resw]
    return res