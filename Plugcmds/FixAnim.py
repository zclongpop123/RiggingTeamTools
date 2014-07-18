import os, inspect, re, json
from PyQt4 import QtCore, uic
import maya.cmds as mc
from FoleyUtils import scriptTool, uiTool

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

UIfile = os.path.join(scriptTool.getScriptPath(), 'FixAnim.ui')
UIClass, BaseClass = uic.loadUiType(UIfile)

class FixAnim(UIClass, BaseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'FixAnimationWindow'):
            return        
        
        super(FixAnim, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #----------------------
        self.referenceFiles = {}
        self.sourceFiles = []
    
    def on_actionRefreshScene_triggered(self, args=None):
        if args == None:return
        self.referenceFiles.clear()
        self.ReferenceFilescomboBox.clear()
        referenceFiles = mc.file(q=True, r=True)
        for rFile in referenceFiles:
            baseBame = os.path.basename(rFile)
            filePath = os.path.dirname(rFile)
            self.referenceFiles[baseBame] = filePath
            self.ReferenceFilescomboBox.addItem(baseBame)

            

    def on_actionRefreshSourceFiles_triggered(self, args=None):
        if args == None:return
        self.ReferenceFileSourcecomboBox.clear()
        currentFile = str(self.ReferenceFilescomboBox.currentText())
        if len(currentFile) == 0:return
        self.sourceFiles = os.listdir(self.referenceFiles[currentFile])
        for sFile in self.sourceFiles:
            if not re.search('.m[ab]$', sFile):continue
            self.ReferenceFileSourcecomboBox.addItem(sFile)


    
    def on_actionLoadControls_triggered(self, args=None):
        if args == None:return
        SelectControl = mc.ls(sl=True)
        self.ControlsLineEdit.setText('   '.join(SelectControl))
        



    def on_actionSetJsonFilePath_triggered(self, args=None):
        if args == None:return
        filePath = mc.fileDialog2(fileFilter=("JSON Files (*.json)"))
        if not filePath:return
        self.FilePathLineEdit.setText(filePath[0])



    def on_actionRefreshData_triggered(self, args=None):
        if args == None:return
        
        OldReferencePath = str(self.ReferenceFilescomboBox.currentText())
        NewReferencePath = str(self.ReferenceFileSourcecomboBox.currentText())
        referencePath = self.referenceFiles[OldReferencePath]
        

        if not os.path.isfile(os.path.join(referencePath, NewReferencePath)):return
        if OldReferencePath == NewReferencePath:return
        
        
        ControlText = str(self.ControlsLineEdit.text())
        Controls = re.findall('\S+', ControlText)
        if len(Controls) == 0:return
        

        JsonFilepath = str(self.FilePathLineEdit.text())
        if len(JsonFilepath) == 0:return
        

        #-> get Data
        data = {}
        for ctr in Controls:
            frames = mc.keyframe(ctr, q=True)
            if not frames:continue
            frames = {}.fromkeys(frames, None).keys()
            
            for fm in frames:
                mc.currentTime(fm)
                position = mc.xform(ctr, q=True, ws=True, t=True)
                rotation = mc.xform(ctr, q=True, ws=True, ro=True)
                data.setdefault(ctr, {})[fm] = (position, rotation)        
        
        #-> save Data
        f = open(JsonFilepath, 'w')
        json.dump(data, f, indent=2)
        f.close()
        
        #-> change reference characters
        referenceNode = mc.file(os.path.join(referencePath, OldReferencePath), q=True, rfn=True)        
        mc.file(os.path.join(referencePath, NewReferencePath), lr=referenceNode)
        
        #-> read Data
        f = open(JsonFilepath, 'r')
        data = json.load(f)
        f.close()
        
        #-> set Data
        for ctr, values in data.iteritems():
            for fm, lst in values.iteritems():
                mc.currentTime(fm)
                mc.xform(ctr, ws=True, t=lst[0])
                mc.xform(ctr, ws=True, ro=lst[1])
                
                mc.setKeyframe('%s.tx'%ctr)
                mc.setKeyframe('%s.ty'%ctr)
                mc.setKeyframe('%s.tz'%ctr)
                mc.setKeyframe('%s.rx'%ctr)
                mc.setKeyframe('%s.ry'%ctr)
                mc.setKeyframe('%s.rz'%ctr)