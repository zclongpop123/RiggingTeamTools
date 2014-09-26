#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 22 Sep 2014 10:35:13
#========================================
import os.path
import maya.cmds as mc
import maya.mel as mel
from FoleyUtils import scriptTool, uiTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

bodywndClass, bodybaseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'transWeights.ui'))
class transWeightsUI(bodywndClass, bodybaseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'transSkeletonToClusters'):
            return 
        
        super(transWeightsUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
    
    def on_btn_LoadGeometry_clicked(self, clicked=None):
        if clicked == None:return
        sel = mc.ls(sl=True)
        if len(sel) < 1:
            return
        
        self.LET_Geometry.setText(sel[0])
    
    
    def on_btn_LoadSkeleton_clicked(self, clicked=None):
        if clicked == None:return   
        sel = mc.ls(sl=True, type='joint')
        if len(sel) > 0:
            self.LET_Skeleton.setText(', '.join(sel))
        else:
            geometry = str(self.LET_Geometry.text())
            if not mc.objExists(geometry):
                return
            skinNode = mel.eval('findRelatedSkinCluster ' + geometry)
            if not mc.objExists(skinNode):
                self.LET_Skeleton.setText('')
                return
            bindJoints = mc.skinCluster(skinNode, q=True, inf=True)
            self.LET_Skeleton.setText(', '.join(bindJoints))
    
    
    def on_btn_Start_clicked(self, clicked=None):
        if clicked == None:return  
        geometry = str(self.LET_Geometry.text())
        joints   = [jnt.strip() for jnt in str(self.LET_Skeleton.text()).split(',')]
        joints   = [jnt for jnt in joints if mc.objExists(jnt)]
    
    
        self.progressBar_A.setMaximum(len(joints))
        self.progressLabel_A.setText('0/%d'%len(joints))
        
        for i, jnt in enumerate(joints):
            #- create cluster
            cluster = mc.cluster(geometry, rel=True)
            
            #- copy weights
            res = transSkinWeightsToCluster(geometry, geometry, jnt, cluster[0], self.progressBar_B, self.progressLabel_B)
            
            if res:
                #- weight Node
                mc.cluster(cluster[0], e=True, wn=(jnt, jnt))
            
                #- delete handle
                mc.delete(cluster[1])
            
            #- progerss
            self.progressBar_A.setValue(i+1)    
            self.progressLabel_A.setText('%d/%d'%(i+1, len(joints)))
            
        self.progressBar_A.setValue(0) 
        self.progressBar_A.setMaximum(1)    
        self.progressLabel_A.setText('0/0')



def transSkinWeightsToCluster(skinGeometry, clusterGeometry, joint, cluster, progressBar=None, progressLabel=None):
    #- get the cluster Node Name..
    if mc.nodeType(cluster) == 'transform':
        cluster = mc.listConnections(cluster, t='cluster')[0]
    else:
        pass    

    #- get SkinNode Name
    skinNode = mel.eval('findRelatedSkinCluster ' + skinGeometry)

    #- set Value
    vtxCount   = mc.polyEvaluate(skinGeometry, v=True)
    try:
        jointIndex = mc.skinCluster(skinNode, q=True, inf=True).index(joint)
    except ValueError:
        mc.delete(cluster)
        return False
    
    #- progress
    if progressBar != None:
        progressBar.setMaximum(vtxCount)
    if progressLabel != None:
        progressLabel.setText('0/%d'%vtxCount)
    
    weights = list()
    for i in range(vtxCount):
        weights.append(mc.skinPercent(skinNode, '%s.vtx[%s]'%(skinGeometry, i), q=True, v=True)[jointIndex])
        #- progress
        if progressBar != None:
            progressBar.setValue(i)        
        if progressLabel != None:
            progressLabel.setText('%d/%d'%(i, vtxCount))
    
    mc.setAttr('%s.wl[0].w[0:%d]'%(cluster, vtxCount-1), *weights)
    
    #- progress
    if progressBar != None:
        progressBar.setValue(0) 
        progressBar.setMaximum(1)
    if progressLabel != None:
        progressLabel.setText('0/0')  
    
    return True