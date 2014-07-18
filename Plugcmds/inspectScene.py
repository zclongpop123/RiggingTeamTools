import string, re, os.path
import maya.cmds as mc
from FoleyUtils import scriptTool, uiTool



UIwndClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'inspectScene.ui'))
class InspectSceneUI(UIwndClass, baseClass):
    
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'inspectSceneWindow'):
            return
        
        super(InspectSceneUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #-------------
    
    
    def on_actionInspectScene_triggered(self, *agrs):
        if not agrs:return
        self.DuplacatesNamesOBJ  = InspectScene.inspectDuplicatesNames()
        self.NoFreeGeometeys     = InspectScene.inspectGeometryAttributes()
        self.DuplicatesShapesOBJ = InspectScene.insepectDuplicatesShapes()
        
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        def _readResult(OBJList, Field, Button):
            if len(OBJList) > 0:
                Button.setEnabled(True)
                Field.setValue(len(OBJList))
                Field.setStyleSheet('color: rgb(255, 90, 90)')
            else:
                Button.setDisabled(True)
                Field.setValue(0)
                Field.setStyleSheet('')            
        
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        _readResult(self.DuplacatesNamesOBJ, self.fldDuplicatesnames, self.btnSelectDuplicatesnames)
        _readResult(self.NoFreeGeometeys, self.fldNoFreezeGeometeys, self.btnSelectNoFreezeGeometeys)
        _readResult(self.DuplicatesShapesOBJ, self.fldDuplicatesShapes, self.btnSelectDuplicatesShapes)
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    
        
    def on_actionSelectDuplicatesnames_triggered(self, *agrs):
        if not agrs:return
        mc.select(self.DuplacatesNamesOBJ)
        
        
        
    def on_actionSelectNoFreezeGeometeys_triggered(self, *agrs):
        if not agrs:return
        mc.select(self.NoFreeGeometeys)
        
        

    def on_actionSelectDuplicatesShapes_triggered(self, *agrs):
        if not agrs:return
        mc.select(self.DuplicatesShapesOBJ)
        



class InspectScene(object):

    @classmethod
    def inspectDuplicatesNames(self):
        transforms = string.join(mc.ls(type='transform'))
        Duplicatesnames = re.findall('\S+\|+\S+', transforms)
        return Duplicatesnames


    @classmethod
    def inspectGeometryAttributes(self):
        geometrys   = mc.listRelatives(mc.ls(type='mesh'), p=True, path=True)
        u_geometrys = []
        for geo in geometrys:
            Values = []
            for attr in ('tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'):
                Values.append(mc.getAttr('%s.%s'%(geo, attr)))
            if sum(Values) == 3 and Values[-3:] == [1, 1, 1]:continue
            u_geometrys.append(geo)
            
        return u_geometrys


    @classmethod
    def insepectDuplicatesShapes(self):
        geometrys   = mc.listRelatives(mc.ls(type='mesh'), p=True, path=True)
        u_geometrys = []
        for geo in geometrys:
            if len(mc.listRelatives(geo, s=True)) > 1:
                u_geometrys.append(geo) 
        return u_geometrys