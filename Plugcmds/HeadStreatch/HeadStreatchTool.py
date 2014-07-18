import os, re, string
from PyQt4 import QtCore, QtGui, uic
import maya.cmds as mc
from FoleyUtils import scriptTool, uiTool


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
UIwndClass, baseClass = uic.loadUiType('%s/HeadStreatchTool.ui'%scriptTool.getScriptPath())
class HeadStreatchUI(UIwndClass, baseClass):
    def __init__(self, parent=None):
        if uiTool.windowExists(parent, 'headStreatchWindow'):
            return
        
        super(HeadStreatchUI, self).__init__(parent)
        self.setupUi(self)
        self.show()
        #-------------

    def on_actionBuildGuide_triggered(self, clicked=None):
        if clicked==None:return
        self.guideFile = os.path.join(getScriptPath(), 'HeadStreatch_guide.ma')
        self.guideFile = self.guideFile.replace('\\', '/')
        
        if self.guideFile in mc.file(q=True, r=True):return 
        mc.file(self.guideFile, r=True, namespace='guide', loadReferenceDepth='all', gl=True)
    


    def on_actionBuildRig_triggered(self, clicked=None):
        if clicked==None:return
        makeHeadStreatch(jointCount=self.jointCountsSpinBox.value())
        
        if self.keepGuideCheckBox.isChecked():return
        if not hasattr(self, 'guideFile'):return
        mc.file(self.guideFile, rr=True)



    
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def clamp(minValue, maxValue, inputValue):
    return min(max(minValue, inputValue), maxValue)
    #if inputValue < minValue:
        #return minValue
    
    #if inputValue > maxValue:
        #return maxValue

    #return inputValue



#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def getHeadStreatchGuide():
    allLocators = ' '.join(mc.listRelatives(mc.ls(type='locator'), p=True, path=True))
    
    streatchStartGuideLoc = re.search('(\w+:)*head_streatchStart_guide_0', allLocators)
    streatchEndGuideLoc = re.search('(\w+:)*head_streatchEnd_guide_0', allLocators)
    
    if not streatchStartGuideLoc:
        return
    if not streatchEndGuideLoc:
        return
    
    return (streatchStartGuideLoc.group(), streatchEndGuideLoc.group())



#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def makeAttachCurve(points=5):
    startLoc, endLoc = getHeadStreatchGuide()
    
    startPs = mc.xform(startLoc, q=True, ws=True, rp=True)
    endPs   = mc.xform(endLoc,   q=True, ws=True, rp=True)

    positions = []
    for i in range(points):
        X = startPs[0] + (endPs[0] - startPs[0]) / (points - 1) * i
        Y = startPs[1] + (endPs[1] - startPs[1]) / (points - 1) * i
        Z = startPs[2] + (endPs[2] - startPs[2]) / (points - 1) * i
        
        positions.append([X, Y, Z])

    Xsv = (positions[1][0] - positions[0][0]) * 0.33333 + positions[0][0]
    Ysv = (positions[1][1] - positions[0][1]) * 0.33333 + positions[0][1]
    Zsv = (positions[1][2] - positions[0][2]) * 0.33333 + positions[0][2]
        
    Xev = (positions[-1][0] - positions[-2][0]) * 0.66666 + positions[-2][0]
    Yev = (positions[-1][1] - positions[-2][1]) * 0.66666 + positions[-2][1]
    Zev = (positions[-1][2] - positions[-2][2]) * 0.66666 + positions[-2][2]
        
    positions.insert(1,  [Xsv, Ysv, Zsv])
    positions.insert(-1, [Xev, Yev, Zev])


    return mc.curve(d=3, p=positions)



