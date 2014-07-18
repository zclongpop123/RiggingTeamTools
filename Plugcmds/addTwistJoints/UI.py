import sys, os, inspect, cmds
from PyQt4 import QtGui, QtCore, uic
from FoleyUtils import scriptTool, uiTool


ScriptPath = scriptTool.getScriptPath()
if ScriptPath not in sys.path:
    sys.path.append(ScriptPath)


waningWindowClass, warningbaseClass = uic.loadUiType(os.path.join(ScriptPath, 'warningDialog.ui'))
class WarningDialog(waningWindowClass, warningbaseClass):
    def __init__(self, waningText, parent=None):
        super(WarningDialog, self).__init__(parent)
        self.setupUi(self)
        self.warningLabel.setText(waningText)
        self.exec_()
        

class ComponentFrame(QtGui.QFrame):
    def __init__(self, parent=None):
        super(ComponentFrame, self).__init__(parent)
        self.buildUI()
    
    def buildUI(self):
        self.setGeometry(QtCore.QRect(170, 240, 323, 40))
        self.setFrameShape(QtGui.QFrame.NoFrame)
        self.setFrameShadow(QtGui.QFrame.Raised)
        
        Layout_1 = QtGui.QHBoxLayout(self)
        Layout_1.setSpacing(2)
        Layout_1.setMargin(2)
        
        self.enableCheckBox = QtGui.QCheckBox(self)
        Layout_1.addWidget(self.enableCheckBox)
        
        groupBox = QtGui.QGroupBox(self)
        groupBox.setMinimumSize(QtCore.QSize(302, 38))
        groupBox.setMaximumSize(QtCore.QSize(302, 38))
        
        
        Layout_2 = QtGui.QHBoxLayout( groupBox)
        Layout_2.setSpacing(2)
        Layout_2.setMargin(3)
        
        self.nameLineEdit = QtGui.QLineEdit(groupBox)
        self.nameLineEdit.setMinimumSize(QtCore.QSize(130, 26))
        self.nameLineEdit.setMaximumSize(QtCore.QSize(130, 26))
        self.nameLineEdit.setText('L_')
        Layout_2.addWidget(self.nameLineEdit)
        
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Layout_2.addItem(spacerItem)
        
        self.jointCountSpinBox = QtGui.QSpinBox(groupBox)
        self.jointCountSpinBox.setMinimumSize(QtCore.QSize(60, 26))
        self.jointCountSpinBox.setMaximumSize(QtCore.QSize(60, 26))
        self.jointCountSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.jointCountSpinBox.setMinimum(2)
        self.jointCountSpinBox.setMaximum(26)
        Layout_2.addWidget( self.jointCountSpinBox)
        
        
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Layout_2.addItem(spacerItem1)
        
        
        self.mirrorCheckBox = QtGui.QCheckBox(groupBox)
        self.mirrorCheckBox.setMinimumSize(QtCore.QSize(16, 26))
        Layout_2.addWidget(self.mirrorCheckBox)
        Layout_1.addWidget(groupBox)         


