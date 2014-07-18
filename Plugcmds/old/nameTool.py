import os, inspect, rigToolUtils
from PyQt4 import  uic
import maya.cmds as mc

def getScriptPath():
    initfile = inspect.getfile(inspect.currentframe())
    initdir  = os.path.dirname(initfile)
    return initdir

#---------------------------------------------------------------------------------------------------------------

Uiwnd, UiClass = uic.loadUiType(os.path.join(getScriptPath(), 'nameTool.ui'))
class NameTool(Uiwnd, UiClass):
    def __init__(self, PntWnd = None):
        super(NameTool, self).__init__(PntWnd)
        self.setupUi(self)
        self.ReplaceInputField.setVisible(False)
        self.show()
        
        #---------------------------------------
        self.insertPs = 0
        self.maxLen = 0
        self.OBJList = []
        self.selOBJList = []
        #---------------------------------------
    def on_actionRefreshList_triggered(self, agrs=None):
        if agrs == None:return
        self.listWidget.clear()
        prefixString = str(self.lineEdit.text())
        replaceString = str(self.ReplaceInputField.text())
        for item in self.OBJList:
            realname = item.split('|')[-1]
            self.maxLen = max(len(realname), self.maxLen)
            displayName = realname
            if self.radioButton_Prefix.isChecked():
                displayName = '%s%s%s'%(realname[:self.insertPs],  prefixString,  realname[self.insertPs:])
            else:
                displayName = realname.replace(prefixString, replaceString)
            self.listWidget.addItem(displayName)



    def on_actionLoadOBJ_triggered(self, agrs=None):
        if agrs == None:return
        #---------------------------------------
        self.insertPs = 0
        self.maxLen = 0
        self.OBJList = []
        self.selOBJList = []
        #---------------------------------------
        self.selOBJList = mc.ls(sl=True)
        if len(self.selOBJList) == 0:return
        
        for OBJ in self.selOBJList:
            self.OBJList.append(OBJ)
            if not self.radioButton_Herarchy.isChecked():continue
            self.OBJList.extend(mc.listRelatives(OBJ, ad=True, path=True, type='transform') or [])
        self.on_actionRefreshList_triggered(True)
        #---------------------------------------

        

    def on_actionToTop_triggered(self, agrs=None):
        if agrs == None:return
        self.insertPs = 0
        self.on_actionRefreshList_triggered(True)
        


    def on_actionToEnd_triggered(self, agrs=None):
        if agrs == None:return
        self.insertPs = self.maxLen
        self.on_actionRefreshList_triggered(True)
        
        

    def on_actionToLeft_triggered(self, agrs=None):
        if agrs == None:return
        if self.insertPs <= 0:return
        self.insertPs -= 1
        self.on_actionRefreshList_triggered(True)
        
        

    def on_actionToRight_triggered(self, agrs=None):
        if agrs == None:return
        if self.insertPs >= self.maxLen:return
        self.insertPs += 1
        self.on_actionRefreshList_triggered(True)
        

    @rigToolUtils.undo_decorator
    def on_actionRename_triggered(self, agrs=None):
        
        if agrs == None:return
        if len(self.OBJList) == 0:return
        mc.select(self.OBJList)
        for i in range(len(self.OBJList)):
            oldName = self.OBJList[i]
            if not mc.objExists(oldName):
                oldName = mc.ls(sl=True)[i]
            newName = str(self.listWidget.item(i).text())
            mc.rename(oldName, newName)
        mc.select(cl=True)
        #---------------------------------------
        self.insertPs = 0
        self.maxLen = 0
        self.OBJList = []
        self.selOBJList = []
        self.listWidget.clear()
        #---------------------------------------        
        

if __name__ == "__main__":NameTool()