import os.path 
import maya.cmds as mc
from FoleyUtils import scriptTool, uiTool


UIwndClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'ChangeOBJpivot.ui'))
class ChangeOBJpivot(UIwndClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'changeObjectPivotWindow'):
            return 
        
        super(ChangeOBJpivot, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #-------------
    
    
    def on_actionLoadMoveOBJ_triggered(self, args=None):
        if args==None:return
        SelectOBJ = mc.ls(sl=True)
        if len(SelectOBJ) == 0:return
        if SelectOBJ[0] == str(self.KeepedOBJLineEdit.text()):return
        
        self.MovedOBJLineEdit.setText(SelectOBJ[0])




    def on_actionLoadKeepOBJ_triggered(self, args=None):
        if args==None:return
        SelectOBJ = mc.ls(sl=True)
        if len(SelectOBJ) == 0:return
        if SelectOBJ[0] == str(self.MovedOBJLineEdit.text()):return
        self.KeepedOBJLineEdit.setText(SelectOBJ[0])
    
    
    
    
    
    def on_actionStartMove_triggered(self, args=None):
        if args==None:return
        toMoveOBJ = str(self.MovedOBJLineEdit.text())
        toKeepOBJ = str(self.KeepedOBJLineEdit.text())
        
        if not mc.objExists(toMoveOBJ) or not mc.objExists(toKeepOBJ):return
        if toMoveOBJ == toKeepOBJ:return
        
        
        self.ConstraintDT = {}
        self.ConstraintLocators = []
        
        
        for Jnt in (toKeepOBJ, toMoveOBJ):
            OldConstraintNode = [x for x in mc.listRelatives(Jnt, c=True, path=True) or [] if mc.nodeType(x).endswith('Constraint')]
            for OCSN in OldConstraintNode:
                ConstraintType = mc.nodeType(OCSN)
                ConstraintOBJ  = eval('mc.%s("%s", q=True, tl=True)'%(ConstraintType, OCSN))
                
                self.ConstraintDT.setdefault(Jnt, {})['type'] = ConstraintType
                self.ConstraintDT.setdefault(Jnt, {})['ConsOBJ'] = ConstraintOBJ
                mc.delete(OCSN)
            
            
            Loc = mc.spaceLocator(p=(0,0,0))
            mc.delete(mc.parentConstraint(Jnt, Loc))
            ConstraintNode = mc.parentConstraint(Loc[0], Jnt)
            
            self.ConstraintLocators.append(Loc[0])
            self.ConstraintLocators.append(ConstraintNode[0])

        
        
    
    def on_actionEndMove_triggered(self, args=None):
        if args==None:return
        if not hasattr(self, 'ConstraintLocators'):return
        if self.ConstraintLocators == []: return
        
        mc.delete(self.ConstraintLocators)
        for Jnt in self.ConstraintDT.iterkeys():
            eval('mc.%s(%s,"%s", mo=True)'%(self.ConstraintDT[Jnt]['type'],  self.ConstraintDT[Jnt]['ConsOBJ'], Jnt))
        