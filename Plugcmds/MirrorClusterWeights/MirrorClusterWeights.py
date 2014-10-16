#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Thu, 16 Oct 2014 10:31:59
#========================================
import os.path
from FoleyUtils import scriptTool, uiTool
import maya.cmds as mc
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
baseClass, windowClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'clusterWeightsUI.ui'))
class ClusterWeightsUI(baseClass, windowClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'MirrorClusterWindow'):
            return             
        super(ClusterWeightsUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
        
        
    def on_btn_Geometry_clicked(self, args=None):
        if args == None:return
        sel = mc.ls(sl=True)
        if len(sel) < 1:return
        if not mc.listRelatives(sel[0], s=True, type='mesh'):return
        self.let_Geometry.setText(sel[0])
    
    
    def on_btn_Source_clicked(self, args=None):
        if args == None:return
        sel = mc.ls(sl=True)
        if len(sel) < 1:return
        if mc.nodeType(sel[0]) == 'cluster':
            self.let_Source.setText(sel[0])
        elif mc.listRelatives(sel[0], s=True, type='clusterHandle'):
            self.let_Source.setText(mc.listConnections(sel[0])[0])
        else:
            return
    
    
    def on_btn_Targent_clicked(self, args=None):
        if args == None:return
        sel = mc.ls(sl=True)
        if len(sel) < 1:return
        if mc.nodeType(sel[0]) == 'cluster':
            self.let_Targent.setText(sel[0])
        elif mc.listRelatives(sel[0], s=True, type='clusterHandle'):
            self.let_Targent.setText(mc.listConnections(sel[0])[0])
        else:
            return
    
    def on_btn_Mirror_clicked(self, args=None):
        if args == None:return
        geo = str(self.let_Geometry.text())
        src = str(self.let_Source.text())
        dst = str(self.let_Targent.text())
        
        if not mc.objExists(geo):
            return
        if not mc.objExists(src):
            return
        if not mc.objExists(dst):
            return
        
        infoNode = mc.createNode('closestPointOnMesh')
        shape = mc.listRelatives(geo, s=True, path=True, type='mesh')[0]
        mc.connectAttr('%s.outMesh'%shape, '%s.inMesh'%infoNode)
        
        srcWeightListIndex = mc.listRelatives(mc.cluster(src, q=True, g=True), p=True, path=True).index(geo)
        dstWeightListIndex = mc.listRelatives(mc.cluster(dst, q=True, g=True), p=True, path=True).index(geo)
        
        vtxCounts = len(mc.ls('%s.vtx[*]'%geo, fl=True))
        srcValues = mc.getAttr('%s.wl[%d].w[:%d]'%(src, srcWeightListIndex, vtxCounts-1))
        dstValues = []
        
        self.progressBar.setMaximum(vtxCounts)
        for i, vtx in enumerate(mc.ls('%s.vtx[*]'%geo, fl=True)):
            postions = mc.xform(vtx, q=True, ws=True, t=True)
        
            mc.setAttr('%s.ipx'%infoNode, postions[0] * -1)
            mc.setAttr('%s.ipy'%infoNode, postions[1] *  1)
            mc.setAttr('%s.ipz'%infoNode, postions[2] *  1)

            dstValues.append(srcValues[mc.getAttr('%s.vt'%infoNode)])
            #-
            self.progressBar.setValue(i)

        mc.setAttr('%s.wl[%d].w[:%d]'%(dst, dstWeightListIndex, len(dstValues)-1), *dstValues)
        mc.delete(infoNode)
        #-
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(0)