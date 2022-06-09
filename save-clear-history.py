from os.path import exists
import configparser
import maya.mel as mel
import maya.OpenMaya as om
import maya.cmds as cmds

# parses string values to be able to cast to booleans (True or False)
def truey(value, default=False):
    result = default
    if value.lower() in ['true', '1', 't', 'y', 'yes']:
        result = True
    elif value.lower() in ['false', '0', 'f', 'n', 'no']:
        result = False
    return result

# setup the parser to be able to read the config file
config = configparser.ConfigParser()
config.optionxform=str

# saveClearHistory install directory located with config.ini within
dir = cmds.internalVar(usd=True) + 'modules/saveClearHistory/config.ini'

# if the config.ini does not exist, create it with the default values
if not exists(dir):
    # default behaviour for plugin is to delete history AFTER save, to preserve history in saved files
    config['DEFAULT']['deleteAfterSave'] = 'true'
    with open(dir, 'w') as configfile:
        config.write(configfile)
        
# read the config file, and put clean data in relevant variables
config.read(dir)
delAfter = truey(config['DEFAULT']['deleteAfterSave'], True)

# callback function called upon save action in maya (see below for before or after save)
def handle_save(*args):
  # all non deformer history is deleted
  mel.eval("BakeAllNonDefHistory;")

# decides whether to setup callback for before or after save, based on config setting
if delAfter:
  message = om.MSceneMessage.kAfterSave
else:
  message = om.MSceneMessage.kBeforeSave

# create callback for the handle_save function with the appropriate callback trigger (message)
id = om.MSceneMessage.addCallback(message, handle_save)