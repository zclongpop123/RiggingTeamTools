#=================================
# author: changlong.zang
#   date: 2014-04-18
#=================================
import os, re
from PyQt4 import QtCore, QtGui
import maya.cmds as mc
import maya.mel as mel
from FoleyUtils import scriptTool, uiTool, mayaTool, nameTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class ListModel(QtCore.QAbstractListModel):
    '''
    List model for files, display & edit..
    '''
    def __init__(self, fileList=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.__baseList = fileList[:]
        self.__fileList = fileList[:]


    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.__fileList)


    def data(self, index, role):
        #- file names
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.__fileList[index.row()]
        
        #- text color
        if role == QtCore.Qt.ForegroundRole:
            if self.__fileList.count(self.__fileList[index.row()]) > 1:
                return QtGui.QColor(255,   0,   0)
            
            if self.__fileList[index.row()] != self.__baseList[index.row()]:
                return QtGui.QColor(255, 170, 127)
        
        #- text Tip
        if role == QtCore.Qt.ToolTipRole:
            return self.__baseList[index.row()]
            
            
    def flags(self, index):
        #- what you can do it
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
    
    
    def setData(self, index, value, role):
        #- user seted value
        if role == QtCore.Qt.EditRole:
            if isinstance(value, basestring):
                self.__fileList[index.row()] = '%s'%value
            else:
                self.__fileList[index.row()] = '%s'%value.toString()
        self.dataChanged.emit(index, index)
        return True


    def insertRow(self, row, value, index=QtCore.QModelIndex()):
        self.beginInsertRows(index, row, row)
        self.__fileList.insert(row, value)
        self.__baseList.insert(row, value)
        self.endInsertRows()

    
    
    def clear(self):
        '''
        clear model datas for empoty view...
        '''
        self.beginRemoveColumns(QtCore.QModelIndex(), 0, self.rowCount())
        del self.__baseList[:]
        del self.__fileList[:]
        self.endRemoveRows()



    def getValue(self, row):
        return self.__baseList[row]
    


    def result(self):
        return self.__baseList, self.__fileList


#-------------------------------------------------------------------------------------

windowClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'nameToolUI.ui'))
class NameUI(windowClass, baseClass):
    '''
    user control pannel...
    '''
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'foleyNameToolWindow'):
            return 
        
        super(NameUI, self).__init__(parent)
        self.setupUi(self)
        #----------------------------------------------------
        #- hide control
        self.widget_windows.setVisible(False)
        
        #- setModel
        self.__listModel = ListModel()
        self.listView.setModel(self.__listModel)
        #----------------------------------------------------
        self.show()
        #-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        self.__textIndex    = 0
        self.__textMaxIndex = 0
        self.on_actionUiVisibleSwitch_triggered(True)
        #-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


    def on_rdn_maya_clicked(self, args=None):
        if args == None:return
        self.__listModel.clear()


    def on_rdn_windows_clicked(self, args=None):
        if args == None:return
        self.__listModel.clear()


    def on_btn_setpath_clicked(self, args=None):
        if args == None:return
        #- select dir
        dirPath = mc.fileDialog2(fm=3, okc="Select")
        if not dirPath:return
        
        #- read first one dir
        dirPath = dirPath[0]
        if not os.path.isdir(dirPath):return
        
        #- setText
        self.LET_path.setText(dirPath)



    def on_LET_path_textChanged(self, dirPath):
        #- refresh List
        self.on_btn_refresh_clicked(True)



    def on_btn_SelectHierarchy_clicked(self, args=None):
        if args == None:return
        mel.eval('SelectHierarchy;')



    def on_btn_loadObjects_clicked(self, args=None):
        if args == None:return
        #- clear List
        self.__listModel.clear()
        objects = mc.ls(sl=True)
    
        #- add Files
        for i, obj in enumerate(objects):
            self.__listModel.insertRow(i, obj)
            self.__textMaxIndex = max(self.__textMaxIndex, len(obj))      




    def __setNameData(self):
        searchText = str(self.LET_inputA.text())
        for i in range(self.__listModel.rowCount()):
            orignalText = self.__listModel.getValue(i)
            #- prefix
            if self.rdn_pre.isChecked():
                resultText = '%s%s%s'%(orignalText[:self.__textIndex],  searchText, orignalText[self.__textIndex:])
           
            #- defind format
            elif self.rdn_def.isChecked():
                resultText  = nameTool.SerializationObjectNames(self.__listModel.result()[0], searchText, 1)[i]
           
            #- search replace
            else:
                replaceText = str(self.LET_inputB.text())
                resultText  = orignalText.replace(searchText, replaceText)
            
            #- set Model data
            self.__listModel.setData(self.__listModel.index(i, 0), resultText, QtCore.Qt.EditRole)



    def on_actionUiVisibleSwitch_triggered(self, args=None):
        if args == None:return
        if self.rdn_pre.isChecked():
            self.widget_buttonBox.setVisible(True)
            self.lab_Ps.setVisible(False)
            self.LET_inputB.setVisible(False)
        elif self.rdn_def.isChecked():
            self.widget_buttonBox.setVisible(False)
            self.lab_Ps.setVisible(True)
            self.LET_inputB.setVisible(False)
        else:   
            self.widget_buttonBox.setVisible(False)
            self.lab_Ps.setVisible(False)
            self.LET_inputB.setVisible(True)
            


    def on_LET_inputA_textChanged(self, text):
        self.__setNameData()


    def on_LET_inputB_textChanged(self, text):
        self.__setNameData()


    #=======================================================================================================================================
    
    def on_btn_top_clicked(self, args=None):
        if args == None:return
        self.__textIndex = 0
        self.__setNameData()



    def on_btn_left_clicked(self, args=None):
        if args == None:return
        self.__textIndex = min(max(0, self.__textIndex - 1), self.__textMaxIndex)
        self.__setNameData()


        
    def on_btn_right_clicked(self, args=None):
        if args == None:return
        self.__textIndex = min(max(0, self.__textIndex + 1), self.__textMaxIndex)
        self.__setNameData()



    def on_btn_end_clicked(self, args=None):
        if args == None:return
        self.__textIndex = self.__textMaxIndex
        self.__setNameData()
    
    #=======================================================================================================================================      

    def on_btn_refresh_clicked(self, args=None):
        if args == None:return
        #- clear List
        self.__listModel.clear()
        if self.rdn_maya.isChecked():
            for i, obj in enumerate(mc.ls(sl=True)):
                self.__listModel.insertRow(i, '%s'%obj)
                self.__textMaxIndex = max(self.__textMaxIndex, len(obj))                
            return 

        dirPath = '%s'%self.LET_path.text()
        if not os.path.isdir(dirPath):return
        
        files = os.listdir(dirPath)
        
        #- add Files
        for i, f in enumerate(files):
            self.__listModel.insertRow(i, '%s'%f)
            self.__textMaxIndex = max(self.__textMaxIndex, len(f))



    def on_btn_rename_clicked(self, args=None):
        if args == None:return
        #- rename
        if self.rdn_maya.isChecked():
            self._mayaRename()
        else:
            self._windowsRename()

        #- refresh List
        self.on_btn_refresh_clicked(True)

    
    #=======================================================================================================================================
    
    def _windowsRename(self):
        path = '%s'%self.LET_path.text()
        baseNameList, resultNameList = self.__listModel.result()
        for baseName, resultName in zip(baseNameList, resultNameList):
            if baseName == resultName:continue
            os.rename(os.path.join(path, baseName), nameTool.compileWindowsFileName(os.path.join(path, resultName)))
    


    @mayaTool.undo_decorator
    def _mayaRename(self):
        baseNameList, resultNameList = self.__listModel.result()
        counts = len(baseNameList)
        if counts == 0:return
        
        mc.select(baseNameList)
        for i in range(counts):
            if baseNameList[i] == resultNameList[i]:
                continue
            
            if mc.objExists(baseNameList[i]):
                mc.rename(baseNameList[i], nameTool.compileMayaObjectName(resultNameList[i]))
                
            else:
                mc.rename(mc.ls(sl=True)[i], nameTool.compileMayaObjectName(resultNameList[i]))
                
    #=======================================================================================================================================