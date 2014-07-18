import os, inspect
from PyQt4 import QtGui, uic
import ConvertControl
import maya.cmds as mc
reload(ConvertControl)
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

def getScriptPath():
    PyFile = inspect.getfile(inspect.currentframe())
    return os.path.dirname(PyFile)

WindowClass, BaseClass = uic.loadUiType(os.path.join(getScriptPath(), 'FaceControlBuilderUI.ui'))
class FaceControlBuilderUI(WindowClass, BaseClass):
    def __init__(self, parent=None, positionPoint=None):
        wnd = parent.findChild(QtGui.QMainWindow, 'FaceControlBuilder')
        if wnd:
            wnd.show()
            wnd.showNormal()
            wnd.activateWindow()
            return        

        super(FaceControlBuilderUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #-----------------------------------------------------------------------------------
        
        self.chara = ''
        
        #-----------------------------------------------------------------------------------
        for child in parent.children():
            if not hasattr(child, 'isWindow'):
                continue
    
            if not child.isWindow():
                continue
    
            if child.windowTitle() == 'Face Rig Builder':
                self.C_characterDisplayLabel.setText(child.frbCharacterAssetListWidget.currentItem().text())
                self.on_actionCurrentCharacterChanged_triggered(True)
                
                child.frbCharacterAssetListWidget.currentTextChanged.connect(self.C_characterDisplayLabel.setText)
                child.frbCharacterAssetListWidget.currentTextChanged.connect(self.on_actionCurrentCharacterChanged_triggered)
                break
    
    
    
    def on_actionCurrentCharacterChanged_triggered(self, args=None):
        if args == None:return
        self.chara = str(self.C_characterDisplayLabel.text())
        self._refreshVersion()
    

    def _refreshVersion(self):
        Versions = ConvertControl.getTempLocatorVersions(self.chara)
        
        self.C_TempLocatorComboBox.clear()
        self.C_TempLocatorComboBox.addItems(Versions)
        self.C_TempLocatorComboBox.setCurrentIndex(self.C_TempLocatorComboBox.count() - 1)


    def on_actionVersionChanged_triggered(self, args=None):
        if args == None:return
        version = str(self.C_TempLocatorComboBox.currentText())
        if version == '':
            self.C_TempLocatorLineEdit.clear()
        else:
            self.C_TempLocatorLineEdit.setText(ConvertControl.getVersiondTempLocatorFile(self.chara, version))
    


    def on_actionImportTempLocators_triggered(self, args=None):
        if args == None:return
        ConvertControl.importLocators(str(self.C_TempLocatorLineEdit.text()))
    
    
    def on_actionPublishTempLocators_triggered(self, args=None):
        if args == None:return
        ConvertControl.publishTempLocators(self.chara)
        self._refreshVersion()
    
    
    def on_actionCreateTempLocators_triggered(self, args=None):
        if args == None:return
        ConvertControl.makeTempLocators()

        
    def on_actionMirrorLocatorsLR_triggered(self, args=None):
        if args == None:return
        ConvertControl.mirrorTempLocators('L_', 'R_', 'x')
        
    
    def on_actionMirrorLocatorsRL_triggered(self, args=None):
        if args == None:return
        ConvertControl.mirrorTempLocators('R_', 'L_', 'x')
    

        
    def on_actionBuildFaceControl_triggered(self, args=None):
        if args == None:return
        version = str(self.C_TempLocatorComboBox.currentText())
        ConvertControl.buildControlOnFace(self.chara, version)

    
    def on_C_publishDataButton_clicked(self, args=None):
        if args==None:return
        filePath = mc.fileDialog2(fm=0, ff='JSON Files (*.json)')[0]
        ConvertControl.exportControlData(filePath)

    def on_C_importDataButton_clicked(self, args=None):
        if args==None:return
        filePath = mc.fileDialog2(fm=1, ff='JSON Files (*.json)')[0]
        if not os.path.isfile(filePath):return
        ConvertControl.importControlData(filePath)