Uiwnd, UiClass = uic.loadUiType(os.path.join(ScriptPath, 'AddTwistJoints.ui'))
class AddTwistJointsUI(Uiwnd, UiClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'addTwistJointsWindow'):
            return
            
        #-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
        super(AddTwistJointsUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #----------------------------
        self.ComponentsUI = []
        #----------------------------
        self.CharacterComboBox.clear()
        self.CharacterComboBox.addItems(cmds.getCharacters())

    
    def on_CharacterComboBox_currentIndexChanged(self, Character):
        if isinstance(Character, int):return
        
        versions = cmds.getAssetVersions(cmds.ROOT_ASSET_PATH, str(Character), 'body', 'twistJointcomponent')
        self.ComponentComboBox.clear()
        self.ComponentComboBox.addItems(versions)
        self.ComponentComboBox.setCurrentIndex(len(versions) - 1)
        
        
        versions = cmds.getAssetVersions(cmds.ROOT_ASSET_PATH, str(Character), 'body', 'twistJointguide')
        self.GuideComboBox.clear()
        self.GuideComboBox.addItems(versions)
        self.GuideComboBox.setCurrentIndex(len(versions) - 1)
        
    
    
    def on_ComponentComboBox_currentIndexChanged(self, version):
        if isinstance(version, int):return
        
        for comUI in self.ComponentsUI:
            comUI.deleteLater()
        self.ComponentsUI = []
        
        data = cmds.readVersiondComponent(str(self.CharacterComboBox.currentText()), str(self.ComponentComboBox.currentText()))
        if not data:return
        for dt in data:
            self.on_actionAddComponent_triggered(True)
            self.ComponentsUI[-1].nameLineEdit.setText(dt[0])
            self.ComponentsUI[-1].jointCountSpinBox.setValue(dt[1])
            self.ComponentsUI[-1].mirrorCheckBox.setChecked(dt[2])




    def on_actionPublishComponent_triggered(self, args=None):
        if args == None:return 
        if WarningDialog('publish new component ? ? ?').result() == 0:return

        character = str(self.CharacterComboBox.currentText())
        data = []
        for comUI in self.ComponentsUI:
            nameSpace = str(comUI.nameLineEdit.text())
            jointCount = comUI.jointCountSpinBox.value()
            mirror = comUI.mirrorCheckBox.isChecked()   
            data.append([nameSpace, jointCount, mirror])
            
        cmds.publishComponent(character, data)




    def on_actionPublishGuide_triggered(self, args=None):
        if args == None:return
        if WarningDialog('publish new guide ? ? ?').result() == 0:return
        
        character = str(self.CharacterComboBox.currentText())
        cmds.publishGuide(character)




    def on_actionAddComponent_triggered(self, args=None):
        if args == None:return 
        self.ComponentsUI.append(ComponentFrame(self.ComponentContainer))
        self.ComponentContainerLayout.insertWidget(self.ComponentContainerLayout.count()-1, self.ComponentsUI[-1])
        


    def on_actionSelectAll_triggered(self, args=None):
        if args == None:return 
        for comUI in self.ComponentsUI:
            comUI.enableCheckBox.setChecked(True)


    
    def on_actionReverSelection_triggered(self, args=None):
        if args == None:return 
        for comUI in self.ComponentsUI:
            if not comUI.enableCheckBox.isChecked():
                comUI.enableCheckBox.setChecked(True)
            else:
                comUI.enableCheckBox.setChecked(False)



    def on_actionRemoveComponent_triggered(self, args=None):
        if args == None:return
        Indexes = []
        for i, comUI in enumerate(self.ComponentsUI):
            if comUI.enableCheckBox.isChecked():
                comUI.deleteLater()
                Indexes.append(i)
        
        Indexes.reverse()
        for i in Indexes:
            self.ComponentsUI.pop(i)


    
    def on_actionBuideGuide_triggered(self, args=None):
        if args == None:return
        if WarningDialog('You will build guides, unsaved guide will be lost.. \r\n continue ? ? ?').result() == 0:return
        
        character = str(self.CharacterComboBox.currentText())
        guideVersion = str(self.GuideComboBox.currentText())
        componentData = []
        for comUI in self.ComponentsUI:
            nameSpace = str(comUI.nameLineEdit.text())
            jointCount = comUI.jointCountSpinBox.value()
            mirror = comUI.mirrorCheckBox.isChecked()
            #-
            componentData.append([nameSpace, jointCount, mirror])
        #---
        cmds.buideGuide(character, guideVersion, componentData)
    


    def on_actionMirrorGuideLR_triggered(self, args=None):
        if args == None:return
        cmds.mirrorGuide('L_', 'R_')
    
    
    
    
    def on_actionMirrorGuideRL_triggered(self, args=None):
        if args == None:return
        cmds.mirrorGuide('R_', 'L_')
    
    
    
    
    def on_actionBuideRig_triggered(self, args=None):
        if args == None:return
        keepGuide = self.keepGuideCBX.isChecked()

        cmds.buildeRig(keepGuide)