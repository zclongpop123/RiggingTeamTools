#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Thu, 14 Aug 2014 10:30:06
#========================================
import os.path, re
from FoleyUtils import scriptTool, uiTool, mayaTool
from PyQt4 import QtCore
import maya.cmds as mc
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class ListModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(ListModel, self).__init__(parent)
        self.__data = []
    
    def rowCount(self, index):
        return len(self.__data)
    
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__data[index.row()]
    
    def changeData(self, L):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, len(self.__data))
        self.__data = L
        self.endRemoveRows()


bodywndClass, bodybaseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'blendShapeWeights.ui'))
class BlendShapeWeightsUI(bodywndClass, bodybaseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'blendShapeWeightsToolUI'):
            return 
        
        super(BlendShapeWeightsUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #-
        self.__skinModel = ListModel()
        self.__bspModel  = ListModel()
        self.VIEW_skin.setModel(self.__skinModel)
        self.VIEW_bsp.setModel(self.__bspModel)



    def on_actionLoadSkinCluster_triggered(self, args=None):
        if args == None:return 
        selSkin = mc.ls(sl=True, type='skinCluster')
        if len(selSkin) < 1:
            return
        self.LET_skin.setText(selSkin[0])
        #-
        influcens = mc.skinCluster(selSkin[0], q=True, inf=True)
        self.__skinModel.changeData(influcens)




    def on_actionLoadBlendShape_triggered(self, args=None):
        if args == None:return 
        selBsp = mc.ls(sl=True, type='blendShape')
        if len(selBsp) < 1:
            return
        self.LET_bsp.setText(selBsp[0])
        #-
        attributes = mayaTool.getBlendShapeAttributes(selBsp[0])
        self.__bspModel.changeData(attributes)



    def on_btn_copyWeights_clicked(self, args=None):
        if args==None:return
        skinNode      = str(self.LET_skin.text())
        bspNode       = str(self.LET_bsp.text())
        influcenIndex = self.VIEW_skin.selectedIndexes()[0].row()
        bspAttribute  = self.VIEW_bsp.selectedIndexes()[0].row()
        
        skinGeo = mc.skinCluster(skinNode, q=True, g=True)[0]
        if mc.nodeType(skinGeo) != 'mesh':
            return
        
        VtxCounts = mc.polyEvaluate(skinGeo, v=True)
        self.progressBar.setMaximum(VtxCounts)  
        for i in range(VtxCounts):
            value = mc.skinPercent(skinNode, '%s.vtx[%d]'%(skinGeo, i), q=True, v=True)
            Skin_weight_value = value[influcenIndex]
            mc.setAttr('%s.it[0].itg[%d].tw[%d]'%(bspNode, bspAttribute, i), Skin_weight_value)
            self.progressBar.setValue(i)
        self.progressBar.setValue(0)

        
#-------------------------------------------------------------------------------------------------
    
    def on_CBX_weightValue_editingFinished(self):
        value = self.CBX_weightValue.value()
        self.SLD_weightValue.setValue(value * 1000)

        
    def on_SLD_weightValue_valueChanged(self, value):
        self.CBX_weightValue.setValue(value / 1000.0)
    
    
    def getId(self):
        ids = []
        for vtx in mc.ls(sl=True, fl=True):
            if not re.search('(?<=\[)\d+(?=\])', vtx):
                continue
            ids.append(int(re.search('(?<=\[)\d+(?=\])', vtx).group()))
        return ids
            
    
    def on_btn_addWeights_clicked(self, args=None):
        if args==None:return
        bspNode       = str(self.LET_bsp.text())
        bspAttribute  = self.VIEW_bsp.selectedIndexes()[0].row() 
        value = self.CBX_weightValue.value()
        for i in self.getId():
            ov = mc.getAttr('%s.it[0].itg[%d].tw[%d]'%(bspNode, bspAttribute, i))
            mc.setAttr('%s.it[0].itg[%d].tw[%d]'%(bspNode, bspAttribute, i), ov + value)
    
    
    def on_btn_minusWeights_clicked(self, args=None):
        if args==None:return
        bspNode       = str(self.LET_bsp.text())
        bspAttribute  = self.VIEW_bsp.selectedIndexes()[0].row() 
        value = self.CBX_weightValue.value()
        for i in self.getId():
            ov = mc.getAttr('%s.it[0].itg[%d].tw[%d]'%(bspNode, bspAttribute, i))
            mc.setAttr('%s.it[0].itg[%d].tw[%d]'%(bspNode, bspAttribute, i), ov - value)
        
    
    def on_btn_floodWeights_clicked(self, args=None):
        if args==None:return
        bspNode       = str(self.LET_bsp.text())
        bspAttribute  = self.VIEW_bsp.selectedIndexes()[0].row() 
        value = self.CBX_weightValue.value()
        for i in self.getId():
            mc.setAttr('%s.it[0].itg[%d].tw[%d]'%(bspNode, bspAttribute, i), value)