#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def makeAttachJoints(pathCus, upVectorCus, num=5):
    '''
    make joints attach to path..
    '''
    #--------------------------
    def _Attach(pathCus, attactOBJ, uValue, UpperOBJ=None, uValuezerotoone=True):
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
        mc.setAttr(motionpathNode + '.frontAxis', 1)
        mc.setAttr(motionpathNode + '.upAxis', 0)        

    #--------------------------
    JointList   = []
    LocatorList = []
    for i in range(num):
        mc.select(cl=True)
        
        Jnt = mc.joint(p=(0, 0, 0))
        Loc = mc.spaceLocator(p=(0, 0, 0))[0]

        uValue = (float(i) - 0) / (float(num - 1) - 0) * (1.0 - 0.0) + 0.0
        uValue = clamp(0.001, 0.999, uValue)
        
        _Attach(upVectorCus, Loc, uValue, None)
        _Attach(pathCus, Jnt, uValue, Loc)

        JointList.append(Jnt)
        LocatorList.append(Loc)

    #----------------------------
    return JointList, LocatorList



def makeHeadStreatch(jointCount=5):
    # -> testing guide
    if not getHeadStreatchGuide():return
    
    # -> make curve
    attachCurve   = makeAttachCurve()
    upVectorCurve = mc.duplicate(attachCurve)[0]
    baseDistanceCurve = mc.duplicate(attachCurve)[0]
    
    # -> move up vector curve
    mc.move(mc.arclen(upVectorCurve, ch=False) / 18, 0, 0, upVectorCurve, r=True)

    # -> make joints
    Joints, upLocators = makeAttachJoints(attachCurve, upVectorCurve, jointCount)
    
    moreWeghtJnt = mc.createNode('joint')
    mc.delete(mc.parentConstraint(Joints[0], moreWeghtJnt))
    mc.setAttr('%s.radius'%moreWeghtJnt, 1.5)
    
    # -> make bend Joints
    BendJoints = []
    for i, jnt in enumerate(Joints):
        BendJoints.append(mc.createNode('joint'))
        mc.delete(mc.parentConstraint(jnt, BendJoints[i]))
        mc.makeIdentity(BendJoints[i], t=True, r=True, s=True, apply=True)
        if i > 0:
            mc.parent(BendJoints[i], BendJoints[i-1])
      
    # -> make streatch
    
    distanceValueNode = mc.arclen(attachCurve, ch=True)
    baseValueNode     = mc.arclen(baseDistanceCurve, ch=True)
    
    divdeNode = mc.createNode('multiplyDivide')
    
    for attr in ('input2X', 'input1Y', 'input2Z'):
        mc.connectAttr('%s.arcLength'%distanceValueNode, '%s.%s'%(divdeNode, attr))
        
    for attr in ('input1X', 'input2Y', 'input1Z'):
        mc.connectAttr('%s.arcLength'%baseValueNode, '%s.%s'%(divdeNode, attr))
        
    mc.setAttr('%s.operation'%divdeNode, 2)
    
    for jnt in Joints:
        for attr in 'XYZ':
            mc.connectAttr('%s.output%s'%(divdeNode, attr), '%s.scale%s'%(jnt, attr))
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    DisStartLocator = mc.spaceLocator(p=(0, 0, 0))[0]
    DisEndLocator   = mc.spaceLocator(p=(0, 0, 0))[0]
    DistanceNode    = mc.createNode('distanceBetween')
    DisDivideNode   = mc.createNode('multiplyDivide')
    
    mc.delete(mc.parentConstraint(BendJoints[0],  DisStartLocator))
    mc.delete(mc.parentConstraint(BendJoints[-1], DisEndLocator))
    
    mc.connectAttr('%s.worldPosition[0]'%mc.listRelatives(DisStartLocator, s=True, path=True)[0], '%s.point1'%DistanceNode)
    mc.connectAttr('%s.worldPosition[0]'%mc.listRelatives(DisEndLocator,   s=True, path=True)[0], '%s.point2'%DistanceNode)
    
    mc.connectAttr('%s.distance'%DistanceNode, '%s.input1Y'%DisDivideNode)
    mc.setAttr('%s.input2Y'%DisDivideNode, mc.getAttr('%s.input1Y'%DisDivideNode))
    mc.setAttr('%s.operation'%DisDivideNode,  2)
    
    for jnt in BendJoints:
        mc.connectAttr('%s.outputY'%DisDivideNode, '%s.sy'%jnt)
    
    # -> Rig
    
    # - bend joints -
    BendIKHandle = mc.ikHandle(sj=BendJoints[0], ee=BendJoints[1], sol='ikRPsolver')[0]
    VectorPosition = mc.getAttr('%s.poleVector'%BendIKHandle)[0]
    
    VectorLoc = mc.spaceLocator(p=(0, 0, 0))[0]
    mc.delete(mc.parentConstraint(Joints[0], VectorLoc))
    mc.move(VectorPosition[0], VectorPosition[1], VectorPosition[2], VectorLoc, r=True)
    
    
    for i, jnt in enumerate(BendJoints):
        if i > 0:
            mc.connectAttr('%s.rotate'%BendJoints[0], '%s.rotate'%jnt)
    
    # - skin bind Curve -
    mc.skinCluster(BendJoints, attachCurve)
    mc.skinCluster(BendJoints, upVectorCurve)
    
    # - make Cotrol -
    localStartControl = mc.circle(nr=(0, 1, 0), ch=False)[0]
    localEndControl   = mc.circle(nr=(0, 1, 0), ch=False)[0]
    
    localStartControlGrp = mc.group(localStartControl)
    localEndControlGrp   = mc.group(localEndControl)    

    
    startControl = mc.circle(nr=(0, 1, 0), ch=False)[0]
    endControl   = mc.circle(nr=(0, 1, 0), ch=False)[0]
    
    startControlGrp = mc.group(startControl)
    endControlGrp   = mc.group(endControl)
    
    #  - match position -
    mc.delete(mc.parentConstraint(Joints[0],  localStartControlGrp))
    mc.delete(mc.parentConstraint(Joints[-1], localEndControlGrp))   
    
    mc.delete(mc.parentConstraint(Joints[0],  startControlGrp))
    mc.delete(mc.parentConstraint(Joints[-1], endControlGrp))  
    
    # - add Attribute -
    mc.addAttr(endControl, ln='range', min=0, max=3, dv=1)
    mc.setAttr('%s.range'%endControl, k=False, cb=True)
    
    
    # - connect -
    for i, attr in enumerate(('tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v')):
        
        mc.connectAttr('%s.%s'%(startControl, attr), '%s.%s'%(localStartControl, attr))
        
        if i < 3:
            multiNode = mc.createNode('multDoubleLinear')
            mc.connectAttr('%s.%s'%(endControl, attr), '%s.input1'%multiNode)
            mc.connectAttr('%s.range'%endControl, '%s.input2'%multiNode)
            mc.connectAttr('%s.output'%multiNode, '%s.%s'%(localEndControl, attr))
        else:
            mc.connectAttr('%s.%s'%(endControl, attr),   '%s.%s'%(localEndControl, attr))

        
        if i > 2:
            mc.setAttr('%s.%s'%(startControl, attr), l=True, k=False)
            mc.setAttr('%s.%s'%(endControl, attr), l=True, k=False)

    # - constraint -
    mc.pointConstraint(localStartControl, BendJoints[0])
    #mc.aimConstraint(localEndControl, BendJoints[0], aim=(0,1,0), wu=(1,0,0), wuo=VectorLoc, wut='object')
    mc.poleVectorConstraint(VectorLoc, BendIKHandle)
    
    
    
    # -> Compile
    JointGrp   = mc.group(Joints, moreWeghtJnt)
    LocatorGrp = mc.group(upLocators)
    CurveGrp   = mc.group(attachCurve, upVectorCurve, baseDistanceCurve)
    
    BendJointGrp = mc.group(BendJoints[0])
    
    controlGrp      = mc.group(startControlGrp, endControlGrp)
    localControlGrp = mc.group(localStartControlGrp, localEndControlGrp)
    setGrp     = mc.group(JointGrp, BendJointGrp, LocatorGrp, CurveGrp)
    
    rootGrp = mc.group(controlGrp, localControlGrp, setGrp)
    
    mc.parent(DisStartLocator, localStartControl)
    mc.parent(DisEndLocator, localEndControl)
    
    mc.parent(VectorLoc, localStartControl)
    mc.parent(BendIKHandle, localEndControl)
    mc.setAttr('%s.translate'%BendIKHandle, 0,0,0)
    
        
    # -> rename
    # - bend set -
    DisStartLocator    = mc.rename(DisStartLocator,    'C_HSbendDisStart_loc_0')
    DisEndLocator      = mc.rename(DisEndLocator,      'C_HSbendDisEnd_loc_0')  

    for i, jnt in enumerate(BendJoints):
        BendJoints[i] = mc.rename(jnt, 'C_HSbend%s_jnt_0'%string.uppercase[i])
    BendJointGrp = mc.rename(BendJointGrp, 'C_HSbendJoint_jnh_0')
    
    VectorLoc = mc.rename(VectorLoc, 'C_HSBendVector_loc_0')
    BendIKHandle = mc.rename(BendIKHandle, 'C_BendJointIK_hdl_0')
    
    # - joint -
    for i, jnt in enumerate(Joints):
        Joints[i] = mc.rename(jnt, 'C_headStreatch%s_bnd_0'%string.uppercase[i])
    
    moreWeghtJnt = mc.rename(moreWeghtJnt, 'C_headStreatch_bnd_0')   
    JointGrp = mc.rename(JointGrp, 'C_headStreatch_bndG_0')
    
    # - locator -
    for i, loc in enumerate(upLocators):
        upLocators[i] = mc.rename(loc, 'C_headStreatchUp%s_loc_0'%string.uppercase[i])
        
    mc.rename(LocatorGrp, 'C_headStreatch_locG_0')
    
    # - control -
    startControl = mc.rename(startControl, 'C_HSstart_ctl_0')
    endControl   = mc.rename(endControl, 'C_HSend_ctl_0')
    
    startControlGrp = mc.rename(startControlGrp, 'C_HSstart_cth_0')
    endControlGrp   = mc.rename(endControlGrp, 'C_HSend_cth_0')

    localStartControl = mc.rename(localStartControl, 'C_HSstartLocal_ctl_0')
    localEndControl   = mc.rename(localEndControl, 'C_HSendLocal_ctl_0')
    
    localStartControlGrp = mc.rename(localStartControlGrp, 'C_HSstartLocal_cth_0')
    localEndControlGrp   = mc.rename(localEndControlGrp, 'C_HSendLocal_cth_0')

    controlGrp      = mc.rename(controlGrp, 'C_headStreatch_cth_0')
    localControlGrp = mc.rename(localControlGrp, 'C_headStreatchLocal_cth_0')

    # - curve -
    attachCurve       = mc.rename(attachCurve, 'C_HSJointAttach_cus_0')
    upVectorCurve     = mc.rename(upVectorCurve, 'C_HSLocatorAttach_cus_0')
    baseDistanceCurve = mc.rename(baseDistanceCurve,'C_HSDistance_cus_0')
    
    mc.rename(CurveGrp, 'C_HeadStreatch_cusgrp_0')

    # - comp group -
    mc.rename(setGrp, 'C_headStreatch_setg_0')
    mc.rename(rootGrp, 'C_headStreatch_grp_0')

    # -> clean up
    mc.hide(upLocators)
    mc.hide(upVectorCurve, baseDistanceCurve)
    mc.hide(localControlGrp)
    mc.hide(BendJointGrp)
    
    mc.setAttr('%s.template'%attachCurve, 1)
    
    # -> create selection sets
    mc.sets(Joints, moreWeghtJnt, name='C_HSJoint_set_0')
    mc.sets(startControl, endControl, name='C_HSControl_set_0')