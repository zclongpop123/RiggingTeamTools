#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 16 Jul 2014 09:31:17
#=============================================
import os.path
import maya.cmds as mc
import maya.mel as mel
from FoleyUtils import scriptTool, uiTool, mayaTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'blendShapeWeights.ui'))
class BlendShapeWeightUI(windowClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'blendShapeWeightsTool'):return
        super(BlendShapeWeightUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
    
    
    def on_btn_mirrorE_clicked(self, clicked=None):
        if clicked == None:return
        doMirrorBlendShapeWeights(envelope=True)
        
        
    def on_btn_mirrorT_clicked(self, clicked=None):
        if clicked == None:return
        doMirrorBlendShapeWeights(envelope=False)
    
    
    def on_btn_inverE_clicked(self, clicked=None):
        if clicked == None:return
        doInvertBlendShapeWeights(envelope=True)
    
    
    def on_btn_inverT_clicked(self, clicked=None):
        if clicked == None:return
        doInvertBlendShapeWeights(envelope=False)






def invertBlendShapeWeights(model, blendShape, envelope=True):
    #- get vetx
    VtxCounts = mc.polyEvaluate(model, v=True)
    
    # Start the progress bar.
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
    mc.progressBar(gMainProgressBar, e=True, bp=True, ii=True, st='Applying weights to %s' % model, max=VtxCounts)
    
    for i in range(VtxCounts):
        #  Increase the progress bar.
        if mc.progressBar(gMainProgressBar, q=True, ic=True): break
        mc.progressBar(gMainProgressBar, e=True, s=1)    
        
        #- get Value, set Value
        if envelope:
            value = mc.getAttr('%s.it[0].baseWeights[%d]'%(blendShape, i))
            mc.setAttr('%s.it[0].baseWeights[%d]'%(blendShape, i), 1 - value)
        
        else:
            for ID in mayaTool.getActiveTargets(blendShape): #- if attrbute seted..
                value = mc.getAttr('%s.it[0].itg[%d].tw[%d]'%(blendShape, ID, i))
                mc.setAttr('%s.it[0].itg[%d].tw[%d]'%(blendShape, ID, i), 1 - value)


    # Stop the progress bar.
    mc.progressBar(gMainProgressBar, e=True, ep=True)

        
        
        
    
def mirrorBlendShapeWeights(model, blendShape, envelope=True):
    #- get vetx
    VtxCounts = mc.polyEvaluate(model, v=True)
    #- create Info node
    InfoNode = mc.createNode('closestPointOnMesh')
    #- connect
    mc.connectAttr('%s.outMesh'%mc.listRelatives(model, s=True, path=True)[0], '%s.inMesh'%InfoNode)
    
    # Start the progress bar.
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
    mc.progressBar(gMainProgressBar, e=True, bp=True, ii=True, st='Applying weights to %s' % model, max=VtxCounts)
    
    for i in range(VtxCounts):
        #  Increase the progress bar.
        if mc.progressBar(gMainProgressBar, q=True, ic=True): break
        mc.progressBar(gMainProgressBar, e=True, s=1)    
        
        #- get vtx positions
        posi = mc.xform('%s.vtx[%d]'%(model, i), q=True, t=True)
        if posi[0] < 0:
            continue
        #- set Info node attributes
        mc.setAttr('%s.ip'%InfoNode, posi[0] * -1, *posi[1:])
        
        #- get mirrord vtx ID
        mrID = mc.getAttr('%s.vt'%InfoNode)
        
        #- get Value, set Value
        if envelope:
            value = mc.getAttr('%s.it[0].baseWeights[%d]'%(blendShape, i))
            mc.setAttr('%s.it[0].baseWeights[%d]'%(blendShape, mrID), value)
        
        else:
            for ID in mayaTool.getActiveTargets(blendShape): #- if attrbute seted..2382
                value = mc.getAttr('%s.it[0].itg[%d].tw[%d]'%(blendShape, ID, i))
                mc.setAttr('%s.it[0].itg[%d].tw[%d]'%(blendShape, ID, mrID), value)

    # Stop the progress bar.
    mc.progressBar(gMainProgressBar, e=True, ep=True)
    mc.delete(InfoNode)
    
        
    
@mayaTool.undo_decorator    
def doMirrorBlendShapeWeights(envelope=True):
    selOBJ = mc.ls(sl=True)
    if len(selOBJ) == 0:return
    
    blendShapes = mayaTool.getHistoryByType(selOBJ[0], 'blendShape')
    
    if len(blendShapes) == 0:return 
    
    for bs in  blendShapes :
        mirrorBlendShapeWeights(selOBJ[0], bs, envelope)

    
    
@mayaTool.undo_decorator    
def doInvertBlendShapeWeights(envelope=True):
    selOBJ = mc.ls(sl=True)
    if len(selOBJ) == 0:return
    
    blendShapes = mayaTool.getHistoryByType(selOBJ[0], 'blendShape')
    
    if len(blendShapes) == 0:return 
    
    for bs in  blendShapes :
        invertBlendShapeWeights(selOBJ[0], bs, envelope)