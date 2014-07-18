import os
from PyQt4 import QtGui, uic
import maya.cmds as mc
import maya.mel as mel
from FoleyUtils import scriptTool, uiTool

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

UIfile = os.path.join(scriptTool.getScriptPath(), 'DynControlUI.ui')
UIClass, BaseClass = uic.loadUiType(UIfile)

class DynControl(UIClass, BaseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'dynControlWindow'):
            return
        
        super(DynControl, self).__init__(parent)
        self.setupUi(self)
        self.show()



    def refreshHairSystems(self):
        for checkBox in self.HairSystemList.children():
            checkBox.deleteLater()
        
        HairSysTem = mc.listRelatives(mc.ls(type='hairSystem'), p=True)
        HairSysTem = {}.fromkeys(HairSysTem, None).keys()
        HairSysTem.sort()
        
        for i, hairsys in  enumerate(HairSysTem):
            CBX = QtGui.QCheckBox(self.HairSystemList)
            CBX.setText(hairsys)
            CBX.move(9, i * 20 + 9)
            CBX.show()
            self.HairSystemList.setMinimumHeight((i + 1) * 20 + 18)
            


    def on_actionCreateDynControl_triggered(self, clicked=None):
        if clicked==None:return
        SelOBJ = mc.ls(sl=True, type='joint')
        if len(SelOBJ) != 2:
            self.refreshHairSystems()
            return
        
        melScripts = os.path.join(scriptTool.getScriptPath(), 'makeIkHair.mel')
        melScripts = melScripts.replace('\\', '/')
        mel.eval('source "%s"'%melScripts)
        self.refreshHairSystems()
        



    def on_actionConnectHairSystem_triggered(self, clicked=None):
        if clicked==None:return
        HairSystem = []
        for checkBox in self.HairSystemList.children():
            if checkBox.isChecked():
                HairSystem.append(str(checkBox.text()))
        if len(HairSystem) == 0:return
        
        ControlFile = os.path.join(scriptTool.getScriptPath(), 'jiesuankaiguan.ma')
        mc.file(ControlFile, i=True)
        
        #----------------------------
        HairControlG = mc.ls(assemblies=True)[-1]
        HairControl  = [x for x in mc.listRelatives(HairControlG, ad=True, path=True) if x.endswith('ctrl')][0]
        attractionScale = [x for x in mc.listRelatives(HairControlG, ad=True, path=True) if x.endswith('attractionScale')][0]
        
        mc.connectAttr('%s.%s'%(HairSystem[0], 'message'), '%s.%s'%(attractionScale, 'hairSystem'), f=True)
        for i, sysNode in enumerate(HairSystem):
            JointA = mc.connectionInfo('%s.%s'%(sysNode, 'iterations'), sfd=True)
            JointA = JointA.split('.')[0]
            mc.connectAttr('%s.%s'%(HairControl, 'chainStartEnveloppe'),  '%s.%s'%(JointA,  'chainStartEnveloppe'),  f=True)
            mc.connectAttr('%s.%s'%(HairControl, 'chainStartFrame'),      '%s.%s'%(sysNode, 'startFrame'),           f=True)
            mc.connectAttr('%s.%s'%(HairControl, 'chainStiffness'),       '%s.%s'%(sysNode, 'stiffness'),            f=True)
            mc.connectAttr('%s.%s'%(HairControl, 'chainDamping'),         '%s.%s'%(sysNode, 'damp'),                 f=True)
            mc.connectAttr('%s.%s'%(HairControl, 'chainGravity'),         '%s.%s'%(sysNode, 'gravity'),              f=True)
            mc.connectAttr('%s.%s'%(HairControl, 'chainCollide'),         '%s.%s'%(sysNode, 'collide'),              f=True)
            mc.connectAttr('%s.%s'%(HairControl, 'StarCurveAttract'),     '%s.%s'%(sysNode, 'startCurveAttract'),    f=True)
        
            if i > 0:
                mc.connectAttr('%s.%s'%(HairSystem[0], 'attractionScale[0]'),  '%s.%s'%(sysNode, 'attractionScale[0]'))
                mc.connectAttr('%s.%s'%(HairSystem[0], 'attractionScale[1]'),  '%s.%s'%(sysNode, 'attractionScale[1]'))        
        
        if mc.objExists('hairExp'):return
        mel.eval('source "%s"'%os.path.join(scriptTool.getScriptPath(), 'makeScriptNode.mel').replace('\\', '/'))
        mc.setAttr('hairExp.scriptType', 1)



    
    def rigJoint(self, Jnt):
        Grp = [mc.group(em=True, name=Jnt.replace(Jnt.split('_')[-2], 'RO2'))]
        NameL = ('RO1', 'ctl', 'cth', 'ctlG', 'ctlGrp') 
        for i in range(5):
            ControlName = Jnt.replace(Jnt.split('_')[-2], NameL[i])
            ControlName = ControlName.replace('ANIM_', '')
            transform  = mc.group(Grp[-1], name=ControlName)
            Grp.append(transform)
            for attr in ('sx', 'sy', 'sz', 'v'):
                mc.setAttr('%s.%s'%(transform, attr), l=True, k=False)
                
        Circle = mc.circle(nr=(1,0,0), r=2, ch=False)[0]
        shape = mc.listRelatives(Circle, s=True, path=True)
        mc.parent(shape, Grp[2], r=True, s=True)
        mc.delete(Circle)
        return Grp
    
    
    
    
    def on_actionRigJoints_triggered(self, clicked=None):
        if clicked==None:return
        sellectedGrp = mc.ls(sl=True)
        if len(sellectedGrp) == 0:return
        for Grp in sellectedGrp:
            JointList = [Grp]
            JointList.extend(mc.listRelatives(Grp, ad=True, path=True, type='joint') or [])
            for childrenJnt in JointList:
                if mc.nodeType(childrenJnt) != 'joint':continue
                if not mc.listRelatives(childrenJnt, c=True, type='joint'):continue
                
                print childrenJnt
                controlList = self.rigJoint(childrenJnt)
                mc.delete(mc.parentConstraint(childrenJnt, controlList[-1]))
                mc.parentConstraint(controlList[0], childrenJnt)
                
                if not mc.listRelatives(childrenJnt, p=True, type='joint'):continue
                mc.parent(controlList[-1], mc.listRelatives(childrenJnt, p=True, type='joint')[0])
            
            Shape = mc.listRelatives(Grp, s=True, path=True)
            if not Shape:continue
            mc.delete(Shape)