#=============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 16 Jul 2014 10:31:46
#=============================================
import os.path
import maya.cmds as mc
from PyQt4 import QtCore, QtGui
from FoleyUtils import scriptTool, uiTool, mayaTool, mathTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class ListModel(QtCore.QAbstractListModel):
    def __init__(self, Listdata=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.__modelData = Listdata[:]

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.__modelData)


    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__modelData[index.row()]


    def clear(self):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount())
        del self.__modelData[:]
        self.endRemoveRows()
    
    def change(self, L=[]):
        self.beginInsertRows(QtCore.QModelIndex(), 0, self.rowCount())
        self.__modelData = L[:]
        self.endInsertRows()



windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'CopyBlendShapeWeights.ui'))
class CopyBlendShapeWeightsUI(windowClass, baseClass):
    def __init__(self, parent):
        if uiTool.windowExists(parent, 'CopyBlendShapeWeightUI'):
            return
        super(CopyBlendShapeWeightsUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #------------------
        iconPath = os.path.join(scriptTool.getScriptPath(), 'icons')
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(iconPath, 'refresh.png')))
        self.btn_refresh.setIcon(icon)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(iconPath, 'arrow.png')))
        self.btn_Copy.setIcon(icon)
        #-+-+-+-+-+-+-+-+-+
        self.__srcModel = ListModel()
        self.__dstModel = ListModel()
        
        self.listView_Src.setModel(self.__srcModel)
        self.listView_Dst.setModel(self.__dstModel)

    def on_actionLoad_src_triggered(self, args=None):
        if args == None:return
        selectBlendShapes = mc.ls(sl=True, type='blendShape')
        if not selectBlendShapes:
            return
        self.let_Src.setText(selectBlendShapes[0])
        self.refresh_Src()
        
    
    def on_actionLoad_dst_triggered(self, args=None):
        if args == None:return
        selectBlendShapes = mc.ls(sl=True, type='blendShape')
        if not selectBlendShapes:
            return
        self.let_Dst.setText(selectBlendShapes[0])
        self.refresh_Dst()
        
        
    def on_actionClear_triggered(self, args=None):
        if args == None:return
        self.let_Src.setText('')
        self.let_Dst.setText('')
        self.refresh_Src()
        self.refresh_Dst()
        
        
    def on_let_Src_editingFinished(self):
        self.refresh_Src()
        
        
    def on_let_Dst_editingFinished(self):
        self.refresh_Dst()
    
    
    
    def refresh_Src(self):
        self.__srcModel.clear()
        
        blendShape = str(self.let_Src.text())
        if not mc.objExists(blendShape):
            return
        if mc.nodeType(blendShape) != 'blendShape':
            return
        attributeList = mayaTool.getBlendShapeAttributes(blendShape)
        attributeList.insert(0, 'envelope')
        self.__srcModel.change(attributeList)
        
        
    def refresh_Dst(self):
        self.__dstModel.clear()
        
        blendShape = str(self.let_Dst.text())
        if not mc.objExists(blendShape):
            return
        if mc.nodeType(blendShape) != 'blendShape':
            return       
        attributeList = mayaTool.getBlendShapeAttributes(blendShape)
        attributeList.insert(0, 'envelope')
        self.__dstModel.change(attributeList)        
    
    
    def on_btn_refresh_clicked(self, clicked=None):
        if clicked == None:return
        self.refresh_Src()
        self.refresh_Dst()
        

    def on_btn_Copy_clicked(self, clicked=None):
        if clicked == None:return
        src_bs = str(self.let_Src.text())
        dst_bs = str(self.let_Dst.text())
        src_index = self.listView_Src.selectedIndexes() or None
        dst_index = self.listView_Dst.selectedIndexes() or None
        
        #- blendShape exists ?
        if not mc.objExists(src_bs):
            return
        
        if not mc.objExists(dst_bs):
            return
        
        #- is blendShape ?
        if mc.nodeType(src_bs) != 'blendShape':
            return
        
        if mc.nodeType(dst_bs) != 'blendShape':
            return
        
        #- index has selected?
        if src_index is None:
            return
        else:
            src_index = src_index[0].row()
        
        
        if dst_index is None:
            return
        else:
            dst_index = dst_index[0].row()
        
        #- is one blendShape and one attr?
        if src_bs == dst_bs and src_index == dst_index:
            return
        
        
        Vtxes = mc.polyEvaluate(mc.blendShape(src_bs, q=True, g=True), v=True)
        self.progressBar.setMaximum(Vtxes)
        
        
        for i in range(Vtxes):
            #-
            if src_index == 0:
                value = mc.getAttr('%s.it[0].bw[%d]'%(src_bs, i))
            else:
                value = mc.getAttr('%s.it[0].itg[%d].tw[%d]'%(src_bs, src_index-1, i))
            
            #-
            if dst_index == 0:
                mc.setAttr('%s.it[0].bw[%d]'%(dst_bs, i), value)
            else:
                mc.setAttr('%s.it[0].itg[%d].tw[%d]'%(dst_bs, dst_index-1, i), value)
            
            
            self.progressBar.setValue(i)
            self.progressLabel.setText('%d%%'%mathTool.setRange(0, Vtxes, 0, 100, i))
        
        #- reset UI
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(0)
        self.progressLabel.setText('0%')