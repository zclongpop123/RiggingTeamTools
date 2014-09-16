#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 15 Sep 2014 16:26:30
#========================================
import os, re, math
from PyQt4 import QtCore, QtGui, uic
import maya.cmds as mc
from FoleyUtils import scriptTool, uiTool, mayaTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def getDrivenKeyInfo(obj):
    DrivenInfo = []
    attributes = mc.setDrivenKeyframe(obj, q=True, dn=True)
    if re.match('^No driven attributes', attributes[0]):
        return DrivenInfo
    
    for attr in attributes:
        DrivenInfo.append((mc.setDrivenKeyframe(attr, q=True, dr=True), attr))
        
    return DrivenInfo




def copyDrivenKeys(src, dsr, dsn, mirror=1):
    for arg in (src, dsr, dsn):
        obj, attribute = arg.split('.', 1)
        if not mc.objExists(obj):
            print 'Error -> obj  %s  was not Exists...'%obj
            return
        if not mc.attributeQuery(attribute, n=obj, ex=True):
            print 'Error -> attributes  %s  was not Exists...'%arg
            return
    
    mc.delete(mc.keyframe(dsn, q=True, n=True))
    
    driverValues = mc.keyframe(src, q=True, fc=True)
    drivenValues = mc.keyframe(src, q=True, vc=True)
    for drv, dnv in zip(driverValues, drivenValues):
        mc.setDrivenKeyframe(dsn, cd=dsr, dv=drv, v=dnv * mirror)
    
    

    
windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'mirrorDrivenKeys.ui'))
class MirrorDrivenKeysUI(windowClass, baseClass):

    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'mirrorDrivenkeysWindow'):
            return
        
        super(MirrorDrivenKeysUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #----------------------------------------------------------------
        self.__SrcOBJ = None
        self.__DstOBJ = None
        
        self.__model_SrcDriver = ListModel()
        self.__model_SrcDriven = ListModel()
        self.__model_DstDriver = ListModel()
        self.__model_DstDriven = ListModel()
        #->
        self.ListView_SrcDriver.setModel(self.__model_SrcDriver)
        self.ListView_SrcDriven.setModel(self.__model_SrcDriven)
        self.ListView_DstDriver.setModel(self.__model_DstDriver)
        self.ListView_DstDriven.setModel(self.__model_DstDriven)
        #----------------------------------------------------------------
        
    def on_ListView_SrcDriver_pressed(self, index):
        self.__refreshView(self.ListView_SrcDriver, index, self.ListView_SrcDriver.verticalScrollBar())
        
    def on_ListView_SrcDriven_pressed(self, index):
        self.__refreshView(self.ListView_SrcDriven, index, self.ListView_SrcDriven.verticalScrollBar())
        
    def on_ListView_DstDriver_pressed(self, index):
        self.__refreshView(self.ListView_DstDriver, index, self.ListView_DstDriver.verticalScrollBar())
        
    def on_ListView_DstDriven_pressed(self, index):
        self.__refreshView(self.ListView_DstDriven, index, self.ListView_DstDriven.verticalScrollBar())
        
    
    def __refreshView(self, view, index, scroll):
        views = (self.ListView_SrcDriver,
                 self.ListView_SrcDriven,
                 self.ListView_DstDriver,
                 self.ListView_DstDriven)
        
        for v in views:
            if v == view:continue
            v.setCurrentIndex(index)
            
            vScroll = v.verticalScrollBar()
            
            Value    = float(scroll.value())
            OldMax   = scroll.maximum()
            OldMin   = max(scroll.minimum(), 1)
            Max      = vScroll.maximum()
            Min      = vScroll.minimum()
            OutValue = math.ceil(Min + (((Value-OldMin)/(OldMax-OldMin)) * (Max-Min)))
            
            vScroll.setValue(OutValue)
    
    
    
    def on_actionLoad_Src_triggered(self, args=None):
        if args == None:return
        self.__model_SrcDriver.clear()
        self.__model_SrcDriven.clear()     
        #-----------------------------
        sel = mc.ls(sl=True)
        if len(sel) == 0:return
        self.__SrcOBJ = sel[0]
        self.LET_SrcOBJ.setText(self.__SrcOBJ)
        #-----------------------------
        for driver, driven in getDrivenKeyInfo(self.__SrcOBJ):
            if len(driver) > 1:continue
            self.__model_SrcDriver.insertRow(driver[0])
            self.__model_SrcDriven.insertRow(driven)



    def on_actionLoad_Dst_triggered(self, args=None):
        if args == None:return
        self.__model_DstDriver.clear()
        self.__model_DstDriven.clear()
        #-----------------------------
        sel = mc.ls(sl=True)
        if len(sel) == 0:return
        self.__DstOBJ = sel[0]
        self.LET_DstOBJ.setText(self.__DstOBJ)
        #-----------------------------
        for driver, driven in getDrivenKeyInfo(self.__SrcOBJ):
            if len(driver) > 1:continue
            self.__model_DstDriver.insertRow(driver[0])
            self.__model_DstDriven.insertRow(driven.replace(self.__SrcOBJ, self.__DstOBJ))



    def on_actionDelete_Item_triggered(self, args=None):
        if args==None:return
        CurrentView = None
        for c in self.findChildren(QtGui.QListView):
            if c.hasFocus():
                CurrentView = c
                break
        if CurrentView == None:return
        
        selectIndexs = [index.row() for index in CurrentView.selectedIndexes()]
        selectIndexs.sort()
        selectIndexs.reverse()
        
        for index in selectIndexs:
            self.__model_SrcDriven.removeRow(index)
            self.__model_SrcDriver.removeRow(index)
            
            self.__model_DstDriven.removeRow(index)
            self.__model_DstDriver.removeRow(index)



    def on_LET_DriverInputA_editingFinished(self):
        self.changeData(self.__model_DstDriver, str(self.LET_DriverInputA.text()), str(self.LET_DriverInputB.text()))
    
    
    def on_LET_DriverInputB_editingFinished(self):
        self.changeData(self.__model_DstDriver, str(self.LET_DriverInputA.text()), str(self.LET_DriverInputB.text()))
    
    
    def on_LET_DrivenInputA_editingFinished(self):
        self.changeData(self.__model_DstDriven, str(self.LET_DrivenInputA.text()), str(self.LET_DrivenInputB.text()))
    
    
    def on_LET_DrivenInputB_editingFinished(self):
        self.changeData(self.__model_DstDriven, str(self.LET_DrivenInputA.text()), str(self.LET_DrivenInputB.text()))


    def changeData(self, model, textA, textB):
        for i, d in enumerate(model.baseDatas()):
            value = d.replace(textA, textB)
            model.setData(model.index(i, 0), QtCore.QVariant(value), QtCore.Qt.EditRole)
       

    @mayaTool.undo_decorator
    def on_btn_SetKeys_clicked(self, args=None):
        if args==None:return
        for src, dsr, dsn in zip(self.__model_SrcDriven.datas(), self.__model_DstDriver.datas(), self.__model_DstDriven.datas()):
            if src == dsn:
                continue
            
            if self.rdn_Copy.isChecked():
                copyDrivenKeys(src, dsr, dsn)
            elif self.rdn_Mirror.isChecked():
                copyDrivenKeys(src, dsr, dsn, -1)
            else:
                if re.search('(translateX|rotateZ)$', dsr):
                    copyDrivenKeys(src, dsr, dsn, -1)
                else:
                    copyDrivenKeys(src, dsr, dsn,  1)



class ListModel(QtCore.QAbstractListModel):
    def __init__(self, L=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.__Base = L[:]
        self.__List = L[:]
        
    
    def rowCount(self, index):
        return len(self.__List)
    
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.__List[index.row()]
        
        if role == QtCore.Qt.TextColorRole:
            if self.__List[index.row()] != self.__Base[index.row()]: 
                return QtGui.QBrush(QtGui.QColor(222, 114, 122))    
   
    def datas(self):
        return self.__List
   
   
    def baseDatas(self):
        return self.__Base
    

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
    

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            self.__List[index.row()] = str(value.toString())
            
            self.dataChanged.emit(index, index)
            return True
        

    def insertRow(self, value='0'):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.__List), len(self.__List))
        self.__Base.append(value)
        self.__List.append(value)
        self.endInsertRows()
    
    
    def removeRow(self, row):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        self.__Base.pop(row)
        self.__List.pop(row)
        self.endRemoveRows()
    
    
    def clear(self):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, len(self.__List))
        del self.__Base[:]
        del self.__List[:]
        self.endRemoveRows()
        