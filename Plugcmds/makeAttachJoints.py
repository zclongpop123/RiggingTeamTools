import os, inspect
import maya.cmds as mc
from FoleyUtils import scriptTool, uiTool


def makePathJoints(basePathCus, UppathCus, JointCounts=5, uValuezerotoone=False):
    '''
    make joints attach to path..
    '''
    #--------------------------
    def _Attach(pathCus, attactOBJ, uValue, UpperOBJ=None, uValuezerotoone=False):
        CusShape = mc.listRelatives(pathCus, s=True, type='nurbsCurve')
        motionpathNode = mc.createNode('motionPath')
        
        # connect curve and motionpath node..
        mc.connectAttr(CusShape[0] + '.worldSpace[0]', motionpathNode + '.geometryPath')
        # connect motionpath node and object..
        for outAttr, inAttr in (('.rotateOrder', '.rotateOrder'),('.rotate', '.rotate'),('.allCoordinates', '.translate')):
            mc.connectAttr(motionpathNode + outAttr, attactOBJ + inAttr)        

        # set Uvalue..
        mc.setAttr(motionpathNode + '.uValue', uValue)
        
        
        # set offset..
        if uValuezerotoone:
            mc.setAttr(motionpathNode + '.fractionMode', 1)


        # set upvector..
        if not UpperOBJ:return
        mc.setAttr(motionpathNode + '.worldUpType', 1)
        mc.connectAttr(UpperOBJ + '.worldMatrix[0]', motionpathNode + '.worldUpMatrix')
        mc.setAttr(motionpathNode + '.frontAxis', 0)
        mc.setAttr(motionpathNode + '.upAxis', 2)        

    #--------------------------
    for i in range(JointCounts):
        mc.select(cl=True)
        
        Jnt = mc.joint(p=(0, 0, 0))
        Loc = mc.spaceLocator(p=(0, 0, 0))[0]
        uValue = 0.0
        
        if not uValuezerotoone:
            uValue = i
        else:
            uValue = (float(i) - 0) / (float(JointCounts - 1) - 0) * (1.0 - 0.0) + 0.0
        
        _Attach(UppathCus, Loc, uValue, None, uValuezerotoone)
        _Attach(basePathCus, Jnt, uValue, Loc, uValuezerotoone)




UIwndClass, baseClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'makeAttachJoints.ui'))
class makeAttachJoints(UIwndClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'makeAttachJointsWindow'):
            return

        super(makeAttachJoints, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #-------------


    def on_actionLoadBaseCurve_triggered(self, clicked=None):
        if clicked==None:return
        SelOBJ = mc.ls(sl=True)
        if len(SelOBJ) == 1:
            self.BaseCusFLD.setText(SelOBJ[0])
        else:
            print '> > > you must select onlyone curve ! ! !',
        

    def on_actionLoadUpCurve_triggered(self, clicked=None):
        if clicked==None:return
        SelOBJ = mc.ls(sl=True)
        if len(SelOBJ) == 1:
            self.UpCusFLD.setText(SelOBJ[0])
        else:
            print '> > > you must select onlyone curve ! ! !',    
    
    
    def on_minmaxRDN_toggled(self, args=None):
        if not args:return
        baseCurve = str(self.BaseCusFLD.text())
        if not mc.objExists(baseCurve):return
        self.CountsFLD.setValue(len(mc.ls('%s.cv[0:%d]'%(baseCurve, self.CountsFLD.maximum()), fl=True)))
    
    
    def on_actionMakeJoints_triggered(self, clicked=None):
        if clicked==None:return
        baseCurve = str(self.BaseCusFLD.text())
        upperCurve = str(self.UpCusFLD.text())
        jointCounts = self.CountsFLD.value()
        zeroToOne = self.zerotooneRDN.isChecked()
        
        # test...
        if len(baseCurve) < 1:return
        if len(upperCurve) < 1:return
        if jointCounts < 1:return
        # make...
        makePathJoints(baseCurve, upperCurve, jointCounts, zeroToOne)