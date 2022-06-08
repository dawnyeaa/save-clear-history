import maya.mel as mel
import maya.OpenMaya as om

def handle_save(*args):
  mel.eval("BakeAllNonDefHistory;")

id = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterSave, handle_save)