import maya.cmds as cmds
import maya.OpenMaya as om

def handle_save(*args):
  cmds.delete(all=True, constructionHistory=True)

id = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterSave, handle_save)